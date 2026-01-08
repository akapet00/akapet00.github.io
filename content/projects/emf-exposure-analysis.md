---
title: "EMF Exposure Analysis"
date: 2023-10-01
description: "Python tools for high-frequency electromagnetic dosimetry and human exposure assessment. Developed during my graduate studies."
links:
  github: "https://github.com/akapet00/EMF-exposure-analysis"
tags: ["Python", "Dosimetry", "Research"]
featured: true
draft: false
---

A collection of tools and reproducible research code for analyzing human exposure to electromagnetic fields, developed during my PhD research.

## Overview

This project tackles the challenge of assessing how radio-frequency electromagnetic fields (6 GHz to 300 GHz) interact with the human body. As wireless technology moves into millimeter-wave frequencies, understanding exposure becomes increasingly important.

## dosipy

The core of this project is `dosipy`, a Python package for high-frequency EM and thermal dosimetry simulation. It includes:

- Data models for anatomical structures
- Numerical integration utilities for complex 3D surfaces
- A bio-heat equation solver for thermal analysis
- Automatic differentiation for EM field assessment

## Research Applications

The `playground` directory contains code that reproduces results from several peer-reviewed publications:

- Spatial averaging of absorbed power density on realistic body models
- Incident power density assessment on anatomical human models
- Machine learning-assisted antenna modeling
- Exposure scenarios involving wearable devices

## Installation

```bash
git clone https://github.com/akapet00/EMF-exposure-analysis.git
cd EMF-exposure-analysis
pip install .
```
