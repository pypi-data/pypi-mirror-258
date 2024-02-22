from setuptools import setup, find_packages

setup(
    name='GoTaskz',
    version='0.1',
    description='A simple command-line task management application',
    author='',
    author_email='',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gotaskz = gotaskz.gotaskz:main',
        ],
    },
    install_requires=[
        # List your dependencies here
    ],
)
