from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
   ld = LaunchDescription()

   package_name = 'ros_basics'
   rviz_config_path = os.path.join(
      get_package_share_directory(package_name),
      'rviz',
      'leo_rover.rviz'
   )

   # Robot node
   robot_node = Node(
      package=package_name,
      executable='move_robot_node',
      name='robot_node',
      output='screen',
      emulate_tty=True
   )

   # RViz2 node
   rviz_node = Node(
      package='rviz2',
      executable='rviz2',
      name='rviz_node',
      arguments=['-d', rviz_config_path]
   )

   # Add actions to launch description
   ld.add_action(robot_node)
   ld.add_action(rviz_node)

   return ld
