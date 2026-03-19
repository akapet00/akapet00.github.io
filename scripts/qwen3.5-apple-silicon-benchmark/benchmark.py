# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx",
#     "mlx-lm>=0.31.1",
# ]
# ///
"""Benchmark Qwen3.5-35B-A3B across local inference engines.

Measures generation tokens/second for ollama, llama.cpp, and MLX
(both HTTP server and Python API) in thinking and non-thinking modes.

Prerequisites:
- Ollama: Install ollama and pull qwen3.5:35b model.
- llama.cpp: Build llama.cpp with OpenAI API and streaming support, quantize model with unsloth's script, and start server with appropriate config for thinking/non-thinking modes.
- MLX HTTP: Install MLX and start the HTTP server with the Qwen3.5-35B-A3B-4bit model.
- MLX Python: Install MLX and ensure the Qwen3.5-35B-A3B-4bit model is available for direct loading

Usage:
    uv run scripts/qwen3.5-apple-silicon-benchmark/benchmark.py --engine ollama --repetitions 10
    uv run scripts/qwen3.5-apple-silicon-benchmark/benchmark.py --engine llamacpp --thinking-modes thinking --repetitions 10
    uv run scripts/qwen3.5-apple-silicon-benchmark/benchmark.py --engine llamacpp --thinking-modes non-thinking --repetitions 10
    uv run scripts/qwen3.5-apple-silicon-benchmark/benchmark.py --engine mlx-http --repetitions 10
    uv run scripts/qwen3.5-apple-silicon-benchmark/benchmark.py --engine mlx-python --repetitions 10
    uv run scripts/qwen3.5-apple-silicon-benchmark/benchmark.py --summarize
"""

import argparse
import json
import math
import platform
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROMPT = "Write a Python function that prints FizzBuzz for numbers 1 to 100."
SYSTEM_PROMPT = "You are a an expert software engineer specialized in Python."

PARAM_SETS: dict[str, dict[str, float]] = {
    "deterministic": {
        "temperature": 0.0,
        "max_tokens": 2048,
    },
    "coding": {
        "temperature": 0.6,
        "top_p": 0.95,
        "max_tokens": 2048,
    },
}

ENGINE_CONFIGS: dict[str, dict[str, str | None]] = {
    "ollama": {
        "base_url": "http://127.0.0.1:11434",
        "model": "qwen3.5:35b",
        "quantization_note": "Standard Q4_K_M (~4.5 bits/weight average)",
    },
    "llamacpp": {
        "base_url": "http://127.0.0.1:8081/v1",
        "model": "unsloth/Qwen3.5-35B-A3B-GGUF:UD-Q4_K_XL",
        "quantization_note": (
            "Unsloth Dynamic Q4_K_XL (important layers upcast to 8/16-bit)"
        ),
    },
    "mlx-http": {
        "base_url": "http://127.0.0.1:8082/v1",
        "model": "~/.local/share/mlx-models/Qwen3.5-35B-A3B-4bit",
        "quantization_note": "MLX 4-bit group quantization",
    },
    "mlx-python": {
        "base_url": None,
        "model": "~/.local/share/mlx-models/Qwen3.5-35B-A3B-4bit",
        "quantization_note": "MLX 4-bit group quantization",
    },
}

REQUEST_TIMEOUT = 300.0  # seconds per request


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class RunResult:
    """Represents the result of a single benchmark run."""

    config: dict
    run_index: int
    generation_tokens: int = 0
    prompt_tokens: int = 0
    generation_tps_native: float | None = None
    prompt_tps_native: float | None = None
    generation_tps_client: float | None = None
    total_seconds: float = 0.0
    finish_reason: str | None = None
    output_length_chars: int = 0
    error: str | None = None


@dataclass
class BenchmarkSuite:
    """Represents the full benchmark suite for a single engine, including metadata and all run results."""

    engine: str
    model_name: str
    quantization_note: str
    timestamp: str
    system_info: dict
    results: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def get_system_info() -> dict:
    """Collect system information for reproducibility."""
    info = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
    }
    # macOS-specific: get chip and memory
    if platform.system() == "Darwin":
        try:
            chip = subprocess.check_output(
                ["/usr/sbin/sysctl", "-n", "machdep.cpu.brand_string"],
                text=True,
            ).strip()
            info["chip"] = chip
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        try:
            mem_bytes = int(
                subprocess.check_output(
                    ["/usr/sbin/sysctl", "-n", "hw.memsize"],
                    text=True,
                ).strip(),
            )
            info["memory_gb"] = round(mem_bytes / (1024**3))
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            pass
    return info


