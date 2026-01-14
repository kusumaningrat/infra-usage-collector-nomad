from prometheus_api_client import PrometheusConnect
import os

PROME_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


def promeConnect(prome_url):
    prom  = PrometheusConnect(
        url=prome_url,
        disable_ssl=True
    )

    return prom