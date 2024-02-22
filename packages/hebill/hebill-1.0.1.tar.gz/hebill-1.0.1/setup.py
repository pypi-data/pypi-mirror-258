# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='hebill',
    version='1.0.1',
    packages=find_packages(),
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "Flask==3.0.2",
        "colorama==0.4.6",
        "bcrypt==4.1.2"
    ],
    entry_points={
        'console_scripts': [
            'hebill = hebill.libraries.hebill_system.console:run',
        ],
    },
    python_requires='>=3.12',
)
