## Infra Usage Collector Nomad

### How to run it

Before starting it, ensure you already have python and pip installed.

```
git clone <repo_url>
cd <dir_name>
python3 -m venv venv
```

Create `.env` file:

```
cat << EOF >> .env
PROMETHEUS_URL=<prometheus_url>

```

Create config file:

```
cat << EOF >> config.cfg
[azure]
clientId = <client_id>
clientSecret = <client_secret>
tenantId = <tenant_id>

[sheet]
site_id = <site_id>
item_id = <item_id>
```

Create minimal query config for prometheus:

```
cat << EOF >> query.cfg
[nodes]
nodes_detail = node_uname_info
total_cpu_core = count(count(node_cpu_seconds_total{mode="system"}) by (cpu, instance)) by (instance)
cpu_usage_per_node = 100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
total_memory_size = node_memory_MemTotal_bytes
memory_usage_per_node = 100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

[nomad_cluster]
nomad_client_details = nomad_client_uptime
nomad_client_allocations = nomad_client_allocations_running
nomad_client_cpu_usage = 100 - nomad_client_unallocated_cpu/(nomad_client_allocated_cpu + nomad_client_unallocated_cpu) * 100
nomad_client_memory_usage = 100 - nomad_client_unallocated_memory / (nomad_client_allocated_memory + nomad_client_unallocated_memory) * 100

[nomad_job]
nomad_job_complete_summary = nomad_nomad_job_summary_complete
nomad_job_failed_summary = nomad_nomad_job_summary_failed
nomad_job_starting_summary = nomad_nomad_job_summary_starting
nomad_job_running_summary = nomad_nomad_job_summary_running

[nomad_allocs]
nomad_allocs_cpu_allocated = nomad_client_allocs_cpu_allocated
nomad_allocs_memory_allocated = nomad_client_allocs_memory_allocated
nomad_allocs_memory_max_usage = nomad_client_allocs_memory_max_usage
```
