resource "aws_instance" "autosneakphish" {
  ami           = var.ami
  instance_type = "t2.micro"
  key_name      = var.private_key
  vpc_security_group_ids = [aws_security_group.autosneakphish.id]
  tags = {
    Name = "autosneakphish"
  }
provisioner "local-exec" {
  command = "sleep 60; ANSIBLE_HOST_KEY_CHECKING=false ansible-playbook -u ubuntu -i ',${self.public_ip}' --private-key ${var.private_key} ansible/phish-playbook.yml"
  }
}
