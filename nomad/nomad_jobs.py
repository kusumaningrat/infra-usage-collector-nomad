from utils.prom_client import promeConnect
import os, configparser
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

env = load_dotenv('.env')
PROME_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


config = configparser.ConfigParser()
config.read(['query.cfg'])

# query config
nomad_cluster_config = config['nomad_job']

end_time = datetime.now()
start_time = end_time - timedelta(days=15)

def getJobsSummary():
    prom = promeConnect(PROME_URL)

    queries = {
        "running": nomad_cluster_config.get('nomad_job_running_summary'),
        "failed": nomad_cluster_config.get('nomad_job_failed_summary'),
        "completed": nomad_cluster_config.get('nomad_job_complete_summary'),
        "starting": nomad_cluster_config.get('nomad_job_starting_summary')
    }

    allocations_dict = {}

    for status, query in queries.items():
        result = prom.custom_query(query)

        for res in result:
            metric = res['metric']
            instance = metric['instance'].split(':')[0]
            job_name = metric['exported_job']
            task_group = metric['task_group']
            namespace = metric['namespace']
            value = res['value'][1]

            key = (instance, job_name, task_group, namespace)

            if key not in allocations_dict:
                allocations_dict[key] = {
                    "job_name": job_name,
                    "task_group": task_group,
                    "namespace": namespace,
                    "running": 0,
                    "completed": 0,
                    "failed": 0,
                    "starting": 0
                }

            allocations_dict[key][status] = value

    jobs_allocations = list(allocations_dict.values())
    return jobs_allocations



def build_job_rows():
    jobs = getJobsSummary()

    rows = []

    for job in jobs:
        row = [
            job["job_name"],
            job["task_group"],
            job["namespace"],
            job["running"],
            job["completed"],
            job["failed"],
            job["starting"]
        ]
        rows.append(row)

    return rows