# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='hebill',
    version='1.0.7',
    packages=find_packages(),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "Flask==3.0.2",
        "colorama==0.4.6",
        "bcrypt==4.1.2"
    ],
    entry_points={
        'console_scripts': [
            'hebill = hebill.libraries.hebill_system.run_console:run',
        ],
    },
    package_data={
        '': ['**/*.ini', '**/*.txt', 'CHANGELOG.md, LICENSE.rst']
    },
    python_requires='>=3.12',
)
