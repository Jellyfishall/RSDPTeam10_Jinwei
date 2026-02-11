from functools import partial

import rclpy
from geometry_msgs.msg import PointStamped, PoseArray
from rclpy.node import Node

from rover_interface.msg import BlockBinColor, BlockPoseObservation, BlockShape

# TODO: add publish function for observations
# TODO: add subs for each block type
# TODO: also need to see where the rover is relative to the blocks to compute the true orientation. Question - what frame are BlockPoseObservations made in?


class VisionStub(Node):
    def __init__(self):
        super().__init__("vision_stub")
        self.sub_red_block = self.create_subscription(
            msg_type=PoseArray,
            topic="/model/block_red_1/pose",
            callback=partial(self.obs_callback, color=BlockBinColor.RED),
            qos_profile=1,
        )

        self.publisher = self.create_publisher(
            BlockPoseObservation,
            topic="observations",
            qos_profile=1,
        )

    def obs_callback(self, msg: PoseArray, color: int):
        """Converts a pose message from gazebo into a
        rover_interface-compatible message"""
        obs = BlockPoseObservation()
        obs.position.header.stamp = msg.header.stamp
        obs.position.header.frame_id = msg.header.frame_id

        obs.position.point.x = msg.poses[0].position.x  # type: ignore
        obs.position.point.y = msg.poses[0].position.y  # type: ignore
        obs.position.point.z = msg.poses[0].position.z  # type: ignore

        obs.shape.shape = BlockShape.CUBE
        obs.color.color = color

        self.publisher.publish(obs)
        return None


def main():
    try:
        rclpy.init()
        node = VisionStub()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
# Pose topics
# /model/bin_blue_1/pose
# /model/bin_red_1/pose
# /model/bin_yellow_1/pose
# /model/block_blue_1/pose
# /model/block_red_1/pose
# /model/block_yellow_1/pose
# /model/platform_blue/pose
# /model/platform_red/pose
# /model/platform_yellow/pose
