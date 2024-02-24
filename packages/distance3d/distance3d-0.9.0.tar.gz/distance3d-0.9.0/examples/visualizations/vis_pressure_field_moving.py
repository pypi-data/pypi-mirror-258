"""
==========================================
Visualize Pressure Fields of Moving Object
==========================================
"""
print(__doc__)

import numpy as np
import pytransform3d.visualizer as pv
from distance3d import visualization, hydroelastic_contact


class AnimationCallback:
    def __init__(self,
             n_frames, rigid_body1, rigid_body2, rigid_body3, rigid_body4,
             position_offset):
        self.n_frames = n_frames

        self.rigid_body1 = rigid_body1
        self.rigid_body2 = rigid_body2
        self.rigid_body3 = rigid_body3
        self.rigid_body4 = rigid_body4

        self.position_offset = position_offset

        self.rigid_body2.express_in(self.rigid_body1.body2origin_)
        self.rigid_body3.express_in(self.rigid_body1.body2origin_)
        self.rigid_body4.express_in(self.rigid_body1.body2origin_)

        self.mesh1 = visualization.RigidBodyTetrahedralMesh(
            self.rigid_body1.body2origin_, self.rigid_body1.vertices_,
            self.rigid_body1.tetrahedra_)
        self.mesh2 = visualization.RigidBodyTetrahedralMesh(
            self.rigid_body2.body2origin_, self.rigid_body2.vertices_,
            self.rigid_body2.tetrahedra_)
        self.mesh3 = visualization.RigidBodyTetrahedralMesh(
            self.rigid_body3.body2origin_, self.rigid_body3.vertices_,
            self.rigid_body3.tetrahedra_)
        self.mesh4 = visualization.RigidBodyTetrahedralMesh(
            self.rigid_body4.body2origin_, self.rigid_body4.vertices_,
            self.rigid_body4.tetrahedra_)

        contact_surface21 = hydroelastic_contact.find_contact_surface(
            self.rigid_body2, self.rigid_body1)
        self.contact_surface21 = visualization.ContactSurface(
            contact_surface21.frame2world,
            contact_surface21.contact_polygons,
            contact_surface21.contact_polygon_triangles,
            contact_surface21.pressures)

        contact_surface31 = hydroelastic_contact.find_contact_surface(
            self.rigid_body3, self.rigid_body1)
        self.contact_surface31 = visualization.ContactSurface(
            contact_surface31.frame2world,
            contact_surface31.contact_polygons,
            contact_surface31.contact_polygon_triangles,
            contact_surface31.pressures)

        contact_surface41 = hydroelastic_contact.find_contact_surface(
            self.rigid_body4, self.rigid_body1)
        self.contact_surface41 = visualization.ContactSurface(
            contact_surface41.frame2world,
            contact_surface41.contact_polygons,
            contact_surface41.contact_polygon_triangles,
            contact_surface41.pressures)

    def add_artists(self, fig):
        self.mesh1.add_artist(fig)
        self.mesh2.add_artist(fig)
        self.mesh3.add_artist(fig)
        self.mesh4.add_artist(fig)
        self.contact_surface21.add_artist(fig)
        self.contact_surface31.add_artist(fig)
        self.contact_surface41.add_artist(fig)

    def __call__(self, step):
        # Transform back to original frame
        rb12origin = np.eye(4)
        t1 = np.sin(2 * np.pi * step / self.n_frames) / 2.0 + 1.0
        rb12origin[:3, 3] = t1 * self.position_offset
        self.rigid_body1.express_in(rb12origin)

        # Move to new pose
        t2 = np.sin(2 * np.pi * (step + 1) / self.n_frames) / 2.0 + 1.0
        rb12origin[:3, 3] = t2 * self.position_offset
        self.rigid_body1.body2origin_ = rb12origin

        self.mesh1.set_data(
            self.rigid_body1.body2origin_, self.rigid_body1.vertices_,
            self.rigid_body1.tetrahedra_)

        contact_surface21 = hydroelastic_contact.find_contact_surface(
            self.rigid_body2, self.rigid_body1)
        self.contact_surface21.set_data(
            contact_surface21.frame2world,
            contact_surface21.contact_polygons,
            contact_surface21.contact_polygon_triangles,
            contact_surface21.pressures)

        contact_surface31 = hydroelastic_contact.find_contact_surface(
            self.rigid_body3, self.rigid_body1)
        self.contact_surface31.set_data(
            contact_surface31.frame2world,
            contact_surface31.contact_polygons,
            contact_surface31.contact_polygon_triangles,
            contact_surface31.pressures)

        contact_surface41 = hydroelastic_contact.find_contact_surface(
            self.rigid_body4, self.rigid_body1)
        self.contact_surface41.set_data(
            contact_surface41.frame2world,
            contact_surface41.contact_polygons,
            contact_surface41.contact_polygon_triangles,
            contact_surface41.pressures)

        return (
            self.mesh1, self.contact_surface21, self.contact_surface31,
            self.contact_surface41)


box2origin = np.eye(4)
rigid_body1 = hydroelastic_contact.RigidBody.make_box(box2origin, np.array([0.2, 0.1, 0.1]))

capsule2origin = np.eye(4)
capsule2origin[:3, 3] = np.array([0.0, 0.13, 0.05])
rigid_body2 = hydroelastic_contact.RigidBody.make_capsule(capsule2origin, 0.1, 0.1, 0.05)

cylinder2origin = np.eye(4)
cylinder2origin[:3, 3] = np.array([-0.3, 0.0, 0.0])
rigid_body3 = hydroelastic_contact.RigidBody.make_cylinder(cylinder2origin, 0.1, 0.4, 0.05)

ellipsoid2origin = np.eye(4)
ellipsoid2origin[:3, 3] = np.array([0.3, 0.0, 0.0])
rigid_body4 = hydroelastic_contact.RigidBody.make_ellipsoid(ellipsoid2origin, np.array([0.05, 0.1, 0.2]), 2)

fig = pv.figure()
fig.plot_transform(np.eye(4), s=0.1)

n_frames = 100
animation_callback = AnimationCallback(
    n_frames, rigid_body1, rigid_body2, rigid_body3, rigid_body4,
    np.array([0.4, 0.0, 0.0]))
animation_callback.add_artists(fig)
fig.view_init()
if "__file__" in globals():
    fig.animate(animation_callback, n_frames, loop=True, fargs=())
    fig.show()
else:
    fig.save_image("__open3d_rendered_image.jpg")
