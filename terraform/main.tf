provider "local" {}

resource "local_file" "mini_app_info" {
  filename = "${path.module}/deployment_info.txt"
  content  = <<EOT
Mini Logistics Tracker Deployment

Container: mini-app
Port: 5000
Monitoring: Prometheus (9090), Grafana (3000)

This file is generated using Terraform to simulate infrastructure setup.
EOT
}
