"""Utility functions for basic (unit) dual quaternion usage."""
from __future__ import annotations

import dual_quaternions
import numpy as np
from dqrobotics import DQ, log, rotation, translation, vec3, vec4, vec6, vec8
from spatialmath import (
    DualQuaternion,
    Quaternion,
    UnitQuaternion,
)


def dq_to_pose(unit_dq: DQ) -> tuple[np.ndarray, UnitQuaternion]:
    """Generate a classic pose from a unit dual quaternion.

    :param unit_dq: pose represented as dual quaternion.
    :type unit_dq: DQ
    :return: translation (3d vector), orientation (quaternion)
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    _translation = vec3(translation(unit_dq))
    _orientation = UnitQuaternion(vec4(rotation(unit_dq)))
    return _translation, _orientation


def pose_to_dq(pose: tuple[np.ndarray, UnitQuaternion]) -> DQ:
    """Generate classic pose from unit dual quaternion.

    :param pose: Pose consisting of translation and a quaternion.
    :type pose: tuple[np.ndarray, Quaternion]
    :return: pose represented as unit dual quaternion.
    :rtype: DQ
    """
    primal = pose[1]
    dual = 0.5 * (Quaternion.Pure(pose[0]) * primal)

    # se3 = SE3(pose[0]) * pose[1].SE3()
    return DQ(DualQuaternion(real=primal, dual=dual).vec)


def dq_sclerp(current_pose: DQ, goal_pose: DQ, alpha: float) -> DQ:
    r"""Perform scLERP (dual quaternion interpolation from one pose to another).

    :param current_pose: Current pose.
    :type current_pose: DQ
    :param goal_pose: Goal pose.
    :type goal_pose: DQ
    :param alpha: Interpolation parameter where :math:`\alpha \in \left[0, 1\right]`.
    :type alpha: float
    :raises ValueError: If :math:`\alpha \not\in \left[0, 1\right]`.
    :return: Unit dual quaternion which represents the pose.
    :rtype: DQ
    """
    if not (0 <= alpha <= 1):
        msg = "alpha must lie between 0 and 1."
        raise ValueError(msg)

    delta_dq = current_pose.inv() * goal_pose

    delta_dq_vec8 = vec8(delta_dq)
    pow_delta = DQ(
        dual_quaternions.DualQuaternion.from_dq_array(delta_dq_vec8)
        .pow(alpha)
        .dq_array()
    )
    return current_pose * pow_delta


def dq_twist(current_dq: DQ, goal_dq: DQ, alpha: float) -> np.ndarray:
    r"""Generate 6d twist using sclerp.

    :param current_dq: Current pose represented as unit dual quaternion.
    :type current_dq: DQ
    :param goal_dq: Goal pose represented as unit dual quaternion.
    :type goal_dq: DQ
    :param alpha: Exponential s.t. :math:`\alpha \in \left[0, 1\right].`
    :type alpha: float
    :return: 6d twist :math:`\mathcal{V} \in \mathbb{R}^6`.
    :rtype: np.ndarray
    """
    next_point = dq_sclerp(current_dq, goal_dq, alpha)
    return vec6(log(next_point * current_dq.conj()))


def dq_pose_error(dq_current: DQ, dq_desired: DQ) -> DQ:
    """Comput unit dual quaternion pose error

    :param dq_current: Current pose expressed as unit dual quaternion.
    :type dq_current: DQ
    :param dq_desired: Desired pose expressed as unit dual quaternion.
    :type dq_desired: DQ
    :return: Error pose expressed as unit dual quaternion.
    :rtype: DQ
    """
    dq_identity = np.zeros((8,))
    dq_identity[0] = 1.0
    return DQ(dq_identity) - (dq_current.conj() * dq_desired)


def generate_intermediate_waypoints(
    start_pose: DQ, goal_pose: DQ, n_points: int
) -> list[DQ]:
    """Generate intermediate waypoints using unit dual quaternions.

    :param start_pose: Start pose represented as unit dual quaternion.
    :type start_pose: DQ
    :param goal_pose: Goal pose represented as unit dual quaternion.
    :type goal_pose: DQ
    :param n_points: Number of points to generate in total (including start- and goal pose).
    :type n_points: int
    :return: Generated intermediate waypoints.
    :rtype: list[DQ]
    """
    steps = np.linspace(0, 1, n_points)[1:-1]
    return (
        [start_pose]
        + [dq_sclerp(start_pose, goal_pose, step) for step in steps]
        + [goal_pose]
    )


def interpolate_waypoints(
    waypoints: list[tuple[np.ndarray, UnitQuaternion]],
    n_points: int,
    adaptive: bool = False,
) -> list[tuple[np.ndarray, UnitQuaternion]]:
    r"""Insert n_points between intermediate waypoints.

    :param waypoints: List of poses.
    :type waypoints: list[tuple[np.ndarray, np.ndarray, float]]
    :param n_points: points to be inserted between two intermediate poses.
    :type n_points: int
    :param adaptive: Set number of waypoint depending on dual quaternion error.
        Between two points then :math:`\lfloor e \left(n_p + 2\right)\rfloor - 2` are inserted,
        where :math:`e_{clipped} \in \left[0, 1\right]` represents the clipped norm of the dual quaternion error s.t. :math:`e_{clipped} = \min\left(e, 1\right), e \ge 0`.
        Defaults to False
    :type adaptive: bool, optional
    :return: New waypoints.
    :rtype: list[tuple[np.ndarray, np.ndarray, float]]
    """
    out = []
    for i in range(len(waypoints) - 1):
        left = pose_to_dq(waypoints[i])
        right = pose_to_dq(waypoints[i + 1])
        error = np.linalg.norm(vec8(dq_pose_error(left, right))) if adaptive else 1.0
        error = np.clip(error, 0.0, 1.0)
        points2add = [
            dq_to_pose(pose)
            for pose in generate_intermediate_waypoints(
                left, right, int(float(n_points + 2) * error)
            )[:-1]
        ]
        out += points2add

    return [*out, waypoints[-1]]
