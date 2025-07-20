from setuptools import setup, find_packages

setup(
    name='bin',
    version='0.1',
    packages=find_packages(),  # This will include the bin/ folder with __init__.py
    description='A library for handling binary data',
)
