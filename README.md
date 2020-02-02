# Pyclops CLI

## Overview


## Installation

### Set up a Python virtual environment (optional)

Setting up a new virtual environment is not required, but recommended, especially if you are planning to install from source in order to further develop the tool. This will allow you to have a fresh Python environment when working with Pyclops and will prevent version conflicts with other software on your machine.

To set up a virtual environment, do the following:

1. Follow the instructions [here](https://github.com/pyenv/pyenv) to install `pyenv` - a Python version management tool.
1. Follow the instructions [here](https://github.com/pyenv/pyenv-virtualenv) to install the `pyenv-virtualenv` plugin - a pyenv plugin that allows you to create and manage virtual environments.
1. Run the following commands to set up a virtual environment for Pyclops:
```
pyenv install 3.7.1
pyenv virtualenv 3.7.1 pyclops-venv
pyenv activate pyclops-venv
```

Pyclops was developed using Python 3.7.1. It should work with Python >=3.6.

### Install from PyPi

The simplest way to install Pyclops is via PyPi:

```
pip install pyclops
```

### Install from source

For the latest features, install Pyclops from source:

```
git clone git@github.com:Stavatech/pyclops-cli.git
cd pyclops-cli
pip install -e .
```

## Usage

The Pyclops CLI is self-describing. Each command has a `--help` flag that will provided more instructions on how to use it:

```
pyclops --help
```