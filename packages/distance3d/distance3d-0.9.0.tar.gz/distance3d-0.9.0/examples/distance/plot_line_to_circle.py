"""
================================
Distance between line and circle
================================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
from distance3d.distance import line_to_circle
from distance3d import random, plotting


random_state = np.random.RandomState(0)
center = np.zeros(3)
radius = 1
normal = np.array([0.0, 0.0, 1.0])

ax = ppu.make_3d_axis(ax_s=2)

accumulated_time = 0.0
for i in range(5000):
    line_point, line_direction = random.randn_line(random_state)
    start = time.time()
    dist, closest_point_line, closest_point_circle = line_to_circle(
        line_point, line_direction, center, radius, normal)
    end = time.time()
    accumulated_time += end - start
    print(dist)
    if i > 10:
        continue
    plotting.plot_segment(ax, closest_point_line, closest_point_circle,
                          c="k", lw=1)
    plotting.plot_line(ax, line_point, line_direction)
print(f"{accumulated_time=}")

plotting.plot_circle(ax, center, radius, normal, surface_alpha=0)
plt.show()
