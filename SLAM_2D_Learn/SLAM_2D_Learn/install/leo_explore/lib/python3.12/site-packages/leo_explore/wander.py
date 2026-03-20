#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class Wander(Node):

    def __init__(self):
        super().__init__('leo_wander')

        self.declare_parameter('scan_topic', '/scan')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('forward_speed', 0.12)
        self.declare_parameter('turn_speed', 0.80)
        self.declare_parameter('safe_dist', 0.60)
        self.declare_parameter('robot_stop_timeout', 0.50)
        self.declare_parameter('angular_sign', -1.0)

        self.scan_topic = self.get_parameter('scan_topic').value
        self.cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        self.forward_speed = float(self.get_parameter('forward_speed').value)
        self.turn_speed = float(self.get_parameter('turn_speed').value)
        self.safe_dist = float(self.get_parameter('safe_dist').value)
        self.robot_stop_timeout = float(self.get_parameter('robot_stop_timeout').value)
        self.angular_sign = float(self.get_parameter('angular_sign').value)

        self.cmd_pub = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.scan_sub = self.create_subscription(
            LaserScan,
            self.scan_topic,
            self.scan_callback,
            10
        )

        self.front = float('inf')
        self.front_left = float('inf')
        self.front_right = float('inf')
        self.left = float('inf')
        self.right = float('inf')
        self.scan_ready = False
        self.last_scan_time = self.get_clock().now()

        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info(f'Autonomous wander started, angular_sign={self.angular_sign}')

    def _angle_to_index(self, angle, angle_min, angle_increment, length):
        idx = int((angle - angle_min) / angle_increment)
        return max(0, min(idx, length - 1))

    def _sector_min(self, ranges, angle_min, angle_increment, deg_start, deg_end):
        if not ranges:
            return 10.0

        start = math.radians(deg_start)
        end = math.radians(deg_end)
        i0 = self._angle_to_index(start, angle_min, angle_increment, len(ranges))
        i1 = self._angle_to_index(end, angle_min, angle_increment, len(ranges))
        if i0 > i1:
            i0, i1 = i1, i0

        valid = []
        for i in range(i0, i1 + 1):
            r = ranges[i]
            if math.isfinite(r) and r > 0.02:
                valid.append(r)

        if not valid:
            return 10.0
        return min(valid)

    def scan_callback(self, msg: LaserScan):
        ranges = list(msg.ranges)
        self.front = self._sector_min(ranges, msg.angle_min, msg.angle_increment, -15, 15)
        self.front_left = self._sector_min(ranges, msg.angle_min, msg.angle_increment, 15, 60)
        self.front_right = self._sector_min(ranges, msg.angle_min, msg.angle_increment, -60, -15)
        self.left = self._sector_min(ranges, msg.angle_min, msg.angle_increment, 60, 100)
        self.right = self._sector_min(ranges, msg.angle_min, msg.angle_increment, -100, -60)
        self.scan_ready = True
        self.last_scan_time = self.get_clock().now()

    def stop_robot(self):
        cmd = Twist()
        self.cmd_pub.publish(cmd)

    def control_loop(self):
        cmd = Twist()

        if not self.scan_ready:
            self.stop_robot()
            return

        dt = (self.get_clock().now() - self.last_scan_time).nanoseconds / 1e9
        if dt > self.robot_stop_timeout:
            self.get_logger().warn('Laser scan timeout, stop robot.')
            self.stop_robot()
            return

        blocked_front = self.front < self.safe_dist
        blocked_left = self.front_left < self.safe_dist * 0.95
        blocked_right = self.front_right < self.safe_dist * 0.95

        if blocked_front or (blocked_left and blocked_right):
            cmd.linear.x = 0.0
            if self.left > self.right:
                cmd.angular.z = self.angular_sign * self.turn_speed
            else:
                cmd.angular.z = self.angular_sign * (-self.turn_speed)

        elif blocked_left:
            cmd.linear.x = 0.05
            cmd.angular.z = self.angular_sign * (-0.5 * self.turn_speed)

        elif blocked_right:
            cmd.linear.x = 0.05
            cmd.angular.z = self.angular_sign * (0.5 * self.turn_speed)

        else:
            cmd.linear.x = self.forward_speed
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = Wander()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop = Twist()
        node.cmd_pub.publish(stop)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
