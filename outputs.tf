output "terraphish_ip" {
  value = aws_instance.autosneakphish.public_ip
}
output "password" {
  value = "aws_iam_user_login_profile.${aws_iam_user.smtp_user.name}.password"
}
