"""
==============================
Distance from line to triangle
==============================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
from distance3d.distance import line_to_triangle
from distance3d import random, plotting


random_state = np.random.RandomState(8)
triangle_points = random.randn_triangle(random_state)

ax = ppu.make_3d_axis(ax_s=5)

accumulated_time = 0.0
for i in range(7500):
    line_point, line_direction = random.randn_line(random_state, scale=3.0)
    start = time.time()
    dist, closest_point_line, closest_point_triangle = line_to_triangle(
        line_point, line_direction, triangle_points)
    end = time.time()
    accumulated_time += end - start
    print(dist)
    if i > 3:
        continue
    plotting.plot_segment(
        ax, closest_point_line, closest_point_triangle, c="k", lw=1)
    plotting.plot_line(ax, line_point, line_direction)
print(f"{accumulated_time=}")

plotting.plot_triangle(ax, triangle_points)
plt.show()
