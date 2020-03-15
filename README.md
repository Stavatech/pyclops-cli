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

## Setup

### Git/Github

Pyclops generates Github repositories for you. To do this, it requires access to your Github account. Before running the commands below, generate a personal access token on Github and set your `GITHUB_TOKEN` environment varibale:

```
export GITHUB_TOKEN=<personal_access_token>
```

Also ensure that git has been configured with your Github account:
```
git config --global user.email "my.email@provider.com"
git config --global user.name "My Name"
```

### AWS

For AWS templates, you will need to have the AWS CLI configured with the credentials of the account you want to deploy to. To do this, see the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration).

## Usage

The Pyclops CLI is self-describing. Each command has a `--help` flag that will provided more instructions on how to use it:

```
pyclops --help
```

Some common workflows are described below.

### Generate and deploy a Django project to ECS/Fargate on AWS

To generate the Django project and repository, run the following command:
```
pyclops django --project-name pyclops-django-project --git-owner githubusername --branch master /path/to/working_directory/pyclops-django-project
```

The above command will generate a project in the specified working directory and push it onto Github. Next, in order to be able to deploy to AWS, run the following commands to create the ECR docker repository and build and push a Docker image to that repository:
```
### TODO:
- Add Pyclops command to create ECR repository
- Add Pyclops command to build and push Docker image to ECR repository
```

The above command will have printed out an ECR repository ARN. Copy this ARN into the `ecr_repo` field in the `params.py` file in the base directory of your project.

You are now all set to build and deploy your project to AWS. In the base directry of your project, run the following commands:
```
pyclops aws cloudformation build --template-dir cfn/service --params-file params.py 
pyclops aws cloudformation deploy --stack-name pyclops-django-project --template-file build/serverless/serverless.template.yml --capabilities CAPABILITY_IAM
```

### Generate and deploy a Flask project to ECS/Fargate on AWS

...

### Generate and deploy a Serverless AWS Lambda/API Gateway project

The [AWS Serverless template](https://github.com/Stavatech/AWS-Serverless-Template) is a API Gateway/Lambda project mastered in CLoudformation. It is based off of a project generated using the SAM CLI provided by AWS. It is completely backwards compatible with the SAM CLI, so if you decide you no longer want to use Pyclops, you are not locked in.

To generate a Lambda project with Pyclops, run the following command:

```
pyclops aws serverless generate-project --project-name pyclops-lambda-project --git-owner githubusername --branch master --deployment-bucket some-unique-s3-bucket-name /path/to/workspace/pyclops-lambda-project
```

The above command will generate a project in the specified working directory and push it onto Github. To deploy the project to AWS, navigate to the working directory and run the follow commands:

```
pyclops aws serverless package
pyclops aws cloudformation deploy --stack-name pyclops-lambda-project --template-file build/serverless/serverless.template.yml --capabilities CAPABILITY_AUTO_EXPAND,CAPABILITY_IAM
```


### Generate and deploy a React front-end project to AWS S3/Cloudfront

...

### Generate and deploy a Virtual Private Cloud (VPC) on AWS

...

### Build (merge multiple Cloudformation Jinja templates) and deploy a Cloudformation stack

...
