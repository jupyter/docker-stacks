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


target "_default" {
  args = {
    OWNER = OWNER
  }
  platforms = ["linux/amd64", "linux/arm64"]
}

target "base-notebook" {
  inherits = ["_default"]
  context = "base-notebook"
  tags = [
    "${OWNER}/base-notebook:latest"
  ]
}

target "minimal-notebook" {
  inherits = ["_default"]
  context = "minimal-notebook"
  tags = [
    "${OWNER}/minimal-notebook:latest"
  ]
}

target "r-notebook" {
  inherits = ["_default"]
  context = "r-notebook"
  tags = [
    "${OWNER}/r-notebook:latest"
  ]
}

target "scipy-notebook" {
  inherits = ["_default"]
  context = "scipy-notebook"
  tags = [
    "${OWNER}/scipy-notebook:latest"
  ]
}

target "tensorflow-notebook" {
  inherits = ["_default"]
  context = "tensorflow-notebook"
  tags = [
    "${OWNER}/tensorflow-notebook:latest"
  ]
  platforms = ["linux/amd64"]
}

target "datascience-notebook" {
  inherits = ["_default"]
  context = "datascience-notebook"
  tags = [
    "${OWNER}/datascience-notebook:latest"
  ]
  platforms = ["linux/amd64"]
}

target "pyspark-notebook" {
  inherits = ["_default"]
  context = "pyspark-notebook"
  tags = [
    "${OWNER}/pyspark-notebook:latest"
  ]
}

target "all-spark-notebook" {
  inherits = ["_default"]
  context = "all-spark-notebook"
  tags = [
    "${OWNER}/all-spark-notebook:latest"
  ]
}
