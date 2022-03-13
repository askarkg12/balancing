import rclpy
from rclpy.node import Node

import sensor_msgs


class MPU6050ComplemetaryFilter(Node):
    def __init__(self):
        super().__init__("mpu6050_complementary_filter")
        self.publisher_ = self.create_publisher(
            msg.String, "/imu/data_complementary", 10
        )
        self.subscription = self.create_subscription(
            sensor_msgs.msg.Imu, "/imu/data_raw", self.listener_callback, 10
        )
        self.subscription

    def listener_callback(self, msg):
        pass


def main():
    print("Hi from mpy_6050_tools.")


if __name__ == "__main__":
    main()
