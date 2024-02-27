from setuptools import setup, find_packages

setup(
    name='cloudwatchlogger',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'boto3',
    ],
)
