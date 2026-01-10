---
title: "Beyond One-Size-Fits-All: Adaptive Neighborhood Selection for Point Clouds"
date: 2025-02-22
draft: false
categories: ["Point-Cloud Processing"]
tags: ["Python", "3D Geometry", "Point Cloud", "Feature Extraction", "Eigenentropy", "Semantic Segmentation", "LiDAR"]
description: "How to automatically select the optimal neighborhood size for each point in a point cloud using eigenentropy minimization. Better features, better segmentation."
math: true
---

When processing point clouds, a fundamental question arises: how many neighbors should you consider for each point? Use too few and you capture noise instead of structure. Use too many and you blur geometric details across different surfaces.

The common approach is to pick a fixed $k$ — say, 30 nearest neighbors — and use it everywhere. This works reasonably well on uniform point clouds but fails when density varies or when you have both fine details and broad surfaces in the same scene.

What if each point could choose its own optimal neighborhood?

## The Problem with Fixed Neighborhoods

Consider a point on a sharp edge versus a point on a flat wall. The edge point needs a small neighborhood to preserve the geometric discontinuity. The wall point can use a larger neighborhood to average out noise without losing information.

A fixed $k$ forces a compromise. Set it small and flat regions become noisy. Set it large and edges get smoothed away. Neither choice is right for the entire point cloud.

This matters because neighborhood size affects everything downstream: normal estimation, curvature computation, planarity measures, and ultimately segmentation and classification accuracy.

## Eigenentropy as a Quality Metric

The key insight, formalized by [Weinmann et al. 2015](https://www.sciencedirect.com/science/article/abs/pii/S0924271615000349), is that a good neighborhood should have low entropy in its local structure.

For a neighborhood of $k$ points, compute the covariance matrix and extract its eigenvalues $\lambda_1 \geq \lambda_2 \geq \lambda_3$. Normalize them:

$$e_i = \frac{\lambda_i}{\lambda_1 + \lambda_2 + \lambda_3}$$

The eigenentropy follows Shannon's formula:

$$E_\lambda = -\sum_{i=1}^{3} e_i \ln(e_i)$$

Low entropy means the eigenvalues are concentrated — the local structure is well-defined. High entropy means the eigenvalues are spread out — the neighborhood mixes different geometric structures.

## The Algorithm

For each point:

1. Consider a range of neighborhood sizes, say $k \in [10, 100]$
2. For each $k$, compute the eigenentropy of the local covariance matrix
3. Select the $k$ that minimizes eigenentropy

$$
\begin{array}{l}
\hline
\textbf{Algorithm: Optimal Neighborhood Selection} \\
\hline
\textbf{Input: } P = \text{point cloud}, \, k_{\min}, \, k_{\max} \\
\textbf{Output: } k_{\text{opt}}[i] \text{ for each point } p_i \in P \\
\hline
\textbf{for each } p_i \in P \textbf{ do} \\
\quad E_{\min} \leftarrow \infty \\
\quad k_{\text{opt}}[i] \leftarrow k_{\min} \\[0.5em]
\quad \triangleright \text{ Step 1: consider a range of neighborhood sizes} \\
\quad \textbf{for } k \leftarrow k_{\min} \textbf{ to } k_{\max} \textbf{ do} \\
\quad\quad \mathcal{N}_k \leftarrow k \text{ nearest neighbors of } p_i \\
\quad\quad \mathbf{C} \leftarrow \text{cov}(\mathcal{N}_k) \\
\quad\quad \lambda_1, \lambda_2, \lambda_3 \leftarrow \text{eig}(\mathbf{C}) \quad (\lambda_1 \geq \lambda_2 \geq \lambda_3) \\[0.5em]
\quad\quad \triangleright \text{ Step 2: compute eigenentropy} \\
\quad\quad \textbf{for } j \leftarrow 1 \textbf{ to } 3 \textbf{ do} \\
\quad\quad\quad e_j \leftarrow \lambda_j \, / \, (\lambda_1 + \lambda_2 + \lambda_3) \\
\quad\quad E_\lambda \leftarrow -\sum_{j=1}^{3} e_j \ln(e_j) \\[0.5em]
\quad\quad \triangleright \text{ Step 3: select } k \text{ that minimizes eigenentropy} \\
\quad\quad \textbf{if } E_\lambda < E_{\min} \textbf{ then} \\
\quad\quad\quad E_{\min} \leftarrow E_\lambda \\
\quad\quad\quad k_{\text{opt}}[i] \leftarrow k \\[0.5em]
\textbf{return } k_{\text{opt}} \\
\hline
\end{array}
$$

The point automatically gets a small neighborhood if it's near an edge (where mixing scales increases entropy) and a larger one if it's on a smooth surface (where more points reduce noise without increasing entropy).

## Why This Matters

Features computed with adaptive neighborhoods are more distinctive. When you feed them into a classifier for semantic segmentation — labeling points as ground, building, vegetation — accuracy improves significantly compared to fixed-$k$ approaches.

The benefits compound:

- **Better normals** — Each point uses the scale that best captures its local surface
- **Sharper features** — Edges and corners retain their geometric signatures
- **Robust to density variation** — Dense and sparse regions each get appropriate treatment
- **No manual tuning** — The entropy criterion is parameter-free

This is particularly valuable for LiDAR data, where point density varies with distance from the sensor, and for photogrammetric reconstructions with uneven coverage.

## Read More

This post covers the intuition. For implementation details, visualizations, and code, see the full article on Medium:

**[Beyond One-Size-Fits-All: Enhancing Accuracy of Point-Cloud Features with Adaptive Neighborhood Size](https://medium.com/@akapet00/beyond-one-size-fits-all-enhancing-accuracy-of-point-cloud-features-with-adaptive-neighborhood-f5fd7ff8cca4)**

The implementation is available in the [point-cloud-central](https://github.com/akapet00/point-cloud-central) repository in the optimal neighborhood notebook.
