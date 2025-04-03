group "default" {
    targets = ["custom-notebook"]
}

target "foundation" {
    context = "https://github.com/jupyter/docker-stacks.git#main:images/docker-stacks-foundation"
    args = {
        PYTHON_VERSION = "3.13"
    }
    tags = ["docker-stacks-foundation"]
}

target "base-notebook" {
    context = "https://github.com/jupyter/docker-stacks.git#main:images/base-notebook"
    contexts = {
        docker-stacks-foundation = "target:foundation"
    }
    args = {
        BASE_IMAGE = "docker-stacks-foundation"
    }
    tags = ["base-notebook"]
}

target "minimal-notebook" {
    context = "https://github.com/jupyter/docker-stacks.git#main:images/minimal-notebook"
    contexts = {
        base-notebook = "target:base-notebook"
    }
    args = {
        BASE_IMAGE = "base-notebook"
    }
    tags = ["minimal-notebook"]
}

target "custom-notebook" {
    context = "."
    contexts = {
        minimal-notebook = "target:minimal-notebook"
    }
    args = {
        BASE_IMAGE = "minimal-notebook"
    }
    tags = ["custom-jupyter"]
}
