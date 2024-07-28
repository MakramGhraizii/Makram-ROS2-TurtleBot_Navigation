# Makram-ROS2-TurtleBot_Navigation
## Overview

This project involves the development of a navigation system for a TurtleBot 3 robot using ROS 2. The system includes several nodes for robot control, wall following, lap timing, and visualization. The project demonstrates the integration of various ROS 2 functionalities to achieve a complete navigation solution.

## Project Structure

The project consists of the following main components:

- **Robot Driver Node**: This node handles the basic movement and control of the TurtleBot 3.
- **Wall Finder Service Node**: This node implements a service that helps the robot detect and follow walls.
- **Lap Time Action Server Node**: This node implements an action server that times the robot's laps.
- **Lap Time Action Client Node**: This node interacts with the lap time action server to measure the time taken for each lap.
- **Visualize Node**: This node visualizes the robot's path and the distance to the nearest wall using real-time plotting.

## Nodes Description

### Robot Driver Node

- **Purpose**: Controls the movement of the TurtleBot 3.
- **Functionality**: Publishes velocity commands to the `/cmd_vel` topic to drive the robot forward, backward, or turn.
- **Topics**:
  - `/cmd_vel` (Publisher): Sends velocity commands to the robot.

### Wall Finder Service Node

- **Purpose**: Detects and follows walls.
- **Functionality**: Implements a service that checks the distance to walls using LIDAR data and adjusts the robot's path to follow the wall.
- **Services**:
  - `/find_wall` (Service): Provides the wall following functionality.
- **Topics**:
  - `/scan` (Subscriber): Receives LIDAR scan data.

### Lap Time Action Server Node

- **Purpose**: Measures the time taken for the robot to complete a lap.
- **Functionality**: Implements an action server that starts a timer when the robot begins a lap and stops it when the lap is completed.
- **Actions**:
  - `/lap_time` (Action Server): Manages lap timing operations.
- **Topics**:
  - `/odom` (Subscriber): Receives odometry data to track the robot's position.

### Lap Time Action Client Node

- **Purpose**: Interacts with the lap time action server to measure lap times.
- **Functionality**: Sends goals to the lap time action server and receives feedback and results.
- **Actions**:
  - `/lap_time` (Action Client): Sends goals to and receives results from the lap time action server.

### Visualize Node

- **Purpose**: Visualizes the robot's path and distance to walls.
- **Functionality**: Subscribes to odometry and LIDAR topics and uses matplotlib to plot the robot's path and the distance to the nearest wall.
- **Topics**:
  - `/odom` (Subscriber): Receives odometry data to plot the robot's path.
  - `/scan` (Subscriber): Receives LIDAR data to plot the distance to walls.

## Installation
```sh
cd ~/ros2_ws/src
git clone <repository_url>
cd ~/ros2_ws
colcon build
source install/setup.bash
```
## Launch the Package
```sh
ros2 launch warehouse_robot launch.py item_name:=item1 quantity:=40

```
or to run each node separately:
```sh
ros2 run turtlebot_navigation robot_driver_node
ros2 run turtlebot_navigation wall_finder_service_node
ros2 run turtlebot_navigation lap_time_action_server_node
ros2 run turtlebot_navigation lap_time_action_client_node
ros2 run turtlebot_navigation visualize_node
```
