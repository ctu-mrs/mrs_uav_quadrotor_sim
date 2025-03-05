#!/usr/bin/env python3

import launch
import os
import sys

from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    LaunchConfiguration,
    IfElseSubstitution,
    PythonExpression,
    PathJoinSubstitution,
    EnvironmentVariable,
)

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    ld = launch.LaunchDescription()

    pkg_name = "mrs_multirotor_simulator"

    pkg_share_path = get_package_share_directory(pkg_name)
    namespace='multirotor_simulator'

    custom_config = LaunchConfiguration('custom_config')

    # this adds the args to the list of args available for this launch files
    # these args can be listed at runtime using -s flag
    # default_value is required to if the arg is supposed to be optional at launch time
    ld.add_action(DeclareLaunchArgument(
        'custom_config',
        default_value="",
        description="Path to the custom configuration file. The path can be absolute, starting with '/' or relative to the current working directory",
    ))

    # behaviour:
    #     custom_config == "" => custom_config: ""
    #     custom_config == "/<path>" => custom_config: "/<path>"
    #     custom_config == "<path>" => custom_config: "$(pwd)/<path>"
    custom_config = IfElseSubstitution(
            condition=PythonExpression(['"', custom_config, '" != "" and ', 'not "', custom_config, '".startswith("/")']),
            if_value=PathJoinSubstitution([EnvironmentVariable('PWD'), custom_config]),
            else_value=custom_config
    )

    ld.add_action(ComposableNodeContainer(

        namespace='',
        name=namespace+'_container',
        package='rclcpp_components',

        executable='component_container_mt',

        # prefix=['debug_roslaunch ' + os.ttyname(sys.stdout.fileno())],

        composable_node_descriptions=[

            ComposableNode(

                package=pkg_name,
                plugin='mrs_multirotor_simulator::MultirotorSimulator',
                namespace='',
                name='multirotor_simulator',
                parameters=[
                    # the main config
                    {'config': pkg_share_path + '/config/multirotor_simulator.yaml'},
                    # control pipeline configs
                    pkg_share_path + '/config/controllers/attitude_controller.yaml',
                    pkg_share_path + '/config/controllers/rate_controller.yaml',
                    pkg_share_path + '/config/controllers/position_controller.yaml',
                    pkg_share_path + '/config/controllers/velocity_controller.yaml',
                    pkg_share_path + '/config/controllers/mixer.yaml',
                    # the UAV configs
                    pkg_share_path + '/config/uavs/a300.yaml',
                    pkg_share_path + '/config/uavs/f330.yaml',
                    pkg_share_path + '/config/uavs/f450.yaml',
                    pkg_share_path + '/config/uavs/f550.yaml',
                    pkg_share_path + '/config/uavs/naki.yaml',
                    pkg_share_path + '/config/uavs/robofly.yaml',
                    pkg_share_path + '/config/uavs/t650.yaml',
                    pkg_share_path + '/config/uavs/x500.yaml',
                    # the list of uavs to be spawned
                    {'config_uavs': pkg_share_path + '/config/uavs.yaml'},
                    # custom config
                    {'custom_config': custom_config}
                ],

                remappings=[
                    ("~/clock_out", "/clock"),
                ],
            )

        ],

        output='screen',

    ))

    return ld
