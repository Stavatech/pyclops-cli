import os
import docker
import json


DEFAULT_TAG:str = "latest"


def build_image(dockerfile, repository, tag=DEFAULT_TAG, rm=True, build_args={}):
    client = docker.from_env()
    repo_tag = f"{repository}:{tag}"

    if os.path.isfile(dockerfile):
        for byte_str in client.build(path=".", dockerfile=dockerfile, tag=repo_tag, rm=rm, buildargs=build_args):
            lines = byte_str.decode("utf-8").splitlines()
            for line in lines:
                print(json.loads(line)['stream'].strip())
    else:
        raise FileNotFoundError(dockerfile)

    return client.inspect_image(repo_tag)


def push_image(repository, username, password, registry):
    client = docker.from_env()
    auth_data = {'username': username, 'password': password}
    for line in client.push(repository=repository, stream=True, decode=True, auth_config=auth_data):
        print(line)


def tag_image(image_id, repository, tag):
    client = docker.from_env()
    client.tag(image_id, repository, tag)
