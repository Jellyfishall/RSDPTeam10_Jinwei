import os
from glob import glob

from setuptools import find_packages, setup

package_name = "rover_slam"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
        (os.path.join("share", package_name, "config"), glob("config/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="nzh",
    maintainer_email="nzh@todo.todo",
    description="Cartographer launch/config package for Leo Rover with RPLIDAR A2M12",
    license="Apache License 2.0",
    entry_points={
        "console_scripts": [],
    },
)
