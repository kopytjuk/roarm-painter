import math

import numpy as np

from robot_painter.definitions import RoArmM3Kinematics


def test_forward_kinematics_simple():
    rk = RoArmM3Kinematics

    theta_list = np.zeros(5)
    M = rk.end_effector_zero_config

    T_ee = rk.forward_kinematics(theta_list)

    np.testing.assert_almost_equal(T_ee, M)


def test_forward_kinematics_arm_straight():
    rk = RoArmM3Kinematics

    theta_list = np.zeros(5)
    theta_list[1] = math.pi / 2
    theta_list[2] = -math.pi / 2

    # Rotation should be the same
    M = rk.end_effector_zero_config
    R0 = M[:3, :3]

    T_ee = rk.forward_kinematics(theta_list)
    R_ee = T_ee[:3, :3]

    np.testing.assert_almost_equal(R_ee, R0)

    # x position shall be higher than from zero config
    assert T_ee[0, 3] > M[0, 3]
