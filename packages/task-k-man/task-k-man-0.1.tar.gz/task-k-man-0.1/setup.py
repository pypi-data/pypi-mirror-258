from setuptools import setup, find_packages

setup(
    name='task-k-man',
    version='0.1',
    description='A simple command-line task management application',
    author='Kiennd',
    author_email='kien.nguyenduc08@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'taskkman = taskkman.taskkman:main',
        ],
    },
    install_requires=[
        # List your dependencies here
    ],
)
