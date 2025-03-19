import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from pathlib import Path
from launch_ros.actions import Node
import xacro  # Xacro 직접 변환 추가


def generate_launch_description():
    # ===========================
    # 기본 세팅 (내 로봇)
    # ===========================
    package_name = 'my_robot_description'
    
    # Xacro 파일을 읽고 robot_description 생성
    urdf_file = os.path.join(get_package_share_directory(package_name), 'urdf', 'robot.urdf.xacro')
    
    robot_description_config = xacro.process_file(urdf_file, mappings={'use_ros2_control': 'true'})
    robot_description = robot_description_config.toxml()
    
    # ===========================
    # 런치 인자 선언
    # ===========================
    world_name = DeclareLaunchArgument(
        "world_name", 
        default_value="realMap.world"
    )

    # 장애물 위치 인자 선언
    declare_x_pos_arg = DeclareLaunchArgument('x_pos', default_value='-4.0')
    declare_y_pos_arg = DeclareLaunchArgument('y_pos', default_value='-10.0')
    declare_z_pos_arg = DeclareLaunchArgument('z_pos', default_value='0.0')
    declare_yaw_arg   = DeclareLaunchArgument('yaw', default_value='1.57')

    # ===========================
    # Gazebo 모델 경로 추가
    # ===========================
    gz_resource_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH', 
        value=[
            EnvironmentVariable('GAZEBO_MODEL_PATH', default_value=''),
            '/usr/share/gazebo-11/models/:',
            str(Path(get_package_share_directory(package_name)).parent.resolve()),
            ':',
            str(Path(get_package_share_directory(package_name)).parent.resolve()) + f"/{package_name}/models"
        ])

    # ===========================
    # Gazebo 플러그인 경로 추가 (옵션)
    # ===========================
    gz_plugin_path = SetEnvironmentVariable(
        name='GAZEBO_PLUGIN_PATH',
        value=[
            EnvironmentVariable('GAZEBO_PLUGIN_PATH', default_value=''),
            str(Path(get_package_share_directory(package_name)).parent.resolve()) + f'/install/{package_name}/lib'
        ]
    )

    # ===========================
    # robot_description 파라미터를 로드하는 launch 파일 포함 (robot_state_publisher 실행 포함)
    # ===========================
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'upload.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # ===========================
    # Gazebo 실행
    # ===========================
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={
            'world': PathJoinSubstitution([
                FindPackageShare(package_name),
                'worlds',
                LaunchConfiguration('world_name')
            ])
        }.items()
    )

    # ===========================
    # 내 로봇 스폰 (gazebo 실행 후 5초 지연하여 실행)
    # ===========================
    spawn_entity = TimerAction(
        period=5.0,  # 초 단위 지연
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=['-topic', 'robot_description', '-entity', 'my_bot'],
                output='screen'
            )
        ]
    )

    # ===========================
    # RViz 실행
    # ===========================
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

    # ===========================
    # animated_box 장애물 관련 (내 로봇 URDF 재사용)
    # ===========================

    # 장애물용 robot_state_publisher 실행
    rsp_animated_box_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='animated_box_robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    # 장애물 스폰 엔티티 (gazebo 실행 후 6초 지연하여 실행)
    spawn_animated_box_node = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=[
                    '-entity', 'animated_box',               # 엔티티 이름 (중복 방지)
                    '-topic', 'robot_description',
                    '-x', LaunchConfiguration('x_pos'),
                    '-y', LaunchConfiguration('y_pos'),
                    '-z', LaunchConfiguration('z_pos'),
                    '-Y', LaunchConfiguration('yaw')
                ],
                output='screen'
            )
        ]
    )

    # ===========================
    # LaunchDescription에 모두 추가!
    # ===========================
    return LaunchDescription([
        # 기본 런치 인자
        world_name,
        declare_x_pos_arg,
        declare_y_pos_arg,
        declare_z_pos_arg,
        declare_yaw_arg,

        # 환경변수 설정
        gz_resource_path,
        gz_plugin_path,

        # 노드 실행 순서
        rsp,
        gazebo,
        spawn_entity,
        rviz,

        # 장애물 노드 실행
        rsp_animated_box_node,
        spawn_animated_box_node
    ])
