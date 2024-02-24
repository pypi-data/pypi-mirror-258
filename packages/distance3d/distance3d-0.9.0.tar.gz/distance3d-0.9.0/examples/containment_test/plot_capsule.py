"""
===================
Capsule Containment
===================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
from distance3d import containment_test


random_state = np.random.RandomState(0)
capsule2origin = np.eye(4)
radius = 0.5
height = 1.0

ax = ppu.make_3d_axis(ax_s=3)
points = random_state.rand(100000, 3)
points[:, 0] -= 0.5
points[:, 0] *= 2.0
points[:, 2] -= 0.5
points[:, 2] *= 2.0
start = time.time()
contained = containment_test.points_in_capsule(points, capsule2origin, radius, height)
stop = time.time()
print(f"{stop - start} s")
ax.scatter(points[::10, 0], points[::10, 1], points[::10, 2], c=contained[::10])
ppu.plot_capsule(ax=ax, A2B=capsule2origin, radius=radius, height=height, wireframe=True, color="r")
ppu.plot_capsule(ax=ax, A2B=capsule2origin, radius=radius, height=height, wireframe=False, alpha=0.5)
plt.show()