def build_messages() -> list[dict]:
    """Build the chat messages list."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": PROMPT},
    ]


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


# ---------------------------------------------------------------------------
# Engine: Ollama (native API with streaming)
# ---------------------------------------------------------------------------


class OllamaEngine:
    """Inference engine using Ollama's native API with streaming responses."""

    name = "ollama"

    def __init__(self) -> None:
        """Initialize engine with configuration."""
        cfg = ENGINE_CONFIGS["ollama"]
        self.base_url = cfg["base_url"]
        self.model = cfg["model"]
        self.quantization_note = cfg["quantization_note"]

    @property
    def model_name(self) -> str:
        """Return the model name for display purposes."""
        return self.model

    def check_health(self) -> bool:
        """Check the health of the engine."""
        try:
            r = httpx.get(self.base_url, timeout=5.0)
        except httpx.ConnectError:
            return False
        else:
            return r.status_code == 200

    def run(
        self,
        messages: list[dict],
        params: dict,
        thinking: bool,
    ) -> RunResult:
        """Run a single benchmark and return the result."""
        config = {
            "engine": self.name,
            "thinking": thinking,
            "param_set": params.get("_name", "unknown"),
        }
        result = RunResult(config=config, run_index=-1)

        body: dict = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "think": thinking,
            "options": {"num_ctx": 65536},
        }
        # Map params to ollama options
        opts = body["options"]
        if "temperature" in params:
            opts["temperature"] = params["temperature"]
        if "top_p" in params:
            opts["top_p"] = params["top_p"]
        if "max_tokens" in params:
            body["options"]["num_predict"] = params["max_tokens"]

        output_chunks: list[str] = []
        t_start = time.perf_counter()

        try:
            with httpx.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json=body,
                timeout=REQUEST_TIMEOUT,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    msg = chunk.get("message", {})
                    content = msg.get("content", "")
                    if content:
                        output_chunks.append(content)
                    # Final chunk has done=True and timing info
                    if chunk.get("done"):
                        t_end = time.perf_counter()
                        result.total_seconds = t_end - t_start

                        eval_count = chunk.get("eval_count", 0)
                        eval_duration = chunk.get("eval_duration", 0)
                        prompt_eval_count = chunk.get("prompt_eval_count", 0)
                        prompt_eval_duration = chunk.get("prompt_eval_duration", 0)

                        result.generation_tokens = eval_count
                        result.prompt_tokens = prompt_eval_count

                        if eval_duration > 0:
                            result.generation_tps_native = (
                                eval_count / eval_duration * 1e9
                            )
                        if prompt_eval_duration > 0:
                            result.prompt_tps_native = (
                                prompt_eval_count / prompt_eval_duration * 1e9
                            )

                        result.finish_reason = (
                            "stop"
                            if chunk.get("done_reason") == "stop"
                            else chunk.get("done_reason", "unknown")
                        )

            output_text = "".join(output_chunks)
            result.output_length_chars = len(output_text)
            if result.generation_tokens > 0 and result.total_seconds > 0:
                result.generation_tps_client = (
                    result.generation_tokens / result.total_seconds
                )

        except Exception as e:  # noqa: BLE001 Do not catch blind exceptions
            result.error = str(e)
            result.total_seconds = time.perf_counter() - t_start

        return result


# ---------------------------------------------------------------------------
# Engine: llama.cpp (OpenAI-compatible API with streaming)
# ---------------------------------------------------------------------------


