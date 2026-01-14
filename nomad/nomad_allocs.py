from utils.prom_client import promeConnect
import os, configparser
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
from utils.convert_bytes import readable_bytes

env = load_dotenv('.env')
PROME_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


config = configparser.ConfigParser()
config.read(['query.cfg'])

# query config
nomad_allocs_config = config['nomad_allocs']

end_time = datetime.now()
start_time = end_time - timedelta(days=15)

def getAllocsCPUAllocated():
    prom = promeConnect(PROME_URL)
    query = nomad_allocs_config.get('nomad_allocs_cpu_allocated')
    result = prom.custom_query(query)

    cpu_allocs = []

    for res in result:
        metric = res['metric']
        instance = metric['instance'].split(':')[0]
        job_name = metric['exported_job']
        task_group = metric['task_group']
        task_name = metric['task']
        namespace = metric['namespace']
        alloc_id = metric['alloc_id']
        cpu_allocated = res['value'][1]

        cpu_allocs.append(
            [instance,
            job_name,
            task_group,
            task_name,
            namespace,
            alloc_id,
            cpu_allocated]
        )

    return cpu_allocs

def getAllocsMemoryAllocated():
    prom = promeConnect(PROME_URL)
    query = nomad_allocs_config.get('nomad_allocs_memory_allocated')
    result = prom.custom_query(query)

    memory_allocs = {}

    for res in result:
        # print(res)
        metric = res['metric']
        instance = metric['instance'].split(':')[0]
        memory_allocated = int(res['value'][1])
        memory_allocated = readable_bytes(memory_allocated)
        memory_allocs[instance] = memory_allocated

    # print(memory_allocs)
    return memory_allocs


def build_allocs_rows():
    allocs = getAllocsCPUAllocated()
    memory_alloc = getAllocsMemoryAllocated()

    rows = []

    for alloc in allocs:
        instance = alloc[0]
        job_name = alloc[1]
        task_group = alloc[2]
        task_name = alloc[3]
        namespace = alloc[4]
        alloc_id = alloc[5]
        cpu_allocated = alloc[6]
        mem_allocated = memory_alloc.get(instance, "N/A")

        # print(mem_allocated)

        row = [
            instance,
            job_name,
            task_group,
            task_name,
            namespace,
            alloc_id,
            cpu_allocated,
            mem_allocated
        ]

        rows.append(row)

    return rows