# Pyclops CLI

## Overview

***This project is still under development and is not fully featured yet - CLI/API is subject to change***

Pyclops is a Python-orientated build tool/project generator focused on generating projects for and deploying project to the cloud. With a few simple commands, Pyclops allows you to generate a brand new project from a template project and deploy it to the cloud. For example, Pyclops allows you to generate a fresh Django project and deploy it to Docker containers running on AWS. Or you can generate a Serverless Lambda project, Python Flask project, React front-end project, etc. Since Pyclops generates projects from templates, there are literally no bounds to what kind of project can be generated. You can choose to create you own templates, or use our growing library of built-in defaults.

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

Pyclops generates Github repositories for you. To do this, it requires access to your Github account. Before running the commands below, generate a personal access token on Github and set your `GITHUB_OAUTH` environment varibale:

```
export GITHUB_OAUTH=<personal_access_token>
```

The Pyclops CLI is self-describing. Each command has a `--help` flag that will provided more instructions on how to use it:

```
pyclops --help
```

Some common workflows are described below.

### Generate and deploy a Django project to ECS/Fargate on AWS

...

### Generate and deploy a Flask project to ECS/Fargate on AWS

...

### Generate and deploy a Serverless AWS Lambda/API Gateway project

The [AWS Serverless template](https://github.com/Stavatech/AWS-Serverless-Template) is a API Gateway/Lambda project mastered in CLoudformation. It is based off of a project generated using the SAM CLI provided by AWS. It is completely backwards compatible with the SAM CLI, so if you decide you no longer want to use Pyclops, you are not locked in.

To generate a Lambda project with Pyclops, run the following command:

```
pyclops aws serverless generate-project --project-name my-project --git-owner githubusername --branch master --deployment-bucket some-unique-s3-bucket-name /path/to/working_directory
```

The above command will generate a project in the specified working directory and push it onto Github. To deploy the project to AWS, navigate to the working directory and run the follow commands:

```
pyclops aws serverless package
pyclops aws cloudformation deploy --stack-name pyclops-lambda-test --template-file build/serverless/serverless.template.yml --capabilities CAPABILITY_AUTO_EXPAND,CAPABILITY_IAM
```


### Generate and deploy a React front-end project to AWS S3/Cloudfront

...

### Generate and deploy a Virtual Private Cloud (VPC) on AWS

...

### Build (merge multiple Cloudformation Jinja templates) and deploy a Cloudformation stack

...
