---
title: Example 2 -- Barnes-Hut Algorithm
date: 2017.12.2
tags: python, c++, programming
---

The Barnes–Hut simulation (Josh Barnes and Piet Hut) is an approximation algorithm for performing an n-body simulation. It is notable for having order O(n log n) compared to a direct-sum algorithm which would be O(n2).[1]

The simulation volume is usually divided up into cubic cells via an octree (in a three-dimensional space), so that only particles from nearby cells need to be treated individually, and particles in distant cells can be treated as a single large particle centered at the cell's center of mass (or as a low-order multipole expansion). This can dramatically reduce the number of particle pair interactions that must be computed.

Some of the most demanding high-performance computing projects do computational astrophysics using the Barnes–Hut treecode algorithm,[2] such as DEGIMA[citation needed].

$$f(x_0,x_i) = f(x_0,(x_i-x_d) + x_d)$$