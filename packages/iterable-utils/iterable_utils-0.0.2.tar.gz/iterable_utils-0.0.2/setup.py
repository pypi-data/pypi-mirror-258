from setuptools import setup, find_packages

setup(
    name='iterable_utils',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        "numpy>=1.26.2"
    ],
    author='fleecy',
    description='utils for iterable objects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
