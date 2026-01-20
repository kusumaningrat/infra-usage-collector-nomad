job "Nomad-Report-Scrapping" {
  datacenters = ["glynac-dc"]
  type        = "batch"
  namespace   = "infrastructure"

  periodic {
    cron             = "0 2 1 * *" # First day of month at 2 AM (02:00)
    prohibit_overlap = true
    time_zone        = "Asia/Jakarta"
  }

  group "nomad-report" {
    constraint {
      attribute = "${attr.unique.hostname}"
      value     = "Worker-02"
    }

    task "nomad-report" {
      driver = "docker"

      config {
        image = "image-reg.ops.glynac.ai/nomad-report-app/nomad-report"
        auth {
          username       = "admin"
          password       = "GlynacP455"
          server_address = "harbor-registry.service.consul:8085"
        }
      }
      service {
        tags = ["public", "logs.promtail"]
        name = "nomad-report"
      }
      env {
        PROMETHEUS_URL = "http://prometheus.service.consul:9090"
      }

      resources {
        cpu    = 80
        memory = 80
      }
    }
  }
}