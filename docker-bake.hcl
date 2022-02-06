group "default" {
  targets = [
    "base-notebook",
    "minimal-notebook",
    "r-notebook",
    "scipy-notebook",
    "tensorflow-notebook",
    "datascience-notebook",
    "pyspark-notebook",
    "all-spark-notebook"
  ]
}

group "linux-arm64" {
  targets = [
    "base-notebook",
    "minimal-notebook",
    "r-notebook",
    "scipy-notebook",
    "pyspark-notebook",
    "all-spark-notebook"
  ]
}

variable "OWNER" {
  default = "jupyter"
}

function "tags" {
  params = [image]
  result = ["${OWNER}/${image}:latest"]
}

target "_default" {
  args = {
    OWNER = OWNER
  }
  platforms = ["linux/amd64", "linux/arm64"]
}

target "base-notebook" {
  inherits = ["_default"]
  context = "base-notebook"
  tags = tags("base-notebook")
}

target "minimal-notebook" {
  inherits = ["_default"]
  context = "minimal-notebook"
  tags = tags("minimal-notebook")
}

target "r-notebook" {
  inherits = ["_default"]
  context = "r-notebook"
  tags = tags("r-notebook")
}

target "scipy-notebook" {
  inherits = ["_default"]
  context = "scipy-notebook"
  tags = tags("scipy-notebook")
}

target "tensorflow-notebook" {
  inherits = ["_default"]
  context = "tensorflow-notebook"
  tags = tags("tensorflow-notebook")
  platforms = ["linux/amd64"]
}

target "datascience-notebook" {
  inherits = ["_default"]
  context = "datascience-notebook"
  tags = tags("datascience-notebook")
  platforms = ["linux/amd64"]
}

target "pyspark-notebook" {
  inherits = ["_default"]
  context = "pyspark-notebook"
  tags = tags("pyspark-notebook")
}

target "all-spark-notebook" {
  inherits = ["_default"]
  context = "all-spark-notebook"
  tags = tags("all-spark-notebook")
}
