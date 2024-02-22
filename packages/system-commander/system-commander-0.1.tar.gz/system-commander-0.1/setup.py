from setuptools import setup,find_packages
import os


requirements = os.popen('pipreqs system-commander --print').read().splitlines()

with open('README.md','r') as file:
    long_description = file.read()

setup(
    name='system-commander',
    version='0.1',
    description='Python package for controlling system actions',
    author='Karthikeyan',
    author_email='karthikeyan02022003@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://git.selfmade.ninja/karthikeyanramesh/python-pip-packages/",
    install_requires=[],
    entry_points={
        'console_scripts' : [
            'system-commander=system.main:main',
        ],
    },
)
