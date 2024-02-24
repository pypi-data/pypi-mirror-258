"""
===============================
Distance from plane to triangle
===============================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
from distance3d.distance import plane_to_triangle
from distance3d import random, plotting


random_state = np.random.RandomState(3)
plane_point, plane_normal = random.randn_plane(random_state)

ax = ppu.make_3d_axis(ax_s=2)

accumulated_time = 0.0
for i in range(40000):
    triangle_points = random.randn_triangle(random_state)
    start = time.time()
    dist, closest_point_plane, closest_point_triangle = plane_to_triangle(
        plane_point, plane_normal, triangle_points)
    end = time.time()
    accumulated_time += end - start
    print(dist)
    if i > 5:
        continue
    plotting.plot_segment(
        ax, closest_point_plane, closest_point_triangle, c="k", lw=1)
    plotting.plot_triangle(ax, triangle_points)
print(f"{accumulated_time=}")

plotting.plot_plane(
    ax=ax, plane_point=plane_point, plane_normal=plane_normal, s=2)
ax.view_init(azim=150, elev=30)
plt.show()
