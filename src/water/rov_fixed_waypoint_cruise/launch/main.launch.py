from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="rov_fixed_waypoint_cruise",
            executable="waypoint_node",
            name="waypoint_cruise",
            output="screen"
        ),
        Node(
            package="rov_fixed_waypoint_cruise",
            executable="viz_node",
            name="waypoint_viz",
            output="screen"
        )
    ])
