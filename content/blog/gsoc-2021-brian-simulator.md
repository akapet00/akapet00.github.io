---
title: "GSoC 2021: Simulation-Based Inference for the Brian Simulator"
date: 2021-08-23
categories: ["Open Source"]
tags: ["GSoC", "Brian2", "Simulation-Based Inference", "Computational Neuroscience"]
description: "My experience as a Google Summer of Code 2021 student, integrating simulation-based inference into the Brian simulator's model fitting toolbox."
draft: false
---

May 17th, 2021. Sitting on my couch exhausted, I turn on my laptop and check my mail:

> Your proposal *Support of the simulation-based inference with the model fitting toolbox* has been accepted! Welcome to GSoC 2021!

I didn't expect to get in. I was equally thrilled and terrified.

## The Project

I worked with my mentor Marcel Stimberg on integrating the [sbi library](https://www.mackelab.org/sbi/) into the [brian2modelfitting](https://brian2modelfitting.readthedocs.io/) toolbox under the [Brian simulator](https://briansimulator.org/) project.

Brian is a free, open-source simulator for biological neurons and spiking neural networks. The model fitting toolbox helps users find optimal parameters for recorded traces and spike trains. My goal was to extend it with simulation-based inference techniques.

Instead of returning a single set of optimal parameters, the new functionality provides the **full posterior distribution** over parameters. This lets researchers understand not just what parameters fit best, but how uncertain those estimates are.

## What I Built

Over the summer, I:

- Created a wrapper class for simulation-based inference that integrates seamlessly with the existing toolbox
- Added support for all inference techniques available in the sbi library
- Implemented efficient storage and loading of simulated data and trained neural density estimators
- Built visualization tools for exploring the posterior distribution
- Added support for multiple output variables and spike train observations
- Contributed an example to the [antropy](https://github.com/raphaelvallat/antropy) package showing entropy metrics for voltage traces

The code is available in the [brian2modelfitting repository](https://github.com/brian-team/brian2modelfitting), with the main contribution in [PR #64](https://github.com/brian-team/brian2modelfitting/pull/64).

## What I Learned

**Technical skills**: Simulation-based inference, neural density estimation, computational neuroscience, and a lot of software engineering best practices.

**Soft skills**: As a non-native English speaker, I became more confident communicating with researchers in the field. Weekly meetings with Marcel taught me how to scope work, handle blocking issues, and maintain momentum on a long project.

**Research breadth**: Coming from computational electromagnetism, this project pushed me into computational neuroscience. The techniques I learned — particularly around inference and parameter estimation — have applications back in my own field.

## Advice for Future GSoC Students

GSoC is hard. Sometimes extremely stressful. I had to balance university obligations and health problems while meeting deadlines. But it's worth it.

My advice:
- Don't hesitate to apply
- Reach out to potential mentors early
- Start writing tests sooner than you think you need to
- Be a good person and do what you love

It all pays off when you submit that last pull request.

## References

Key papers that informed this work:

- Cranmer et al. (2020). [The frontier of simulation-based inference](https://doi.org/10.1073/pnas.1912789117). PNAS.
- Gonçalves et al. (2020). [Training deep neural density estimators to identify mechanistic models of neural dynamics](https://doi.org/10.7554/eLife.56261). eLife.
- Tejero-Cantero et al. (2020). [sbi: A toolkit for simulation-based inference](https://doi.org/10.21105/joss.02505). JOSS.
