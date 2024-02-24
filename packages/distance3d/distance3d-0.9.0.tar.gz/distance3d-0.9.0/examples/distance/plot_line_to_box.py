"""
=========================
Distance from line to box
=========================
"""
print(__doc__)
import time
import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.transformations as pt
import pytransform3d.plot_utils as ppu
from distance3d.distance import line_to_box
from distance3d import random, plotting


random_state = np.random.RandomState(2)
box2origin = np.eye(4)
size = np.ones(3)

ax = ppu.make_3d_axis(ax_s=2)

accumulated_time = 0.0
for i in range(18000):
    line_point, line_direction = random.randn_line(random_state)
    if random_state.rand() < 0.33:
        line_direction[random_state.randint(3)] = 0.0
    if random_state.rand() < 0.33:
        line_direction[random_state.randint(3)] = 0.0
    if random_state.rand() < 0.33:
        line_direction[random_state.randint(3)] = 0.0
    start = time.time()
    dist, closest_point_line, closest_point_box = line_to_box(
        line_point, line_direction, box2origin, size)
    end = time.time()
    accumulated_time += end - start
    print(dist)
    if i > 10:
        continue
    plotting.plot_segment(
        ax, closest_point_line, closest_point_box, c="k", lw=1)
    plotting.plot_line(ax, line_point, line_direction)
print(f"{accumulated_time=}")

ppu.plot_box(ax=ax, A2B=box2origin, size=size, wireframe=False, alpha=0.5)
pt.plot_transform(ax=ax, A2B=box2origin, s=0.1)
plt.show()
