"""Start all nodes to demonstrate capabilities."""
import launch
import launch.actions
import launch.substitutions

import launch_ros.actions


def generate_launch_description():
    """TODO."""
    return launch.LaunchDescription(
        [
            launch_ros.actions.Node(
                name="complementary_filter",
                package="mpu_6050_tools",
                executable="complementary_filter",
                output="screen",
                remappings=[("/imu/data_raw", "/balancing/imu/data_raw")],
            ),
        ]
    )
