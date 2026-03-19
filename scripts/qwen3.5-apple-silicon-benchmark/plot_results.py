"""Generate a horizontal bar chart from benchmark results.

Usage:
    uv run python scripts/qwen3.5-apple-silicon-benchmark/plot_results.py
"""

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import ticker

RESULTS_DIR = Path(__file__).parent / "results"
OUTPUT_PATH = (
    Path(__file__).parents[2]
    / "static"
    / "images"
    / "blog"
    / "qwen3.5-apple-silicon-benchmark"
    / "qwen3.5-apple-silicon-benchmark-results.png"
)

# Engine display order (top to bottom = fastest to slowest)
ENGINES = ["mlx-python", "mlx-http", "llamacpp", "ollama"]
ENGINE_DISPLAY = {
    "mlx-python": "mlx-py",
    "mlx-http": "mlx-http",
    "llamacpp": "llama.cpp",
    "ollama": "Ollama",
}

TEAL_DARK = "#0d9488"
TEAL_LIGHT = "#5eead4"

# Subplot grid: rows = param_set, cols = thinking
PARAM_SETS = ["deterministic", "coding"]
PARAM_DISPLAY = {"deterministic": "deterministic", "coding": "coding-mode"}
THINKING_MODES = [True, False]
THINKING_DISPLAY = {True: "think", False: "no-think"}

# Match blog monospace font stack
FONT_FAMILY = "monospace"


def load_results() -> dict[tuple[str, bool, str], dict[str, list[float]]]:
    """Load all JSON results and group by (engine, thinking, param_set)."""
    grouped: dict[tuple[str, bool, str], dict[str, list[float]]] = {}
    for fp in sorted(RESULTS_DIR.glob("*.json")):
        with fp.open() as f:
            data = json.load(f)
        engine = data["engine"]
        for r in data["results"]:
            if r.get("error"):
                continue
            cfg = r["config"]
            key = (engine, cfg["thinking"], cfg["param_set"])
            if key not in grouped:
                grouped[key] = {"native": [], "client": []}
            if r.get("generation_tps_native") is not None:
                grouped[key]["native"].append(r["generation_tps_native"])
            if r.get("generation_tps_client") is not None:
                grouped[key]["client"].append(r["generation_tps_client"])
    return grouped


def compute_stats(values: list[float]) -> tuple[float, float]:
    """Return (mean, std) for a list of values."""
    if not values:
        return (0.0, 0.0)
    n = len(values)
    mean = sum(values) / n
    if n < 2:
        return (mean, 0.0)
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    return (mean, math.sqrt(variance))


def plot(grouped: dict) -> None:
    """Produce and save the 2x2 subplot horizontal bar chart."""
    plt.rcParams.update(
        {
            "font.family": FONT_FAMILY,
            "font.size": 14,
        },
    )

    fig, axes = plt.subplots(
        nrows=2,
        ncols=2,
        figsize=(14, 9),
        sharey=True,
        sharex=True,
    )
    fig.patch.set_facecolor("white")

    x_max = 0.0
    bar_height = 0.32
    n_engines = len(ENGINES)
    y_positions = list(range(n_engines))

    for row_idx, param_set in enumerate(PARAM_SETS):
        for col_idx, thinking in enumerate(THINKING_MODES):
            ax = axes[row_idx][col_idx]
            ax.set_facecolor("white")

            # Collect data for this subplot (engines in order)
            for i, engine in enumerate(ENGINES):
                key = (engine, thinking, param_set)
                vals = grouped.get(key, {"native": [], "client": []})

                client_mean, client_std = compute_stats(vals["client"])
                native_mean, native_std = compute_stats(vals["native"])
                has_native = len(vals["native"]) > 0

                # Client-side bar
                bar_y = i - bar_height / 2 if has_native else i
                ax.barh(
                    bar_y,
                    client_mean,
                    bar_height,
                    xerr=client_std,
                    color=TEAL_DARK,
                    edgecolor="white",
                    linewidth=0.5,
                    capsize=3,
                    error_kw={"ecolor": "#333", "linewidth": 1.2, "capthick": 1.2},
                )
                # White label inside bar, left-aligned
                ax.text(
                    3,
                    bar_y,
                    f"{client_mean:.2f}",
                    va="center",
                    ha="left",
                    fontsize=12,
                    fontweight="bold",
                    color="white",
                    fontfamily=FONT_FAMILY,
                )

                # Native bar (where available)
                native_bar_y = i + bar_height / 2
                if has_native:
                    ax.barh(
                        native_bar_y,
                        native_mean,
                        bar_height,
                        xerr=native_std,
                        color=TEAL_LIGHT,
                        edgecolor="white",
                        linewidth=0.5,
                        capsize=3,
                        error_kw={
                            "ecolor": "#333",
                            "linewidth": 1.2,
                            "capthick": 1.2,
                        },
                    )
                    ax.text(
                        3,
                        native_bar_y,
                        f"{native_mean:.2f}",
                        va="center",
                        ha="left",
                        fontsize=12,
                        fontweight="bold",
                        color="#111",
                        fontfamily=FONT_FAMILY,
                    )

                x_max = max(x_max, client_mean, native_mean)

            # Subplot title
            title = f"{THINKING_DISPLAY[thinking]} / {PARAM_DISPLAY[param_set]}"
            ax.set_title(title, fontsize=15, fontweight="bold", pad=10)

            # Axes styling
            ax.set_yticks(y_positions)
            ax.set_yticklabels(
                [ENGINE_DISPLAY[e] for e in ENGINES],
                fontsize=14,
            )
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_color("#ccc")
            ax.spines["bottom"].set_color("#ccc")
            ax.tick_params(colors="#555", labelsize=13)
            ax.invert_yaxis()

    # Shared x-axis label and limits
    for ax in axes.flat:
        ax.set_xlim(0, x_max + 20)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(20))

    for ax in axes[1]:
        ax.set_xlabel("Generation tok/s", fontsize=14, color="#333")

    # Shared legend
    from matplotlib.patches import Patch  # noqa: PLC0415

    legend_elements = [
        Patch(facecolor=TEAL_DARK, label="Client-side"),
        Patch(facecolor=TEAL_LIGHT, label="Native (engine-reported)"),
    ]
    fig.legend(
        handles=legend_elements,
        loc="lower center",
        ncol=2,
        fontsize=13,
        frameon=False,
        bbox_to_anchor=(0.5, -0.02),
    )

    plt.tight_layout()
    fig.subplots_adjust(bottom=0.1)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"Saved to {OUTPUT_PATH}")
    plt.close(fig)


def main() -> None:
    """Load results and generate the chart."""
    grouped = load_results()
    print(f"Loaded {len(grouped)} configurations")
    plot(grouped)


if __name__ == "__main__":
    main()
