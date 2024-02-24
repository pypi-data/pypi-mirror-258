"""
==================================
Distance from line to line segment
==================================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
from distance3d.distance import line_to_line_segment
from distance3d import random, plotting


random_state = np.random.RandomState(0)
segment_start, segment_end = random.randn_line_segment(random_state)

ax = ppu.make_3d_axis(ax_s=3)

accumulated_time = 0.0
for i in range(45000):
    line_point, line_direction = random.randn_line(random_state)
    start = time.time()
    dist, closest_point_line, closest_point_segment = line_to_line_segment(
        line_point, line_direction, segment_start, segment_end)
    end = time.time()
    accumulated_time += end - start
    print(dist)
    if i > 5:
        continue
    plotting.plot_segment(
        ax, closest_point_line, closest_point_segment, c="k", lw=1)
    plotting.plot_line(ax, line_point, line_direction)
print(f"{accumulated_time=}")

plotting.plot_segment(ax, segment_start, segment_end)
plt.show()
