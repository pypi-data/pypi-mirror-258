"""
===============================
Distance between two rectangles
===============================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.plot_utils as ppu
from distance3d.distance import rectangle_to_rectangle
from distance3d import random, plotting


random_state = np.random.RandomState(0)
rectangle_center, rectangle_axes, rectangle_lengths = random.randn_rectangle(
    random_state, center_scale=1.0, length_scale=5.0)

ax = ppu.make_3d_axis(ax_s=3)

accumulated_time = 0.0
for i in range(500):
    rectangle_center2, rectangle_axes2, rectangle_lengths2 = random.randn_rectangle(
        random_state, center_scale=1.0, length_scale=5.0)
    start = time.time()
    dist, closest_point_rectangle, closest_point_rectangle2 = rectangle_to_rectangle(
        rectangle_center, rectangle_axes, rectangle_lengths,
        rectangle_center2, rectangle_axes2, rectangle_lengths2)
    end = time.time()
    accumulated_time += end - start
    print(dist)
    if i > 7:
        continue
    plotting.plot_segment(
        ax, closest_point_rectangle, closest_point_rectangle2, c="k", lw=1)
    plotting.plot_rectangle(ax, rectangle_center2, rectangle_axes2, rectangle_lengths2, show_axes=False)
print(f"{accumulated_time=}")

plotting.plot_rectangle(ax, rectangle_center, rectangle_axes, rectangle_lengths)
plt.show()
