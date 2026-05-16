output "alb_dns" {
  value = aws_lb.alb.dns_name
}
output "db_endpoint" {
  value     = aws_db_instance.postgres.address
  sensitive = true
}
output "ec2_a_id" { value = aws_instance.ec2_a.id }
output "ec2_b_id" { value = aws_instance.ec2_b.id }