terraform {
  required_version = ">= 0.11.0"
}

resource "aws_key_pair" "autosneakphish" {
  key_name   = "keyname_replacer"
  public_key = "publickey_replacer"
}

resource "aws_security_group" "autosneakphish" {
  name = "autosneakphish"
  description = "White Oak Security goes Phishing"
  vpc_id = data.aws_vpc.selected.id 

  ingress {
    from_port = 3333
    to_port = 3333
    protocol = "tcp"
    cidr_blocks = [var.whitelist_cidr]
  } 
 ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [var.whitelist_cidr]
  }
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 60000
    to_port = 61000
    protocol = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 53
    to_port = 53
    protocol = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 25
    to_port = 25
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 465
    to_port = 465
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

