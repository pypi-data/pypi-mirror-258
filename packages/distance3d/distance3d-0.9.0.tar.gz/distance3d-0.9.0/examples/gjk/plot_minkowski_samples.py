"""
======================================
Plot Samples from Minkowski Difference
======================================
"""
print(__doc__)
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
import pytransform3d.transformations as pt
from distance3d import colliders, minkowski, random, gjk, plotting


n_direction_samples = 50
random_state = np.random.RandomState(42)
capsule12origin, radius1, height1 = random.rand_capsule(random_state)
capsule22origin, radius2, height2 = random.rand_capsule(random_state)
capsule1 = colliders.Capsule(capsule12origin, radius1, height1)
capsule2 = colliders.Capsule(capsule22origin, radius2, height2)

vertices1 = np.empty((n_direction_samples, 3))
vertices2 = np.empty((n_direction_samples, 3))
for i in range(n_direction_samples):
    direction = random.randn_direction(random_state)
    vertices1[i] = capsule1.support_function(direction)
    vertices2[i] = capsule2.support_function(direction)
minkowski_difference = minkowski.minkowski_sum(vertices1, -vertices2)

_, cp1, cp2, simplex = gjk.gjk_distance(capsule1, capsule2)

ax = ppu.make_3d_axis(
    np.max(np.abs(np.linalg.norm(minkowski_difference, axis=1))), pos=121)
pt.plot_transform(ax, np.eye(4), s=3)
ax.scatter(minkowski_difference[:, 0], minkowski_difference[:, 1],
           minkowski_difference[:, 2], c="k", alpha=0.2, s=1)
plotting.plot_tetrahedron(ax, simplex)

ax = ppu.make_3d_axis(2.0, pos=122)
ppu.plot_capsule(ax, A2B=capsule12origin, height=height1, radius=radius1,
                 wireframe=False, color="r", alpha=0.1)
ppu.plot_capsule(ax, A2B=capsule22origin, height=height2, radius=radius2,
                 wireframe=False, color="b", alpha=0.1)
ax.scatter(cp1[0], cp1[1], cp1[2], c="k", s=5)
ax.scatter(cp2[0], cp2[1], cp2[2], c="k", s=5)

plt.show()
