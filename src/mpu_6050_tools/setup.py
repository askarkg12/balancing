from setuptools import setup

package_name = "mpu_6050_tools"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Askar Sulaimanov",
    maintainer_email="askarkg12@gmail.com",
    description="A package with tools for working with MPU6050 IMU",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "complementary_filter = mpu_6050_tools.complementary_filter:main"
        ],
    },
)
