"""Read raw data from MPU6050 and publish complementary filter data."""
import math

import quaternion

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
        self.publisher_ = self.create_publisher(Imu, "/imu/data_comp", 10)
        self.subscription
        self.accel_angle_z = 0
        self.gyro_angle_x = 0
        self.gyro_angle_y = 0
        self.gyro_angle_z = 0
        self.current_time = 0
        self.orientation_x = 0
        self.orientation_y = 0
        self.orientation_z = 0
        self.alpha = 0.96

    def listener_callback(self, msg):
        """TODO."""
        if self.current_time == 0:
            self.last_time = self.get_clock().now().nanoseconds
        self.current_time = self.get_clock().now().nanoseconds
        self.dt = (self.current_time - self.last_time) / (10**9)
        self.accel_angle_x = math.atan(
            msg.linear_acceleration.y
            / math.sqrt(msg.linear_acceleration.z**2 + msg.linear_acceleration.x**2)
        )
        self.accel_angle_y = math.atan(
            -1
            * msg.linear_acceleration.x
            / math.sqrt(msg.linear_acceleration.y**2 + msg.linear_acceleration.z**2)
        )
        self.orientation_x = (
            self.alpha * (self.orientation_x + msg.angular_velocity.x * self.dt)
            + (1 - self.alpha) * self.accel_angle_x
        )
        self.orientation_y = (
            self.alpha * (self.orientation_y + msg.angular_velocity.y * self.dt)
            + (1 - self.alpha) * self.accel_angle_y
        )
        self.orientation_z = (
            self.alpha * (self.orientation_z + msg.angular_velocity.z * self.dt)
            + (1 - self.alpha) * self.accel_angle_z
        )
        complementary_imu = Imu()
        complementary_imu.angular_velocity = msg.angular_velocity
        complementary_imu.linear_acceleration = msg.linear_acceleration
        q = quaternion.from_euler_angles(
            self.orientation_x, self.orientation_y, self.orientation_z
        )
        complementary_imu.orientation.x = q.x
        complementary_imu.orientation.y = q.y
        complementary_imu.orientation.z = q.z
        complementary_imu.orientation.w = q.w
        self.publisher_.publish(complementary_imu)


def main(args=None):
    """TODO."""
    rclpy.init(args=args)
    comp_filter = MPU6050ComplementaryFilter()
    rclpy.spin(comp_filter)

    comp_filter.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
