#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup  # type: ignore

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

test_requirements = ["pytest"]

setup(
    author="Ian Roberts",
    author_email="ian1blog@icloud.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Experiment with cookiecutter and docker to create a toyapp",
    entry_points={
        "console_scripts": [
            "toyapp=toyapp.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="toyapp",
    name="toyapp",
    packages=find_packages(include=["toyapp", "toyapp.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ian1roberts/toyapp",
    version="0.1.2",
    zip_safe=False,
)
