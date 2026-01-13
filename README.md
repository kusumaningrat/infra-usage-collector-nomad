## Infra Usage Collector Nomad

### How to run it

Before starting it, ensure you already have python and pip installed.

```
git clone <repo_url>
cd <dir_name>
python3 -m venv venv
```

Create config file

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
