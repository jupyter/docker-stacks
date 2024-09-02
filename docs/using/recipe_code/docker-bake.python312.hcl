group "default" {
    targets = ["custom-notebook"]
}

target "foundation" {
    context = "https://github.com/jupyter/docker-stacks.git#main:images/docker-stacks-foundation"
    args = {
        PYTHON_VERSION = "3.12"
    }
    tags = ["docker-stacks-foundation"]
}


target "base-notebook" {
    context = "https://github.com/jupyter/docker-stacks.git#main:images/base-notebook"
    contexts = {
        docker-stacks-foundation = "target:foundation"
    }
    args = {
        BASE_CONTAINER = "docker-stacks-foundation"
    }
    tags = ["base-notebook"]
}

target "minimal-notebook" {
    context = "https://github.com/jupyter/docker-stacks.git#main:images/minimal-notebook"
    contexts = {
        base-notebook = "target:base-notebook"
    }
    args = {
        BASE_CONTAINER = "base-notebook"
    }
    tags = ["minimal-notebook"]
}

target "custom-notebook" {
    context = "."
    contexts = {
        minimal-notebook = "target:minimal-notebook"
    }
    args = {
        BASE_CONTAINER = "minimal-notebook"
    }
    tags = ["custom-jupyter"]
}
