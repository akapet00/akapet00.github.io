---
title: "Point Cloud Central"
date: 2021-03-01
description: "Experiments and techniques for processing and analyzing 3D point cloud data."
links:
  github: "https://github.com/akapet00/point-cloud-central"
tags: ["3D Geometry", "Point-Cloud Processing", "Surface Reconstruction", "Normal Estimation"]
featured: false
draft: false
---

A playground for experimenting with point cloud processing techniques, from feature extraction to surface reconstruction.

## What's Inside

A series of notebooks that build on each other:

- **Geometry feature extraction** — Computing local geometric properties from raw point data
- **Optimal neighborhood selection** — Finding the right scale for local analysis
- **Surface point extraction** — Isolating surface points from volumetric data
- **Surface reconstruction** — Turning scattered points back into continuous surfaces

## Why Point Clouds

Point clouds are everywhere — LiDAR scans, depth cameras, medical imaging, simulation outputs. But they're just unstructured sets of coordinates. Extracting meaningful geometry from them requires careful processing, and this repo is where I test different approaches.

## Installation

```bash
git clone https://github.com/akapet00/point-cloud-central.git
cd point-cloud-central
uv sync
```