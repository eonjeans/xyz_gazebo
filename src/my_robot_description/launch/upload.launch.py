import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
import xacro  # 🔥 직접 xacro 변환을 위해 추가

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    use_ros2_control = LaunchConfiguration('use_ros2_control', default='True')
    
    # 🔥 Xacro 파일 경로 설정
    robot_description_path = os.path.join(
        get_package_share_directory('my_robot_description'),
        'urdf',
        'robot.urdf.xacro'
    )
    
    # 🔥 Xacro 파일을 직접 변환하여 robot_description 설정
    robot_description_config = xacro.process_file(robot_description_path, mappings={'use_ros2_control': 'true'})
    robot_description = robot_description_config.toxml()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value='true', description='Use simulation time if true'
        ),
        DeclareLaunchArgument(
            'use_ros2_control', default_value='false', description='Enable ROS 2 Control'
        ),
        
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {'robot_description': robot_description},  # 🔥 직접 변환된 robot_description 설정
                {'use_sim_time': use_sim_time},
                {'use_ros2_control': use_ros2_control}
            ]
        )
    ])
