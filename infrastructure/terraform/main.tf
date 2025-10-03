terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecs_cluster" "hvac_cluster" {
  name = "hvac-ecs-cluster"
}

# Add ECS service, task definitions, RDS, etc. as needed
