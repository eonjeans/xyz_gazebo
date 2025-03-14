from setuptools import find_packages, setup

package_name = 'goal'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/multi_node.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='addinedu',
    maintainer_email='zkzkdh0818@g.skku.edu',
    description='ROS 2 package for goal-based navigation with separate nodes',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pose_estimator = goal.pose_estimator_node:main',
            'goal_navigator = goal.goal_navigator_node:main',
            'user_input = goal.user_input_node:main',
        ],
    },
)