class LlamaCppEngine:
    """Inference engine using llama.cpp's OpenAI-compatible API with streaming responses."""

    name = "llamacpp"

    def __init__(self) -> None:
        """Initialize engine with configuration."""
        cfg = ENGINE_CONFIGS["llamacpp"]
        self.base_url = cfg["base_url"]
        self.model = cfg["model"]
        self.quantization_note = cfg["quantization_note"]

    @property
    def model_name(self) -> str:
        """Return the model name for display purposes."""
        return self.model

    def check_health(self) -> bool:
        """Check the health of the engine by making a request to the models endpoint."""
        try:
            r = httpx.get(
                f"{self.base_url}/models",
                timeout=5.0,
            )
        except httpx.ConnectError:
            return False
        else:
            return r.status_code == 200

    def run(
        self,
        messages: list[dict],
        params: dict,
        thinking: bool,
    ) -> RunResult:
        """Run a single benchmark and return the result."""
        config = {
            "engine": self.name,
            "thinking": thinking,
            "param_set": params.get("_name", "unknown"),
        }
        result = RunResult(config=config, run_index=-1)

        body: dict = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if "temperature" in params:
            body["temperature"] = params["temperature"]
        if "top_p" in params:
            body["top_p"] = params["top_p"]
        if "max_tokens" in params:
            body["max_completion_tokens"] = params["max_tokens"]

        output_chunks: list[str] = []
        t_start = time.perf_counter()

        try:
            with httpx.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=body,
                timeout=REQUEST_TIMEOUT,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        break
                    chunk = json.loads(data)

                    # Extract content from delta
                    choices = chunk.get("choices", [])
                    if choices:
                        delta = choices[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            output_chunks.append(content)
                        fr = choices[0].get("finish_reason")
                        if fr:
                            result.finish_reason = fr

                    # Usage info (may appear in final chunk)
                    usage = chunk.get("usage")
                    if usage:
                        result.generation_tokens = usage.get("completion_tokens", 0)
                        result.prompt_tokens = usage.get("prompt_tokens", 0)

                    # llama.cpp timings (in final chunk)
                    timings = chunk.get("timings")
                    if timings:
                        result.generation_tps_native = timings.get(
                            "predicted_per_second",
                        )
                        result.prompt_tps_native = timings.get("prompt_per_second")

            t_end = time.perf_counter()
            result.total_seconds = t_end - t_start

            output_text = "".join(output_chunks)
            result.output_length_chars = len(output_text)
            if result.generation_tokens > 0 and result.total_seconds > 0:
                result.generation_tps_client = (
                    result.generation_tokens / result.total_seconds
                )

        except Exception as e:  # noqa: BLE001 Do not catch blind exceptions
            result.error = str(e)
            result.total_seconds = time.perf_counter() - t_start

        return result


# ---------------------------------------------------------------------------
# Engine: MLX HTTP server (OpenAI-compatible API)
# ---------------------------------------------------------------------------


class MlxHttpEngine:
    """Inference engine using MLX's HTTP server with OpenAI-compatible API and streaming responses."""

    name = "mlx-http"

    def __init__(self) -> None:
        """Initialize engine with configuration."""
        cfg = ENGINE_CONFIGS["mlx-http"]
        self.base_url = cfg["base_url"]
        self.model = str(Path(cfg["model"]).expanduser())
        self.quantization_note = cfg["quantization_note"]

    @property
    def model_name(self) -> str:
        """Return the model name for display purposes."""
        return self.model

    def check_health(self) -> bool:
        """Check the health of the engine by making a request to the models endpoint."""
        try:
            r = httpx.get(
                f"{self.base_url}/models",
                timeout=5.0,
            )
        except httpx.ConnectError:
            return False
        else:
            return r.status_code == 200

    def run(
        self,
        messages: list[dict],
        params: dict,
        thinking: bool,
    ) -> RunResult:
        """Run a single benchmark and return the result."""
        config = {
            "engine": self.name,
            "thinking": thinking,
            "param_set": params.get("_name", "unknown"),
        }
        result = RunResult(config=config, run_index=-1)

        body: dict = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "chat_template_kwargs": {"enable_thinking": thinking},
        }
        if "temperature" in params:
            body["temperature"] = params["temperature"]
        if "top_p" in params:
            body["top_p"] = params["top_p"]
        if "max_tokens" in params:
            body["max_tokens"] = params["max_tokens"]

        output_chunks: list[str] = []
        gen_tokens = 0
        t_start = time.perf_counter()

        try:
            with httpx.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=body,
                timeout=REQUEST_TIMEOUT,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        break
                    chunk = json.loads(data)

                    choices = chunk.get("choices", [])
                    if choices:
                        delta = choices[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            output_chunks.append(content)
                            gen_tokens += 1
                        fr = choices[0].get("finish_reason")
                        if fr:
                            result.finish_reason = fr

                    usage = chunk.get("usage")
                    if usage:
                        result.prompt_tokens = usage.get("prompt_tokens", 0)
                        comp = usage.get("completion_tokens")
                        if comp:
                            gen_tokens = comp

            t_end = time.perf_counter()
            result.total_seconds = t_end - t_start
            result.generation_tokens = gen_tokens

            output_text = "".join(output_chunks)
            result.output_length_chars = len(output_text)
            # MLX HTTP: client-side timing only
            if gen_tokens > 0 and result.total_seconds > 0:
                result.generation_tps_client = gen_tokens / result.total_seconds

        except Exception as e:  # noqa: BLE001 Do not catch blind exceptions
            result.error = str(e)
            result.total_seconds = time.perf_counter() - t_start

        return result


# ---------------------------------------------------------------------------
# Engine: MLX Python (direct mlx_lm API)
# ---------------------------------------------------------------------------


class MlxPythonEngine:
    """Inference engine using MLX's Python API (mlx_lm) for direct model loading and generation."""

    name = "mlx-python"

    def __init__(self) -> None:
        """Initialize engine with configuration."""
        cfg = ENGINE_CONFIGS["mlx-python"]
        self.model_path = str(Path(cfg["model"]).expanduser())
        self.quantization_note = cfg["quantization_note"]
        self._model = None
        self._tokenizer = None

    @property
    def model_name(self) -> str:
        """Return the model name for display purposes."""
        return self.model_path

    def _ensure_loaded(self) -> None:
        """Load the model if it hasn't been loaded yet."""
        import mlx_lm  # noqa: PLC0415

        if self._model is not None:
            return

        resolved = str(Path(self.model_path).expanduser())
        print(f"  Loading model from {resolved}...")
        self._model, self._tokenizer = mlx_lm.load(resolved)
        print("  Model loaded.")

    def check_health(self) -> bool:
        """Check if the model can be loaded successfully."""
        try:
            self._ensure_loaded()
            return self._model is not None  # noqa: TRY300 Try, consider else
        except Exception as e:  # noqa: BLE001 Do not catch blind exceptions
            print(f"  MLX Python load failed: {e}")
            return False

    def run(
        self,
        messages: list[dict],
        params: dict,
        thinking: bool,
    ) -> RunResult:
        """Run a single benchmark and return the result."""
        import mlx_lm  # noqa: PLC0415

        config = {
            "engine": self.name,
            "thinking": thinking,
            "param_set": params.get("_name", "unknown"),
        }
        result = RunResult(config=config, run_index=-1)

        self._ensure_loaded()

        # Apply chat template
        prompt_text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=thinking,
        )

        # Build sampler and generation kwargs
        from mlx_lm.sample_utils import make_sampler  # noqa: PLC0415

        sampler_kwargs: dict = {}
        if "temperature" in params:
            sampler_kwargs["temp"] = params["temperature"]
        if "top_p" in params:
            sampler_kwargs["top_p"] = params["top_p"]
        sampler = make_sampler(**sampler_kwargs)

        max_tokens = params.get("max_tokens", 2048)

        output_chunks: list[str] = []
        t_start = time.perf_counter()

        try:
            response = None
            for response in mlx_lm.stream_generate(
                self._model,
                self._tokenizer,
                prompt=prompt_text,
                max_tokens=max_tokens,
                sampler=sampler,
            ):
                output_chunks.append(response.text)

            t_end = time.perf_counter()
            result.total_seconds = t_end - t_start

            output_text = "".join(output_chunks)
            result.output_length_chars = len(output_text)

            # Extract metrics from final response
            if response is not None:
                result.generation_tokens = response.generation_tokens
                result.prompt_tokens = response.prompt_tokens
                result.generation_tps_native = response.generation_tps
                result.prompt_tps_native = response.prompt_tps
                result.finish_reason = response.finish_reason or "unknown"

            if result.generation_tokens > 0 and result.total_seconds > 0:
                result.generation_tps_client = (
                    result.generation_tokens / result.total_seconds
                )

        except Exception as e:  # noqa: BLE001 Do not catch blind exceptions
            result.error = str(e)
            result.total_seconds = time.perf_counter() - t_start

        return result


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

