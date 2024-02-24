"""
=======================================
Distance from line segment to rectangle
=======================================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
from distance3d.distance import line_segment_to_rectangle
from distance3d import random, plotting


random_state = np.random.RandomState(6)
rectangle_center, rectangle_axes, rectangle_lengths = random.randn_rectangle(
    random_state, center_scale=0.3, length_scale=2.0)

ax = ppu.make_3d_axis(ax_s=2)

accumulated_time = 0.0
for i in range(5500):
    segment_start, segment_end = random.randn_line_segment(random_state)
    start = time.time()
    dist, closest_point_segment, closest_point_rectangle = line_segment_to_rectangle(
        segment_start, segment_end, rectangle_center, rectangle_axes, rectangle_lengths)
    end = time.time()
    accumulated_time += end - start
    print(dist)
    if i > 10:
        continue
    plotting.plot_segment(
        ax, closest_point_segment, closest_point_rectangle, c="k", lw=1)
    plotting.plot_segment(ax, segment_start, segment_end)
print(f"{accumulated_time=}")

plotting.plot_rectangle(ax, rectangle_center, rectangle_axes, rectangle_lengths)
plt.show()
