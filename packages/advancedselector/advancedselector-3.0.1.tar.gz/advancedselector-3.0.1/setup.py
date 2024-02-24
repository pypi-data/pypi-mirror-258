from setuptools import setup

setup(
    # other setup configurations...
    install_requires=[
        # Your other dependencies here
        'getch>=1.0.0; sys_platform == "linux" or sys_platform == "linux2"',
    ],
)
