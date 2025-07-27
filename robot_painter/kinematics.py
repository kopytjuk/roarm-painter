from dataclasses import dataclass

import modern_robotics as mr
import numpy as np

from robot_painter.utils import normalize_angles


@dataclass
class RobotKinematics:
    end_effector_zero_config: np.ndarray  # end effector zero config
    screw_axes_matrix: np.ndarray  # column i is a screw axis of joint i

    @property
    def num_joints(self) -> int:
        return self.screw_axes_matrix.shape[1]

    def forward_kinematics(self, theta_list: np.ndarray) -> np.ndarray:
        theta_list = np.array(theta_list)
        return mr.FKinSpace(
            self.end_effector_zero_config, self.screw_axes_matrix, theta_list
        )

    def inverse_kinematics(
        self, end_effector_pose: np.ndarray, theta_0: np.ndarray | None = None
    ) -> np.ndarray:
        # initial guess
        if theta_0 is None:
            theta_0 = np.zeros(self.num_joints)

        theta_result, success = mr.IKinSpace(
            self.screw_axes_matrix,
            self.end_effector_zero_config,
            end_effector_pose,
            theta_0,
            eomg=0.01,
            ev=0.001,
        )

        theta_result = normalize_angles(theta_result)

        return theta_result
