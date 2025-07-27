import numpy as np

from robot_painter.kinematics import RobotKinematics

# Dimensions

# all values are in mm
L1 = 44.0
L2A = 240.0
L2B = 30.0
L3 = 144.0
L4A = 55.0
L4B = 10.0
L5 = 123.0  # end effector length

# convert to m
L1 /= 1000
L2A /= 1000
L2B /= 1000
L3 /= 1000
L4A /= 1000
L4B /= 1000
L5 /= 1000


# End-Effector Zero Configuration
M = np.eye(4, dtype=float)

# End effector position
x_e = L2B + L3 + L4A + L5
y_e = 0.0
z_e = L1 + L2A - L4B

M[:3, 3] = [x_e, y_e, z_e]

# Screw Axes

# ### S1 - base
S1 = np.r_[0, 0, 1, 0, 0, 0]

# ### S2 - shoulder
omega_2 = np.r_[0, 1, 0]
q_2 = np.r_[0, 0, L1]  # point on screw axis
v_2 = np.cross(-omega_2, q_2)

S2 = np.r_[omega_2, v_2]


# ### S3 - elbow
omega_3 = np.r_[0, 1, 0]
q_3 = np.r_[L2B, 0, L1 + L2A]  # point on screw axis
v_3 = np.cross(-omega_3, q_3)

S3 = np.r_[omega_3, v_3]

# ### S4 - wrist 1
omega_4 = np.r_[0, 1, 0]
q_4 = np.r_[L2B + L3, 0, L1 + L2A]  # point on screw axis
v_4 = np.cross(-omega_4, q_4)

S4 = np.r_[omega_4, v_4]

# ### S5 - wrist 2
omega_5 = np.r_[1, 0, 0]
q_5 = np.r_[L2B + L3 + L4A, 0, L1 + L2A - L4B]  # point on screw axis
v_5 = np.cross(-omega_5, q_5)
S5 = np.r_[omega_5, v_5]


# ### All screw axes as a single matrix

S = np.c_[S1, S2, S3, S4, S5]


RoArmM3Kinematics = RobotKinematics(M, S)
