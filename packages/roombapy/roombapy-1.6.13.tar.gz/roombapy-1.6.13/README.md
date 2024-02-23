# roombapy

[![CI](https://github.com/pschmitt/roombapy/actions/workflows/ci.yaml/badge.svg)](https://github.com/pschmitt/roombapy/actions/workflows/ci.yaml)
[![PyPI](https://img.shields.io/pypi/v/roombapy)](https://pypi.org/project/roombapy/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/roombapy)](https://pypi.org/project/roombapy/)
[![PyPI - License](https://img.shields.io/pypi/l/roombapy)](./LICENSE)

Unofficial iRobot Roomba python library (SDK).

Fork of [NickWaterton/Roomba980-Python](https://github.com/NickWaterton/Roomba980-Python)

This library was created for the [Home Assistant Roomba integration](https://www.home-assistant.io/integrations/roomba/).

# Installation

```shell
pip install roombapy
```

# Notes

This library is only for firmware 2.x.x [Check your robot version!](http://homesupport.irobot.com/app/answers/detail/a_id/529)

Only local connections are supported.

# How to get your username/blid and password

To get password from Roomba type in console:

```shell
$ roomba-password <ip>
```

It will find your Roomba in local network, then follow the instructions in console to get password.
If IP address not provided password will be request for auto discovered robot.

Also you can just ask Roomba for info:

```shell
$ roomba-discovery <optional ip address>
```

To test connection with iRobot:

```shell
$ roomba-connect <ip> <password>
```

## Development

To improve your development experience, you can install pre-commit hooks via the following command.
With every commit it will run a set of checks, making sure it meets the quality standards.

```shell
pre-commit install
```
