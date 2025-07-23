import json
import time
from typing import Any, Dict

import click
import pandas as pd
import requests


class Robot:
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
            "t": 1.57,
            "r": 0,
            "g": 3.14,
            "spd": speed,
        }
        self._send_command(command)

    def move_to_home(self) -> None:
        """Move robot to home position."""
        command = {"T": 100}
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


@click.command()
@click.argument("ip_address")
@click.argument("strokes_file", type=click.Path(exists=True))
@click.option("--speed", "-s", default=0.25, help="Movement speed (default: 0.25)")
@click.option(
    "--z-offset", "-z", default=-60, help="Z-axis offset in mm (default: -60)"
)
def paint_strokes(ip_address, strokes_file, speed, z_offset):
    """Execute painting movements from a CSV file containing stroke coordinates."""
    df = pd.read_csv(strokes_file)

    required_columns = {"stroke_id", "x", "y", "z"}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns in CSV: {', '.join(missing)}")

    robot = Robot(ip_address)

    # Initialize robot
    robot.move_to_home()
    time.sleep(1)
    print("Robot in initial position!")

    try:
        for _, stroke_group in df.groupby("stroke_id"):
            coords = stroke_group[["x", "y", "z"]].values

            for x, y, z in coords:
                robot.move_to(x, y, z_offset + z, speed)
                print(f"Moving to x={x:.2f}, y={y:.2f}, z={z:.2f}")
                time.sleep(0.005)

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
    finally:
        robot.move_to_home()
        print("Movement complete!")


if __name__ == "__main__":
    paint_strokes()
