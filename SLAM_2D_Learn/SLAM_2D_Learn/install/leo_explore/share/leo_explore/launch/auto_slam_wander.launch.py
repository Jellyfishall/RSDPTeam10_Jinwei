#!/usr/bin/python3
import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('rplidar_ros'),
                'launch',
                'rplidar_a2m12_launch.py'
            )
        ),
        launch_arguments={
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': '256000',
            'frame_id': 'laser',
            'inverted': 'false',
            'angle_compensate': 'true',
            'scan_mode': 'Sensitivity',
        }.items()
    )

    cartographer_calc_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('lslidar_catorgrapher'),
                'launch',
                'catorgrapher_calc.py'
            )
        )
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('lslidar_catorgrapher'),
                'launch',
                'catorgrapher_rviz.py'
            )
        )
    )

    wander_node = Node(
        package='leo_explore',
        executable='wander',
        name='leo_wander',
        output='screen',
        parameters=[
            {
                'scan_topic': '/scan',
                'cmd_vel_topic': '/cmd_vel',
                'forward_speed': 0.12,
                'turn_speed': 0.80,
                'safe_dist': 0.60,
                'robot_stop_timeout': 0.50,
            }
        ]
    )

    return LaunchDescription([
        rplidar_launch,
        TimerAction(period=2.0, actions=[cartographer_calc_launch]),
        TimerAction(period=4.0, actions=[rviz_launch]),
        TimerAction(period=8.0, actions=[wander_node]),
    ])
