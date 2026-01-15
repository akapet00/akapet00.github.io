---
title: "Normal Estimation"
date: 2024-02-01
description: "Comparison of surface normal estimation methods for point clouds: PCA, weighted least squares, and B-spline smoothing. Python implementation with Jupyter notebooks."
links:
  github: "https://github.com/akapet00/normal-estimation"
  article: "https://medium.com/@akapet00/why-you-should-consider-b-splines-for-surface-normal-estimation-898c65ef0351"
tags: ["Python", "3D Geometry", "Point Cloud", "Normal Estimation", "B-Splines", "PCA", "Surface Reconstruction"]
featured: false
draft: false
---

A comparison of several algorithms for computing surface normal vectors from point cloud data, a fundamental task in 3D geometry processing.

## Methods Covered

The `primer.ipynb` notebook explores and compares different approaches:

- **PCA-based estimation** &mdash; Using principal component analysis on local neighborhoods
- **Weighted least squares** &mdash; Fitting local planes with distance-based weighting
- **Bivariate smoothing splines** &mdash; Fitting smooth B-spline surfaces and computing normals analytically

## Why Smoothing Splines?

While neural network-based methods dominate modern normal estimation, bivariate smoothing splines offer a compelling alternative. They strike a balance between simplicity, efficiency, and robustness, achieving results comparable to some neural network approaches while far outperforming traditional methods like PCA.

Key advantages:
- **Computational simplicity** &mdash; No training required, works out of the box
- **Robustness to irregular sampling** &mdash; Handles non-uniform and inhomogeneous point clouds well
- **Exceptional on clean data** &mdash; Ideal for synthetic data applications where noise is minimal

The smoothing spline approach fits a continuous surface to local point neighborhoods, allowing normals to be computed analytically from the surface derivatives rather than estimated from discrete point configurations.
