# Robot painter

A python CLI for drawing with the RoArm M3 Pro robot arm.

It accepts a files with strokes (i.e. sets of points which shall be connected 
with a pencil) and sends the control commands to the web-server running on
the ESP32 controller of the robot arm.

## Setup

Just run `uv sync`, make sure the robot is accessible via its IP and run the 
`python robot_painter.py 192.168.0.123 strokes.csv`. Enjoy!
 