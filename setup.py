# -*- coding: utf-8 -*-

import setuptools
from os import path
from typing import List

README = "README.md"
REQUIREMENTS = "requirements.txt"
VERSION = "VERSION"

root_dir = path.abspath(path.dirname(__file__))

def version() -> str:
    with open(VERSION, "r") as f:
        return f.readline().strip()

def readme() -> str:
    with open(README, "r") as f:
        return f.read()

def requirements() -> List[str]:
    return [name.rstrip() for name in open(path.join(root_dir, REQUIREMENTS)).readlines()]

setuptools.setup(
    name="lkj",
    version=version(),
    author="Aki-7",
    license="MIT",
    author_email="aki.develop8128@gmail.com",
    description="CLI tool to report working time to Google Calendar",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/gray-armor/lkj",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['lkj = lkj.cli:main']
    },
    python_requires='>=3.7',
    install_requires=requirements(),
)
