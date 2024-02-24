"""Broad-phase collision detection."""
import warnings

import numpy as np
from pytransform3d import urdf

from .aabb_tree import AabbTree
from .colliders import Sphere, Box, Cylinder, MeshGraph
from .urdf_utils import self_collision_whitelists
from .io import load_mesh


class BoundingVolumeHierarchy:
    """Bounding volume hierarchy (BVH) for broad phase collision detection.

    Wraps multiple colliders that are connected through transformations.
    In addition, these colliders are stored in an AABB tree for broad phase
    collision detection.

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
        tm.add_transform(base_frame, "origin", base_frame2origin)
        self.tm = tm
        self.base_frame = base_frame
        self.base_frame2origin = base_frame2origin
        self.collider_frames = set()
        self.aabbtree_ = AabbTree()
        self.colliders_ = {}
        self.self_collision_whitelists_ = {}

    def fill_tree_with_colliders(
            self, tm, make_artists=False,
            fill_self_collision_whitelists=False, use_visuals=False):
        """Fill tree with colliders from URDF transform manager.

        Parameters
        ----------
        tm : pytransform3d.urdf.UrdfTransformManager
            Transform manager that has colliders.

        make_artists : bool, optional (default: False)
            Create artist for visualization for each collision object.

        fill_self_collision_whitelists : bool, optional (default: False)
            Fill whitelists for self collision detection. All collision
            objects connected to the current link, child, and parent links
            will be ignored.

        use_visuals : bool, optional (default: False)
            Use visual objects as colliders.
        """
        if use_visuals:
            objects = tm.visuals
        else:
            objects = tm.collision_objects

        for obj in objects:
            try:
                collider = self._make_collider(tm, obj, make_artists)
                self.add_collider(obj.frame, collider)
            except RuntimeError as e:
                warnings.warn(str(e))

        if fill_self_collision_whitelists:
            self.self_collision_whitelists_.update(
                self_collision_whitelists(tm))

        self.update_collider_poses()

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
            collider = Sphere(center=A2B[:3, 3], radius=obj.radius)
        elif isinstance(obj, urdf.Box):
            collider = Box(A2B, obj.size)
        elif isinstance(obj, urdf.Cylinder):
            collider = Cylinder(
                cylinder2origin=A2B, radius=obj.radius,
                length=obj.length)
        else:
            assert isinstance(obj, urdf.Mesh)
            vertices, triangles = load_mesh(obj.filename, obj.scale)
            collider = MeshGraph(A2B, vertices, triangles)
        if make_artists:
            collider.make_artist()
        return collider

    def add_collider(self, frame, collider):
        """Add collider.

        Parameters
        ----------
        frame : Hashable
            Frame in which the collider is located.

        collider : ConvexCollider
            Collider.
        """
        self.collider_frames.add(frame)
        self.colliders_[frame] = collider
        self.aabbtree_.insert_aabb(collider.aabb(), (frame, collider))

    def update_collider_poses(self):
        """Update poses of all colliders from transform manager."""
        self.aabbtree_ = AabbTree()
        for frame in self.colliders_:
            A2B = self.tm.get_transform(frame, "origin")
            collider = self.colliders_[frame]
            collider.update_pose(A2B)
            self.aabbtree_.insert_aabb(collider.aabb(), (frame, collider))

    def get_colliders(self):
        """Get all colliders.

        Returns
        -------
        colliders : list
            List of colliders.
        """
        return self.colliders_.values()

    def get_artists(self):
        """Get all artists.

        Returns
        -------
        artists : list
            List of artists.
        """
        return [collider.artist_ for collider in self.colliders_.values()
                if collider.artist_ is not None]

    def aabb_overlapping_colliders(self, collider, whitelist=()):
        """Get colliders with an overlapping AABB.

        This function performs broad phase collision detection with a bounding
        volume hierarchy, where the bounding volumes are axis-aligned bounding
        boxes.

        Parameters
        ----------
        collider : ConvexCollider
            Collider.

        whitelist : sequence
            Names of frames to which collisions are allowed.

        Returns
        -------
        colliders : dict
            Maps frame names to colliders with overlapping AABB.
        """
        aabb = collider.aabb()
        _, overlaps = self.aabbtree_.overlaps_aabb(aabb)
        colliders = dict(np.array(self.aabbtree_.external_data_list,
                                  dtype=object)[overlaps.astype(int)])
        for frame in whitelist:
            colliders.pop(frame, None)
        return colliders

    def aabb_overlapping_with_other_bvh(self, other_bvh):
        """Get colliders with an overlapping AABB.

        This function performs broad phase collision detection with a bounding
        volume hierarchy, where the bounding volumes are axis-aligned bounding
        boxes.

        Parameters
        ----------
        other_bvh : BoundingVolumeHierarchy
            the other BVH.

        Returns
        -------
        data_pairs : array, shape(n, 2)
            A list of colliding colliders.
        """
        _, _, _, pairs = self.aabbtree_.overlaps_aabb_tree(other_bvh.aabbtree_)

        data_pairs = []
        for pair in pairs:
            data_pair = (self.aabbtree_.external_data_list[pair[0]],
                         other_bvh.aabbtree_.external_data_list[pair[1]])
            data_pairs.append(data_pair)

        return data_pairs

    def aabb_overlapping_with_self(self):
        """Get colliders with overlapping with itself.

        This function performs broad phase collision detection with a bounding
        volume hierarchy, where the bounding volumes are axis-aligned bounding
        boxes.

        Returns
        -------
        data_pairs : array, shape(n, 2)
            A list of colliding colliders.
        """
        _, _, _, pairs = self.aabbtree_.overlaps_aabb_tree(self.aabbtree_)

        data_pairs = []
        for pair in pairs:
            if pair[0] == pair[1]:
                continue

            data_pair = (self.aabbtree_.external_data_list[pair[0]],
                         self.aabbtree_.external_data_list[pair[1]])
            data_pairs.append(data_pair)

        return data_pairs

    def get_collider_frames(self):
        """Get collider frames.

        Returns
        -------
        collider_frames : set
            Collider frames.
        """
        return self.collider_frames
