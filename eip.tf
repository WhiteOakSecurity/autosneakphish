resource "aws_eip" "phishingtime" {
  instance = aws_instance.autosneakphish.id
  vpc      = true
}


