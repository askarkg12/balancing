"""Read raw data from MPU6050 and publish complementary filter data."""
import math

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
        self.accel_angle_z = 0
        self.gyro_angle_x = 0

    def listener_callback(self, msg):
        """TODO."""
        self.accel_angle_x = math.atan(
            msg.linear_acceleration.y
            / math.sqrt(msg.linear_acceleration.z**2 + msg.linear_acceleration.x**2)
        )
        self.accel_angle_y = math.atan(
            -1
            * msg.linear_acceleration.x
            / math.sqrt(msg.linear_acceleration.y**2 + msg.linear_acceleration.z**2)
        )
        self.gyro_angle_x = self.gyro_angle_x + msg.angular_velocity.x * 2


def main(args=None):
    """TODO."""
    rclpy.init(args=args)
    comp_filter = MPU6050ComplementaryFilter()
    rclpy.spin(comp_filter)

    comp_filter.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
