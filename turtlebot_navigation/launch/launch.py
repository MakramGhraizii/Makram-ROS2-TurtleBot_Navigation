from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlebot_navigation',
            executable='robot_driver_node',
            name='robot_driver'
        ),
        Node(
            package='turtlebot_navigation',
            executable='wall_finder_service_node',
            name='wall_finder_service'
        ),
        Node(
            package='turtlebot_navigation',
            executable='lap_time_action_server_node',
            name='lap_time_action_server'
        ),
        Node(
            package='turtlebot_navigation',
            executable='lap_time_action_client_node',
            name='lap_time_action_client'
        ),
        Node(
            package='turtlebot_navigation',
            executable='visualize_node',
            name='visualize_node'
        ),
    ])
