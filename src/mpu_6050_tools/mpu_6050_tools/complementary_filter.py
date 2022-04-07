"""Read raw data from MPU6050 and publish complementary filter data."""
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu


class MPU6050ComplementaryFilter(Node):
    """TODO."""

    def __init__(self):
        """TODO."""
        super().__init__("mpu6050_complementary_filter")
        self.subscription = self.create_subscription(
            Imu, "/imu/data_raw", self.listener_callback, 10
        )
        self.subscription
        self.angleX = 0

    def listener_callback(self, msg):
        """TODO."""
        print("Got a msg")


def main(args=None):
    """TODO."""
    rclpy.init(args=args)
    comp_filter = MPU6050ComplementaryFilter()
    rclpy.spin(comp_filter)

    comp_filter.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
