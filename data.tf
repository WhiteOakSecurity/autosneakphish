data "aws_region" "current" {}

data "aws_vpc" "selected" {
  id = var.vpc_id
}
