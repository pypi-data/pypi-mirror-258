from setuptools import setup, find_packages

setup(
    name="lambda_tago",
    version="0.1.0",
    description="A custom library for interacting with Tago",
    author="Vincent Raaijmakers",
    packages=find_packages(),
    install_requires=[
        # Any dependencies you need to install along with your package, e.g.,
        # 'requests',
    ],
)
