variable "aws_region"   { default = "us-east-1" }
variable "project_name" { default = "flask-app" }
variable "db_password"  { sensitive = true }
variable "db_username"  { default = "flaskuser" }
variable "db_name"      { default = "flaskdb" }
variable "instance_type" { default = "t3.micro" }
variable "ami_id"        { default = "ami-0c02fb55956c7d316" } # Amazon Linux 2 us-east-1