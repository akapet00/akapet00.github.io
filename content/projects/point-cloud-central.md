---
title: "Point Cloud Central"
date: 2024-02-10
description: "Python notebooks for 3D point cloud processing: feature extraction, adaptive neighborhood selection, surface point detection, and mesh reconstruction from LiDAR and depth data."
links:
  github: "https://github.com/akapet00/point-cloud-central"
tags: ["Python", "3D Geometry", "Point Cloud", "LiDAR", "Surface Reconstruction", "Normal Estimation", "Feature Extraction"]
featured: false
draft: false
---

A playground for experimenting with point cloud processing techniques, from feature extraction to surface reconstruction.

## What's Inside

A series of notebooks that build on each other:

- **Geometry feature extraction**&mdash;Computing local geometric properties from raw point data
- **[Optimal neighborhood selection](https://medium.com/@akapet00/beyond-one-size-fits-all-enhancing-accuracy-of-point-cloud-features-with-adaptive-neighborhood-f5fd7ff8cca4)**&mdash;Finding the right scale for local analysis by minimizing eigenentropy
- **[Surface point extraction](https://medium.com/@akapet00/a-simple-technique-for-extracting-points-on-the-surface-of-3-d-models-7dc75a7ac75f)**&mdash;Isolating surface points from volumetric data using normal-based detection
- **Surface reconstruction**&mdash;Turning scattered points back into continuous surfaces

## Why Point Clouds

Point clouds are everywhere: LiDAR scans, depth cameras, medical imaging, and simulation outputs. But they're just unstructured sets of coordinates. Extracting meaningful geometry from them requires careful processing, and this repo is where I test different approaches.
