======
toyapp
======

.. image:: https://img.shields.io/pypi/v/toyapp.svg
        :target: https://test.pypi.org/pypi/toyapp

.. image:: https://img.shields.io/docker/image-size/ian1roberts/toyapp/latest
   :alt: Docker Image Size (tag)


Abstract
--------

Experiment with cookiecutter and docker to create a robust python tool that
can be run directly in a container.

This toy project introduces the following concepts:

- Creating python packages from a cookiecutter template
- Basic elements of simple python package, including setuptools, entry points, and testing
- Adding a simple command line interface thanks to click
- Using docker to containerize the application 

The toy application takes two numbers and a mathemtical operation and returns the result

Quickstart
----------

Install the package with pip. 

.. code-block:: bash

    $ mkdir demo
    $ cd demo
    $ git clone https://github.com/ian1roberts/toyapp.git
    $ cd toyapp
    $ pip install .

Try out the command line interface

.. code-block:: bash

    $ toyapp 1 2 "+"

Note that the operators must be quoted to avoid shell expansion.

Check out the help

.. code-block:: bash

    $ toyapp --help

    Usage: toyapp [OPTIONS] NUM1 NUM2 [OPERATION]

    Perform simple arithmetic operations given two numbers and an operator.

    If operator is ommited, the default is addition. To prevent * being
    interpreted as a wildcard, use quotes around the operator.

    --quiet, -q: Don't print the leading message, just return the result.
    num1: float - The first number
    num2: float - The second number
    operation: str -The operation to perform on the two numbers

    Evaluates the expression num1 operation num2 and prints the result.

    Options:
        -q, --quiet  Don't print the result
        --help       Show this message and exit.

Features
--------

The repository includes a `Makefiile` and `Dockerfile` to build and run the application in a container.

To build the container, run `make build`.

You can also pull the image from dockerhub with `docker pull ian1roberts/toyapp:latest`


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Appendix
--------
* Free software: MIT license
* Documentation: https://toyapp.readthedocs.io.