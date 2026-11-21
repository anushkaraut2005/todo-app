terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "npipe:////.//pipe//docker_engine"
}

data "docker_image" "todo" {
  name = "todo-app:latest"
}

resource "docker_container" "todo" {
  name  = "todo-terraform"
  image = data.docker_image.todo.id

  ports {
    internal = 5000
    external = 5001
  }
}