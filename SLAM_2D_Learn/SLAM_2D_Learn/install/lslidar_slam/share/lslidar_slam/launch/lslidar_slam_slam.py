from launch import LaunchDescription  
from ament_index_python.packages import get_package_share_directory 
from launch_ros.actions import Node, LifecycleNode  
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription  
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution  
from launch.launch_description_sources import PythonLaunchDescriptionSource  
import os
def generate_launch_description():
    
    slam_config = os.path.join(get_package_share_directory("lslidar_slam"), "config", "slam_config.yaml")

    async_slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory("slam_toolbox"), "/launch", "/online_async_launch.py"]),
        launch_arguments={
            "use_sim_time": "false", 
            "slam_params_file": slam_config,
            "use_lifecycle_manager": "true"
        }.items()      
    )

    return LaunchDescription([
        async_slam_toolbox
    ])
