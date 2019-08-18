import os


project_name = "mock_project"

github_token = "mock_token"
github_user = "abd"
github_repo = "def"
git_branch = "ghi"

stages = {
        "staging": {
            "domain": "staging.mock.com",
            "hosted_zone_id": "ABCDEFG",
            "container_count": 1,
            "container_port": 8000,
            "container_cpu": 256,
            "container_memory": 512
        }, "production": {
            "domain": "www.mock.com",
            "hosted_zone_id": "ABCDEFG",
            "container_count": 2,
            "container_port": 8000,
            "container_cpu": 1024,
            "container_memory": 2048
        }
}

ecr_repo = "ecr_repo"

load_balancer_path = "*"
load_balancer_priority = 1

image_tag = os.getenv('IMAGE_TAG')
