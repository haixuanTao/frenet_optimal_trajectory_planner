from setuptools import Distribution
import setuptools.command.build_ext as _build_ext
from distutils.core import setup, Extension
import os
import subprocess

from setuptools import find_packages


# For running external build
class build_ext(_build_ext.build_ext):
    def run(self):
        command = ["./build.sh"]
        subprocess.check_call(command)


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


def main():
    pwd = os.path.dirname(os.path.realpath(__file__))
    # os.environ["CC"] = "g++"
    # os.environ["CXX"] = "g++"
    # Path to Eigen might differ, replace path if necessary
    command = ["./build.sh"]
    subprocess.check_call(command)
    CFLAGS = [
        "-std=c++11",
        "-fPIC",
        "-shared",
        "-I",
        "-O3",
        "-pthread",
        "-Wall",
        "-I/usr/include/eigen3",
    ]

    LDFLAGS = []
    LDFLAGS += ["-Xlinker", "-export-dynamic"]
    LDFLAGS += ["-W", "-Wno-undef", "-lstdc++", "-static-libstdc++"]

    # Link static library libPackageFrenetOptimalTrajectory.a
    LDFLAGS += ["-L" + os.path.join(pwd, "build"), "-lPackageFrenetOptimalTrajectory"]
    LDFLAGS += ["-I", "/usr/include/x86_64-linux-gnu/qt5/QtCore", "-l", "Qt5Core"]
    print("Linker Flag:", LDFLAGS)

    module = Extension(
        "fot_planner",
        sources=["src/FrenetOptimalTrajectory/planner_package.cpp"],
        language="C++",
        include_dirs=[
            "src",
            "src/CubicSpline",
            "src/Polynomials",
            "src/FrenetOptimalTrajectory",
            "src/Obstacle",
            "src/Car",
            "FrenetOptimalTrajectory",
        ],
        extra_compile_args=CFLAGS,
        extra_link_args=LDFLAGS,
    )

    setup(
        name="frenetoptimaltrajectory",
        version="1.0.0",
        description="FOT Planner",
        author="ERDOS Project",
        packages=find_packages(),
        url="https://github.com/erdos-project/",
        package_data={"": ["**/*.so"]},
        include_package_data=True,
        # ext_modules=[module],
        # cmdclass={"build_ext": build_ext},
    )


if __name__ == "__main__":
    main()
