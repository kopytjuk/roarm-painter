from dataclasses import dataclass

import modern_robotics as mr
import numpy as np


@dataclass
class RobotKinematics:
    end_effector_zero_config: np.ndarray  # end effector zero config
    screw_axes_matrix: np.ndarray  # column i is a screw axis of joint i

    def end_effector_pose_from_joints(self, theta_list: np.ndarray) -> np.ndarray:
        theta_list = np.array(theta_list)
        return mr.FKinSpace(
            self.end_effector_zero_config, self.screw_axes_matrix, theta_list
        )
