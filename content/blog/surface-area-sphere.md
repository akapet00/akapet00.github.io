---
title: "Assessment of the Surface Area of a Sphere"
date: 2021-11-12
categories: ["Physics-Guided ML"]
tags: ["JAX", "Numerical Methods", "Autodiff"]
description: "Computing the surface area of a sphere using closed-form expressions, Gauss quadrature, convex hull triangulation, and JAX automatic differentiation."
math: true
draft: false
---

A sphere is a common geometrical object in many computational sciences, used to approximate continuous, closed surfaces forming 3D ball-like models. In my research area — computational bioelectromagnetics and dosimetry — and in computational neuroscience, we often approximate the surface of the human head by using a sphere.

Even though this kind of representation of real world objects is a crude geometrical approximation (see figure below), it allows a much simpler simulation setup due to the high symmetry of the solution domain.

![Botero's Mona Lisa](/images/blog/surface-area-sphere-mona-lisa.jpg)

This would have been Mona Lisa had Leonardo da Vinci been a computational scientist. Jokes aside, this painting is the work by the great Fernando Botero, a Colombian figurative artist and sculptor whose signature style often depicts people and figures in hyperbolic manner.

One of the common issues in simulations is the estimation of the total surface area of a portion of the observed object. For regular spherical surfaces, this is fairly easy to do, and yet in this short essay, I will demonstrate the hard way to do it.

## Closed-Form Expression

Let's start by calculating the area of a sphere defined by some radius, $r$, using the following closed-form expression:

$$A = 4 \pi r^2$$

```python
from scipy.constants import pi

r = 1.
A_analytic = 4 * pi * r ** 2
print(f'A = {A_analytic:.6f}')
```

```
A = 12.566371
```

It turns out that the area of a sphere with a radius set to $1$ amounts to approximately 12.566371.

The closed-form expression derives from the surface integral of a tiny surface element, $dA$, on the sphere. In spherical coordinates:

$$dA = r^2 \sin \theta \, d\theta \, d\phi$$

The overall area is obtained by integrating all these tiny surface elements for the entire domain, $\theta \in [0, 2\pi]$ and $\phi \in [0, \pi]$, and by setting the radius to a fixed value:

$$A = \int_{0}^{2\pi}\int_{0}^{\pi}r^2 \sin \theta \, d\theta \, d\phi$$

## Gauss Quadrature with Legendre Polynomials

There is no chance I will do the math by hand. Rather, let's take advantage of a very smart box called computer and implement Gauss quadrature. In a nutshell, the above integral can be approximated as a weighted sum of each surface element at each specific point within the domain. These "specific" points, and associated weights, arise from the choice of underlying polynomials that define our domain. Here, we use Legendre polynomials.

```python
import numpy as np

# define `theta` and `phi`, and set `r` to 1
theta = (0., pi)
phi = (0., 2 * pi)
r = 1.

# extract and scale roots and weights for quadrature using Legendre polynomials
deg = 20
roots, weights = np.polynomial.legendre.leggauss(deg)
theta_roots = 0.5 * (roots + 1.) * (theta[1] - theta[0]) + theta[0]
theta_weights = 0.5 * weights * (theta[1] - theta[0])
phi_roots = 0.5 * (roots + 1.) * (phi[1] - phi[0]) + phi[0]
phi_weights = 0.5 * weights * (phi[1] - phi[0])
theta_grid, phi_grid = np.meshgrid(theta_roots, phi_roots)

# quadrature
A_quad = phi_weights @ np.sin(theta_grid) * r ** 2 @ theta_weights
print(f'A = {A_quad:.6f}')
```

```
A = 12.566371
```

We are accurate to at least the 6th decimal, which should be satisfactory for most small-scale applications.

## Convex Hull for Random Point Clouds

The main issue with the quadrature approach is that we have to use predefined set of sample points and weights. In real-world applications and simulations, points are unordered, random, sometimes even noisy. For irregular point clouds, we should first reconstruct the surface, and only then can we estimate the total surface area.

A common way to approach this, assuming that the surface is convex, is by triangulating the surface using the convex hull or envelope. The convex hull is the smallest convex region containing the point set.

Let's randomly generate a point cloud representing the sphere with radius 1. We use the elegant Marsaglia method that consists of picking two values from independent uniform distributions, $a$ and $b$, and rejecting points that do not satisfy:

$$a^2 + b^2 \leq r$$

```python
import scipy.spatial as ss

def marsaglia(n_points, r=1.):
    """Return a randomly generated point cloud representing a sphere.
    Refs: Marsaglia, G., Ann. Math. Stat. 43:645-646, 1972
    """
    assert r > 0, 'radius must be a positive number'
    a = np.random.uniform(-r, r, size=n_points)
    b = np.random.uniform(-r, r, size=n_points)

    mask = np.where(a ** 2 + b ** 2 < 1)
    a = a[mask]
    b = b[mask]

    x = 2 * a * np.sqrt(1 - a ** 2 - b ** 2)
    y = 2 * b * np.sqrt(1 - a ** 2 - b ** 2)
    z = 1 - 2 * (a ** 2 + b ** 2)
    return np.stack((x, y, z), axis=-1)

# generate random point cloud
xyz = marsaglia(deg ** 2, r)

# create convex hull and extract the surface area
hull = ss.ConvexHull(xyz)
A_hull = hull.area
print(f'A = {A_hull:.6f}')
```

```
A = 12.342118
```

Results are not as good as with the Gaussian-Legendre quadrature approach, but this is expected since a convex hull is nothing but a bunch of small **planar** polygons that reconstruct a sphere, and the sphere is inherently **non-planar**.

This problem can be somewhat circumvented if we generate a larger number of surface points. With 20,000 points:

```python
xyz = marsaglia(20000, r)
hull2 = ss.ConvexHull(xyz)
A_hull2 = hull2.area
print(f'A = {A_hull2:.6f}')
```

```
A = 12.561579
```

Very nice.

## Surface Integral with JAX Autodiff

All this so far is simple and elegant, but I want something that is a complete opposite of that. I will now demonstrate how to compute the area of a sphere in an overly complicated way just because I want to be a cool kid who uses new fancy libraries for sport.

Here, we use JAX and its automatic differentiation capabilities to extract the gradients of vectors normal to the sphere in order to compute the following integral:

$$A = \int_x \int_y \sqrt{\Big(\frac{\partial z}{\partial x}\Big)^2 + \Big(\frac{\partial z}{\partial y}\Big)^2 + 1} \, dx \, dy$$

We first set $z$ to be a function of the other two coordinates:

$$z = z(x, y) = \pm \sqrt{r - x^2 - y^2}$$

This parametrization yields the definition of the position vector $\vec{r}$:

$$\vec{r} = \vec{r}(x, y) = x \vec{i} + y \vec{j} + z(x, y) \vec{k}$$

The magnitude of the cross product of the partial derivatives of $\vec{r}(x, y)$ yields the vector surface element, $\vec{dA}$:

$$\vec{dA} = \Big|\frac{\partial \vec{r}(x, y)}{\partial x} \times \frac{\partial \vec{r}(x, y)}{\partial y}\Big|$$

Following the definition of the position vector, the partial derivatives with respect to $x$ and $y$ are:

$$\frac{\partial \vec{r}}{\partial x} = \vec{i} + \frac{\partial z(x,y)}{\partial x} \vec{k}$$

$$\frac{\partial \vec{r}}{\partial y} = \vec{j} + \frac{\partial z(x,y)}{\partial y} \vec{k}$$

This gives us:

$$|\vec{dA}| = \sqrt{\Big(\frac{\partial z}{\partial x}\Big)^2 + \Big(\frac{\partial z}{\partial y}\Big)^2 + 1}$$

If we can compute gradients of the normal vector at each point on our parameterized surface, we can compute the overall surface area:

```python
from jax import (jit, grad, vmap)
import jax.numpy as jnp

# explicit sphere parametrization via z=z(x, y)
z_fn = lambda x, y, r: jnp.sqrt(r ** 2 - x ** 2 - y ** 2)

# derivatives of z(x,y) with respect to x and y
grad_z_fn = grad(z_fn, argnums=(0, 1))

# vectorized implementation of the above function
grad_z_fn_vmap = vmap(grad_z_fn, in_axes=(0, 0, None))

# define the domain using polar coordinates...
u = (0, 1)
v = (0, np.pi)

roots, _ = np.polynomial.chebyshev.chebgauss(deg)
u_roots = 0.5 * (roots + 1.) * (u[1] - u[0]) + u[0]
v_roots = 0.5 * (roots + 1.) * (v[1] - v[0]) + v[0]

U, V = np.meshgrid(u_roots, v_roots)
X = U * np.sin(V)
Y = U * np.cos(V)
Z = z_fn(X, Y, r)

# compute the normal vector length in each point of interest
dzdx, dzdy = grad_z_fn_vmap(X.ravel(), Y.ravel(), r)
n_abs = np.sqrt(dzdx ** 2 + dzdy ** 2 + 1)

# integrate and scale the integral according to the definition of the domain
A_n = 4 * np.sum(n_abs[deg:] * (np.diff(X, axis=0).ravel()
                                * np.diff(Y, axis=1).ravel()))
print(f'A = {A_n:.6f}')
```

```
A = 12.403081
```

The result is not as accurate as the other methods, but the point was to demonstrate that JAX's automatic differentiation can be used to compute geometric properties through gradient computation — even if it's overkill for this particular problem.
