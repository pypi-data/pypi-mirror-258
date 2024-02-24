from distance3d.broad_phase import BoundingVolumeHierarchy
from pytransform3d import urdf
from distance3d.hydroelastic_contact import RigidBody
import numpy as np


class HydroelasticBoundingVolumeHierarchy(BoundingVolumeHierarchy):
    """Hydroelastic BVH for broad phase collision detection.

    This BVH works the same but uses the hydroelastic RigidBody as the
    collider object.

    Parameters
    ----------
    tm : pytransform3d.transform_manager.TransformManager
        Transform manager that stores the transformations.

    base_frame : str
        Name of the base frame in which colliders are represented.

    base_frame2origin : array, shape (4, 4), optional (default: np.eye(4))
        The position of the base_frame to origin.

    Attributes
    ----------
    aabbtree_ : AabbTree
        Tree of axis-aligned bounding boxes.

    colliders_ : dict
        Maps frames of collision objects to colliders.

    self_collision_whitelists_ : dict
        Whitelists for self-collision detection in case this BVH represents
        a robot.
    """

    def __init__(self, tm, base_frame, base_frame2origin=np.eye(4)):
        super().__init__(tm, base_frame, base_frame2origin)

    def _make_collider(self, tm, obj, make_artists):
        """Creates a collider from a URDF object.

        Parameters
        ----------
        tm : pytransform3d.urdf.UrdfTransformManager
            Transform manager that has colliders.

        obj: pytransform3d.urdf.Geometry
            The urdf object.

        make_artists : bool, optional (default: False)
            Create artist for visualization for each collision object.

        Returns
        -------
        collider : ConvexCollider
            The corresponding collider.
        """
        A2B = tm.get_transform(obj.frame, "origin")

        if isinstance(obj, urdf.Sphere):
            collider = RigidBody.make_sphere(A2B[:3, 3], obj.radius, 2)
        elif isinstance(obj, urdf.Box):
            collider = RigidBody.make_box(A2B, obj.size)
        elif isinstance(obj, urdf.Cylinder):
            collider = RigidBody.make_cylinder(
                A2B, obj.radius, obj.length, resolution_hint=0.01)
        else:  # pragma: no cover
            assert isinstance(obj, urdf.Mesh)
            raise NotImplementedError(
                "Arbitrary mesh conversion is not implemented!")

        if make_artists:
            collider.make_artist()
        return collider

    # Override to change the docstring.
    def aabb_overlapping_colliders(self, collider, whitelist=()):
        """Get colliders with an overlapping AABB.

        This function performs broad phase collision detection with a bounding
        volume hierarchy, where the bounding volumes are axis-aligned bounding
        boxes.

        Parameters
        ----------
        collider : RigidBody
            RigidBody.

        whitelist : sequence
            Names of frames to which collisions are allowed.

        Returns
        -------
        colliders : dict
            Maps frame names to colliders with overlapping AABB.
        """
        return super().aabb_overlapping_colliders(collider, whitelist)
