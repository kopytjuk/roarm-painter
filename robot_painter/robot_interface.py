import json
import math
from typing import Any, Dict

import requests


class RobotInterface:
    """
    Robot class for controlling a painting robot via HTTP commands.

        ip_address (str): IP address of the robot.

    Methods:
        move_to(x, y, z, speed): Move robot to specified coordinates.
        home(): Move robot to home position.
        get_state(): Retrieve current state of the robot.
    """

    def __init__(self, ip_address: str):
        self._ip_address = ip_address
        self._session = requests.Session()

    def move_to(self, x: float, y: float, z: float, speed: float | None = 0.25) -> None:
        """Move robot to specified coordinates."""
        command = {
            "T": 104 if speed is not None else 1041,
            "x": float(x),
            "y": float(y),
            "z": float(z),
            "t": 0.0,  # 1.57,
            "r": 0,
            "g": 3.14,
            "spd": speed,
        }
        self._send_command(command)

    def move_to_home(self) -> None:
        """Move robot to home position."""
        command = {"T": 100}
        self._send_command(command)

    def control_joints(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        gripper: float = 3.15,
    ):
        command = {
            "T": 102,
            "base": j1,
            "shoulder": j2,
            "elbow": j3 + math.pi / 2,
            "wrist": j4,
            "roll": j5,
            "hand": gripper,
            "spd": 0.1,
            "acc": 10,
        }
        self._send_command(command)

    def get_state(self) -> None:
        command = {"T": 105}
        response = self._send_command(command)
        return response

    def _send_command(self, command: Dict[str, Any]) -> str:
        """Send a command to the robot."""
        url = f"http://{self._ip_address}/js?json={json.dumps(command)}"
        response = self._session.get(url)
        return response.text
