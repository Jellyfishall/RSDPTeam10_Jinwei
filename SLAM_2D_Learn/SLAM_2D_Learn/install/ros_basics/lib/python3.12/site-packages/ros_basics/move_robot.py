import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class BasicROS(Node):
   def __init__(self):
      super().__init__('move_robot_node')
      self.counter = 0
      self.counter_period = 5
      self.switch_direction = False
      self.vel_step = 0.1
      self.twist_cmd = Twist()
      self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
      self.timer_period = 1.0
      self.timer = self.create_timer(self.timer_period, self.timer_callback)

   def timer_callback(self):
      if self.counter % self.counter_period == 0:
         self.switch_direction = True
      else:
         self.switch_direction = False
      self.move_robot()
      self.counter += 1

   def move_robot(self):
      self.vel_step = -self.vel_step if self.switch_direction else self.vel_step
      self.twist_cmd.linear.x = self.vel_step
      self.twist_cmd.angular.z = 0.0
      self.cmd_vel_pub.publish(self.twist_cmd)

def main(args=None):
   rclpy.init(args=args)
   basic_ros_node = BasicROS()
   try:
      rclpy.spin(basic_ros_node)
   except KeyboardInterrupt:
      pass
   finally:
      basic_ros_node.destroy_node()
      rclpy.shutdown()

if __name__ == '__main__':
   main()