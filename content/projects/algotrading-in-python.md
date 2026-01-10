---
title: "Algorithmic Trading in Python"
date: 2025-04-01
description: "Modernized freeCodeCamp algorithmic trading course with yfinance, backtesting, and portfolio optimization. Updated Python code for S&P 500, momentum, and value strategies."
links:
  github: "https://github.com/akapet00/algotrading-in-python"
tags: ["Python", "Finance", "Quantitative Trading", "Portfolio Optimization", "freeCodeCamp", "yfinance", "Backtesting", "S&P 500"]
featured: false
draft: false
---

A modernized version of the popular [Algorithmic Trading Course](https://www.youtube.com/watch?v=xfzGZB4HhEE) by freeCodeCamp.org, updated to work with current tools and extended with proper backtesting.

## What's in the Original Course

The freeCodeCamp course teaches three strategies:

- **Equal-Weight S&P 500** — Replicates an index fund by equally weighting all constituents
- **Quantitative Momentum** — Ranks stocks based on price performance
- **Quantitative Value** — Identifies undervalued stocks using multiple valuation metrics

## What's New

The original course relied on the IEX Cloud API, which has since become deprecated and inaccessible for most users. This repository fixes that and adds features the original lacked:

- **Working data source** — Replaced IEX Cloud with yfinance for reliable, free market data
- **Multithreaded fetching** — Optimized data retrieval across hundreds of securities
- **Backtesting** — Added performance validation against SPY benchmark
- **Portfolio optimization** — Integrated cvxpy for proper mean-variance optimization in the value strategy

## Why This Matters

The original course videos remain one of the best free introductions to algorithmic trading, but without working code, learners hit a wall. This repository makes the course usable again while demonstrating how to validate strategies before risking real capital.
