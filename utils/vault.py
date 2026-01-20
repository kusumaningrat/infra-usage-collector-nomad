import os
import hvac

BASE_MOUNT = "secrets"


def vault_client():
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        raise RuntimeError("VAULT_ADDR or VAULT_TOKEN not set")

    client = hvac.Client(
        url=vault_addr,
        token=vault_token
    )

    if not client.is_authenticated():
        raise RuntimeError("Vault authentication failed")

    return client


def get_azure_secret():
    client = vault_client()
    secret = client.secrets.kv.v2.read_secret_version(
        path="graph-app",
        mount_point="secrets"
    )
    return secret["data"]["data"]
