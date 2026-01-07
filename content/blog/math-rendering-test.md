---
title: "Math Rendering with KaTeX"
date: 2026-01-04
categories: ["Tutorial"]
tags: ["math", "latex"]
description: "A demonstration of mathematical equation rendering using KaTeX."
math: true
---

This post demonstrates how mathematical equations are rendered on this site using KaTeX.

## Inline Math

Einstein's famous equation $E = mc^2$ shows the relationship between mass and energy.

The quadratic formula gives us $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.

## Block Equations

The Gaussian integral:

$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

Maxwell's equations in differential form:

$$\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}$$

$$\nabla \cdot \mathbf{B} = 0$$

$$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$$

$$\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}$$

## Matrices

A rotation matrix in 2D:

$$R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$

## Summary

KaTeX provides fast and beautiful math rendering. Just add `math: true` to the frontmatter of any post that needs equations.
