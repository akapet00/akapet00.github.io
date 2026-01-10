---
title: "Peak Spatial Power Density Autodetection"
date: 2023-09-01
description: "Python algorithm for peak spatial-average power density detection on 3D body surfaces. Automated RF exposure assessment for 5G and millimeter-wave safety compliance."
links:
  github: "https://github.com/akapet00/pspd-autodetect"
  paper: "https://ieeexplore.ieee.org/abstract/document/10271620/"
tags: ["Python", "Dosimetry", "Human Exposure", "5G Safety", "Point Cloud", "RF Compliance", "Research"]
featured: true
draft: false
---

The core algorithm from my PhD thesis for automatically finding worst-case electromagnetic exposure regions on realistic 3D body surfaces. Presented at SoftCOM 2023.

## The Problem

Traditional RF safety standards evaluate power density on flat surfaces, but human bodies are anything but flat. When assessing exposure from 5G and millimeter-wave devices, using planar approximations can miss the actual peak exposure on curved anatomical regions.

## The Solution

This algorithm takes a point cloud of any body surface along with power density values at each point, then automatically identifies where the peak spatial-average power density occurs. No manual region selection needed.

## Features

- Works with arbitrary curved surfaces (not just planes)
- Minimal input: just a point cloud and power density values
- Automatically finds worst-case exposure regions
- Includes demo with realistic human head model
- Jupyter notebook tutorial for getting started
