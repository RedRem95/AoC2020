[![GitHub](https://img.shields.io/github/license/RedRem95/AoC2020?style=for-the-badge)](LICENSE)

[![Unittests](https://img.shields.io/github/workflow/status/RedRem95/AoC2020/Unittests/master?style=for-the-badge&logo=github&label=Unittests)](https://github.com/RedRem95/AoC2020/actions?query=workflow%3AUnittests)
[![Lint AoC](https://img.shields.io/github/workflow/status/RedRem95/AoC2020/Lint%20AoC/master?style=for-the-badge&logo=github&label=Lint%20AoC)](https://github.com/RedRem95/AoC2020/actions?query=workflow%3A%22Lint+AoC%22)

[![GitHub version](https://img.shields.io/github/v/release/redrem95/AoC2020?label=Version&sort=semver&style=for-the-badge&logo=github)](https://github.com/RedRem95/AoC2020)

[![Codecov](https://img.shields.io/codecov/c/github/RedRem95/AoC2020?style=for-the-badge&logo=codecov)](https://codecov.io/gh/RedRem95/AoC2020)

![GitHub downloads](https://img.shields.io/github/downloads/RedRem95/AoC2020/total?label=Downloads&style=for-the-badge&logo=github)
![Repo size](https://img.shields.io/github/repo-size/RedRem95/AoC2020?label=Repo%20Size&style=for-the-badge&logo=github)
![Code size](https://img.shields.io/github/languages/code-size/RedRem95/AoC2020?label=Code%20Size&style=for-the-badge&logo=github)

# AoC 2020 Implementation

This is my implementation of the [2020 Advent of Code](https://adventofcode.com/2020) event.

## Features

Every implemented day should run. It's a very mediocre implementation for Advent of Code so dont expect any special
features.

## Getting Started

### Installation/Dependencies

This project was written using a conda environment. It is not necessary but still advised.

When using conda you should create your environment using the provided ``environment.yml`` file.

The only real necessary dependency although is [numpy](https://numpy.org/). The others stated in can be left out since
they are optional. You wont be able to use some of the features though.

* [requests](https://requests.readthedocs.io/en/master/) - Used to download your input of the day. You will also have to
  set the environment variable ``AOC_SESSION_ID`` with your personal session id. The simplest way to get it is by
  logging in with a browser and checking your cookies.
* [packaging](https://packaging.python.org/overview/) - Used to parse own version into an version object that could be
  compared and such stuff. So this is absolutely optional and not required at all if you want to keep it lightweight. I
  just thought it would be neat.

### Usage

Simply run ``main.py`` inside your environment.

Use ``main.py -h`` to see all usable options

### Add a day

To add a day, add it into the AoC2020 package.
Simply create a package for the Day like ``DayXX`` and create a class with the same name in the ``__init__.py``.
This class has to inherit from the ``AoC.Day.Day`` class and call its ``__init__`` upon creation to be added to the list of implemented days.
Call ``self.get_input(task)`` to get the input provided for the task and day.

### Tests

Tests are written using pytest. Simply add them under their conventions into the ``test`` package.

## License

[GPL-3.0](LICENSE)