ENGINE_CLASSES: dict[str, type] = {
    "ollama": OllamaEngine,
    "llamacpp": LlamaCppEngine,
    "mlx-http": MlxHttpEngine,
    "mlx-python": MlxPythonEngine,
}


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def run_benchmark(
    engine_name: str,
    thinking_modes: list[bool],
    repetitions: int,
    output_dir: Path,
) -> None:
    """Run the full benchmark for a single engine."""
    engine = ENGINE_CLASSES[engine_name]()
    print(f"\n{'=' * 60}")
    print(f"Engine: {engine.name}")
    print(f"Model:  {engine.model_name}")
    print(f"Quant:  {engine.quantization_note}")
    print(f"{'=' * 60}")

    # Health check
    print("\nChecking server health...")
    if not engine.check_health():
        print(f"ERROR: {engine.name} server is not reachable. Aborting.")
        sys.exit(1)
    print("Server is up.\n")

    messages = build_messages()
    all_results: list[dict] = []
    prev_thinking = None

    for thinking in thinking_modes:
        # llamacpp needs server restart for thinking mode toggle
        if (
            engine_name == "llamacpp"
            and prev_thinking is not None
            and thinking != prev_thinking
        ):
            mode_label = "thinking" if thinking else "non-thinking"
            print(f"\n{'!' * 60}")
            print(f"Please restart llama.cpp server for {mode_label} mode.")
            if thinking:
                print("Start WITHOUT --reasoning-budget 0")
            else:
                print("Start WITH --reasoning-budget 0")
            print(f"{'!' * 60}")
            input("Press Enter when the server is ready...")
            print("Checking server health...")
            if not engine.check_health():
                print(f"ERROR: {engine.name} server is not reachable.")
                sys.exit(1)
            print("Server is up.\n")

        prev_thinking = thinking

        for param_name, param_values in PARAM_SETS.items():
            params = {**param_values, "_name": param_name}
            think_label = "thinking" if thinking else "non-thinking"
            print(f"--- {think_label} | {param_name} ---")

            # Warmup run
            print("  Warmup run...", end=" ", flush=True)
            warmup = engine.run(messages, params, thinking)
            if warmup.error:
                print(f"WARN: warmup error: {warmup.error}")
            else:
                print(f"done ({warmup.total_seconds:.1f}s)")

            gen_tps_native_vals: list[float] = []
            gen_tps_client_vals: list[float] = []

            for i in range(repetitions):
                print(
                    f"  Run {i + 1}/{repetitions}...",
                    end=" ",
                    flush=True,
                )
                r = engine.run(messages, params, thinking)
                r.run_index = i

                if r.error:
                    print(f"ERROR: {r.error}")
                else:
                    native_str = (
                        f"{r.generation_tps_native:.1f}"
                        if r.generation_tps_native
                        else "N/A"
                    )
                    client_str = (
                        f"{r.generation_tps_client:.1f}"
                        if r.generation_tps_client
                        else "N/A"
                    )
                    print(
                        f"gen_tps native={native_str} "
                        f"client={client_str} "
                        f"({r.total_seconds:.1f}s, "
                        f"{r.generation_tokens} tokens, "
                        f"finish={r.finish_reason})",
                    )
                    if r.generation_tps_native is not None:
                        gen_tps_native_vals.append(r.generation_tps_native)
                    if r.generation_tps_client is not None:
                        gen_tps_client_vals.append(r.generation_tps_client)

                all_results.append(asdict(r))

            # Per-config summary
            if gen_tps_native_vals:
                mean, std = compute_stats(gen_tps_native_vals)
                print(f"  Native gen tok/s: {mean:.1f} +/- {std:.1f}")
            if gen_tps_client_vals:
                mean, std = compute_stats(gen_tps_client_vals)
                print(f"  Client gen tok/s: {mean:.1f} +/- {std:.1f}")
            print()

    # Save results
    suite = BenchmarkSuite(
        engine=engine.name,
        model_name=engine.model_name,
        quantization_note=engine.quantization_note,
        timestamp=datetime.now(tz=UTC).isoformat(),
        system_info=get_system_info(),
        results=all_results,
    )
    save_results(suite, output_dir)


