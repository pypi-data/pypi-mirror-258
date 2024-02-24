"""
====================================
Visualize Intersection of Tetrahedra
====================================
"""
print(__doc__)

import numpy as np
import pytransform3d.visualizer as pv
from distance3d import hydroelastic_contact, visualization

sphere1 = hydroelastic_contact.RigidBody.make_sphere(np.array([0.1, 0.2, 0.1]), 1.0, order=2)
sphere1.express_in(np.eye(4))
sphere2 = hydroelastic_contact.RigidBody.make_sphere(np.array([0.05, 0.15, 1.6]), 1.0, order=2)
sphere2.express_in(np.eye(4))

tetrahedron1 = sphere1.tetrahedra_points[257]
tetrahedron2 = sphere2.tetrahedra_points[310]

epsilon1 = np.array([0.0, 0.0, 0.0, 1.0])
epsilon2 = np.array([0.0, 0.0, 0.0, 1.0])

X1 = hydroelastic_contact.barycentric_transforms(tetrahedron1[np.newaxis])[0]
X2 = hydroelastic_contact.barycentric_transforms(tetrahedron2[np.newaxis])[0]
intersection, contact = hydroelastic_contact.intersect_tetrahedron_pair(
    tetrahedron1, epsilon1, X1, tetrahedron2, epsilon2, X2)
assert intersection
contact_plane_hnf, contact_polygon = contact

intersection_com, force_vector, _, _ = hydroelastic_contact.compute_contact_force(
    tetrahedron1, epsilon1, contact_plane_hnf, contact_polygon)

fig = pv.figure()
fig.scatter(tetrahedron1, s=0.01, c=(1, 0, 0))
fig.scatter(tetrahedron2, s=0.01, c=(0, 0, 1))
fig.plot_transform(np.eye(4), s=0.05)
fig.plot_plane(normal=contact_plane_hnf[:3], d=contact_plane_hnf[3])
fig.scatter(contact_polygon, s=0.03, c=(1, 0, 1))
fig.plot_vector(intersection_com, 100.0 * force_vector, c=(1, 0, 0))
visualization.Tetrahedron(tetrahedron1).add_artist(fig)
visualization.Tetrahedron(tetrahedron2).add_artist(fig)
fig.view_init()

if "__file__" in globals():
    fig.show()
else:
    fig.save_image("__open3d_rendered_image.jpg")
