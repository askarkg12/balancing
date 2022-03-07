from setuptools import setup

package_name = 'mpy_6050_tools'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='askar',
    maintainer_email='askar.sulaimanov@arctoris.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'complemetary_filter = mpy_6050_tools.complemetary_filter:main'
        ],
    },
)
