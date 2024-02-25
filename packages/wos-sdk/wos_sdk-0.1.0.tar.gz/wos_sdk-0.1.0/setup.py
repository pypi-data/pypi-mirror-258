# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wos_sdk',
    version='0.1.0',
    description='Python SDK for interact with WinGs Operating System',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='WinGs Robotics',
    author_email="dev@wingsrobotics.com",
    packages=find_packages(include=['wos_sdk']),
    install_requires=[
        # List your project dependencies here
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)