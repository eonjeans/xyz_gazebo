import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from pathlib import Path
from launch_ros.actions import Node
import xacro  # 🔥 Xacro 직접 변환 추가

def generate_launch_description():
    package_name = 'my_robot_description'
    
    urdf_file = os.path.join(get_package_share_directory(package_name), 'urdf', 'robot.urdf.xacro')
    
    robot_description_config = xacro.process_file(urdf_file, mappings={'use_ros2_control': 'true'})
    robot_description = robot_description_config.toxml()
    
    # Declare launch arguments
    world_name = DeclareLaunchArgument(
        "world_name", 
        # default_value="model.sdf"
        default_value="RealMap.model"
    )


    
    # Set Gazebo model path
    gz_resource_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH', 
        value=[
            EnvironmentVariable('GAZEBO_MODEL_PATH', default_value=''),
            '/usr/share/gazebo-11/models/:',
            str(Path(get_package_share_directory('my_robot_description')).parent.resolve()),
            ':',
            str(Path(get_package_share_directory('my_robot_description')).parent.resolve()) + "/my_robot_description/models"
        ])
    
    # Load URDF file
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'upload.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': PathJoinSubstitution([FindPackageShare('my_robot_description'), 'worlds', LaunchConfiguration('world_name')])}.items()
    )

    # Spawn entity in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_bot'],
        output='screen'
    )
    
    # Robot State Publisher (for TF & Rviz)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}] 
    )

    # Rviz configuration
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare(package_name), 'rviz', 'my_robot.rviz'
    ])
    
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    # Launch all processes
    return LaunchDescription([
        world_name,
        gz_resource_path,
        rsp,
        gazebo,
        spawn_entity,
        robot_state_publisher, 
        rviz,
    ])