def save_results(suite: BenchmarkSuite, output_dir: Path) -> None:
    """Save benchmark results to a JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
    filename = f"{suite.engine}_{ts}.json"
    filepath = output_dir / filename
    with Path.open(filepath, "w", encoding="utf-8") as f:
        json.dump(asdict(suite), f, indent=2, ensure_ascii=False)
    print(f"Results saved to {filepath}")


# ---------------------------------------------------------------------------
# Summarize mode
# ---------------------------------------------------------------------------


def summarize_results(output_dir: Path) -> None:
    """Read all JSON result files and print a comparison table."""
    json_files = sorted(output_dir.glob("*.json"))
    if not json_files:
        print(f"No result files found in {output_dir}")
        return

    print(f"\nFound {len(json_files)} result file(s) in {output_dir}\n")

    # Collect rows: (engine, thinking, param_set) -> (native_vals, client_vals)
    grouped: dict[tuple, dict[str, list[float]]] = {}

    for fp in json_files:
        with Path.open(fp) as f:
            data = json.load(f)
        engine = data.get("engine", "unknown")
        for r in data.get("results", []):
            cfg = r.get("config", {})
            thinking = cfg.get("thinking", False)
            param_set = cfg.get("param_set", "unknown")
            key = (engine, thinking, param_set)
            if key not in grouped:
                grouped[key] = {"native": [], "client": []}
            if r.get("generation_tps_native") is not None and r.get("error") is None:
                grouped[key]["native"].append(r["generation_tps_native"])
            if r.get("generation_tps_client") is not None and r.get("error") is None:
                grouped[key]["client"].append(r["generation_tps_client"])

    print_summary_table(grouped)


def print_summary_table(
    grouped: dict[tuple, dict[str, list[float]]],
) -> None:
    """Print a formatted summary table."""
    header = (
        f"{'Engine':<12} | {'Thinking':<9} | {'Params':<14} | "
        f"{'Gen tok/s (native)':<20} | {'Gen tok/s (client)':<20} | "
        f"{'Runs':<4}"
    )
    sep = "-" * len(header)
    print(header)
    print(sep)

    for key in sorted(grouped.keys()):
        engine, thinking, param_set = key
        vals = grouped[key]
        think_str = "yes" if thinking else "no"

        if vals["native"]:
            mean, std = compute_stats(vals["native"])
            native_str = f"{mean:.1f} +/- {std:.1f}"
        else:
            native_str = "N/A"

        if vals["client"]:
            mean, std = compute_stats(vals["client"])
            client_str = f"{mean:.1f} +/- {std:.1f}"
        else:
            client_str = "N/A"

        n_runs = max(len(vals["native"]), len(vals["client"]))
        print(
            f"{engine:<12} | {think_str:<9} | {param_set:<14} | "
            f"{native_str:<20} | {client_str:<20} | {n_runs:<4}",
        )

    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Benchmark Qwen3.5-35B-A3B across local inference engines.",
    )
    parser.add_argument(
        "--engine",
        choices=list(ENGINE_CLASSES.keys()),
        help="Engine to benchmark.",
    )
    parser.add_argument(
        "--thinking-modes",
        nargs="+",
        choices=["thinking", "non-thinking"],
        default=["thinking", "non-thinking"],
        help="Thinking modes to test (default: both).",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        default=10,
        help="Number of measured runs per config (default: 10).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "results",
        help="Directory to save result JSON files.",
    )
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Summarize existing results instead of running benchmarks.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the benchmark or summarize results based on command-line arguments."""
    args = parse_args()

    if args.summarize:
        summarize_results(args.output_dir)
        return

    if not args.engine:
        print("ERROR: --engine is required (unless using --summarize).")
        sys.exit(1)

    thinking_modes = [mode == "thinking" for mode in args.thinking_modes]

    run_benchmark(
        engine_name=args.engine,
        thinking_modes=thinking_modes,
        repetitions=args.repetitions,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
