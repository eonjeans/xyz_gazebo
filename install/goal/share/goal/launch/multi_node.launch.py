from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='goal',
            executable='pose_estimator',
            name='pose_estimator_node'
        ),
        Node(
            package='goal',
            executable='goal_navigator',
            name='goal_navigator_node'
        ),
        Node(
            package='goal',
            executable='user_input',
            name='user_input_node'
        )
    ])
