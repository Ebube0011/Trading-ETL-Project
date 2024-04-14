resource "aws_key_pair" "sde_auth" {
  key_name   = "sdekey"
  public_key = file("~/.ssh/sdekey.pub")
}


# Create security group for access to EC2 from your Anywhere
resource "aws_security_group" "sde_security_group" {
  name        = "sde_security_group"
  description = "Security group to allow ssh"

  ingress {
    description = "Inbound SCP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sde_security_group"
  }
}


resource "aws_instance" "sde_ec2" {
  ami             = data.aws_ami.ubuntu.id
  instance_type   = var.instance_type
  key_name        = aws_key_pair.sde_auth.key_name
  security_groups = [aws_security_group.sde_security_group.name]
  user_data       = file("user_data.tpl")

  root_block_device {
    volume_size = 25
  }

  tags = {
    Name = "sde_ec2"
  }

  provisioner "local-exec" {
    command = templatefile("windows-ssh-config.tpl", {
      hostname     = self.public_ip,
      user         = "ubuntu",
      identityfile = "~/.ssh/sdekey"
    })

    interpreter = ["Powershell", "-Command"]
  }
}