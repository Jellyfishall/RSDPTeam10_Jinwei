import numpy as np
import rclpy
from geometry_msgs.msg import Point, PointStamped
from rclpy.node import Node
from rover_interface.msg import (
    BlockBinColor,
    BlockPoseObservation,
    BlockPoseSmoothed,
    BlockPoseSmoothedArray,
    BlockShape,
)


class AggregateObservations(Node):
    """This node subscribes to observations from the Computer Vision node
    and aggregates them to form a persistent array of distinct block positions."""

    def __init__(self):
        super().__init__("aggregate_observations")

        self.block_dist_threshold_m = self.declare_parameter(
            "block_dist_threshold_m", 0.1
        )

        self.sub = self.create_subscription(
            BlockPoseObservation,
            topic="/cv/block_poses",
            callback=self.observe_block,
            qos_profile=1,
        )

        self.pub = self.create_publisher(
            msg_type=BlockPoseSmoothedArray,
            topic="controller/block_poses",
            qos_profile=1,
        )
        self.pub_period_seconds = 0.1
        self.timer = self.create_timer(
            timer_period_sec=self.pub_period_seconds,
            callback=self.publish_smoothed_array,
        )

        self.block_poses: np.ndarray | None = None
        self.block_colors: list[BlockBinColor] = []

    def compare_blocks(self, pos: np.ndarray) -> tuple[int, bool]:
        # TODO: get the distances to each block. If none are lower than
        # the threshold, then it's a new block
        dists = np.linalg.norm(pos - self.block_poses, axis=-1)
        if dists.min() < self.block_dist_threshold_m:
            return dists.argmax(), False
        return len(dists), True  # it's a new object, return a new longest idx

    def publish_smoothed_array(self, poses: np.ndarray):
        msg = BlockPoseSmoothedArray()
        for i in range(len(poses)):
            block = BlockPoseSmoothed()
            block.id = i

            # Add block position info
            pose = poses[i]
            block.position = PointStamped()
            # TODO: convert to map as slam frame comes in
            block.position.header.frame_id = "odom"
            block.position.header.stamp = self.get_clock().now().to_msg()
            block.position.point = Point(x=pose[0], y=pose[1], z=pose[2])
            block.shape = BlockShape()
            block.shape.shape = BlockShape.CUBE

            # Add block features
            block.color = BlockBinColor()
            block.color.color = BlockBinColor.RED
            block.state = BlockPoseSmoothed.NOT_COLLECTED

            msg.blocks.append(block)  # type:ignore

        self.pub.publish(msg=msg)

    @staticmethod
    def update_pose_estimate(
        current_estimate: np.ndarray,
        new_estimate: np.ndarray,
    ):  # type: ignore
        # Just using EMA for the time being as a super basic approach
        # can upgrade to smarter averaging or a Kalman or something if needed
        # TODO: implement more complex smoothing approach if needed
        return 0.05 * current_estimate + 0.95 * new_estimate

    def observe_block(self, msg: BlockPoseObservation):
        "Smooth block pose, add to existing array"
        pos = np.zeros((1, 3))
        pos[0] = msg.position.point.x
        pos[1] = msg.position.point.y
        pos[2] = msg.position.point.z

        # if this is the first block detected, start the array
        if self.block_poses is None:
            self.block_poses = pos
            self.block_colors.append(msg.color)
            return

        # Otherwise, compare it to the existing positions to estimate whether
        # it's an observation of an existing block or a new one
        idx, is_distinct = self.compare_blocks(pos)
        if is_distinct:
            self.block_poses = np.vstack([self.block_poses, pos])
            self.block_colors.append(msg.color)
        else:
            self.block_poses[idx] = self.update_pose_estimate(
                self.block_poses[idx], pos
            )


def main():
    try:
        rclpy.init()
        node = AggregateObservations()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
