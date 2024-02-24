"""
==================================
Distance between capsules with GJK
==================================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
import pytransform3d.transformations as pt
from distance3d import gjk, colliders
from distance3d import random
from distance3d import plotting


random_state = np.random.RandomState(0)
capsule2origin, radius, height = random.rand_capsule(random_state, 0.2, 0.4, 1.0)

ax = ppu.make_3d_axis(ax_s=2)

accumulated_time = 0.0
for i in range(700):
    capsule2origin2, radius2, height2 = random.rand_capsule(random_state, 1.0, 0.3, 1.0)
    start = time.time()
    c1 = colliders.Capsule(capsule2origin, radius, height)
    c2 = colliders.Capsule(capsule2origin2, radius2, height2)
    dist, closest_point_capsule, closest_point_capsule2, _ = gjk.gjk(c1, c2)
    end = time.time()
    accumulated_time += end - start
    print(dist)
    if i > 5:
        continue
    plotting.plot_segment(
        ax, closest_point_capsule, closest_point_capsule2, c="k", lw=1)
    pt.plot_transform(ax=ax, A2B=capsule2origin2, s=0.1)
    ppu.plot_capsule(
        ax=ax, A2B=capsule2origin2, radius=radius2, height=height2,
        wireframe=False, alpha=0.5)
print(f"{accumulated_time=}")

pt.plot_transform(ax=ax, A2B=capsule2origin, s=0.1)
ppu.plot_capsule(
    ax=ax, A2B=capsule2origin, radius=radius, height=height, wireframe=False,
    alpha=0.5, color="yellow")
plt.show()
