from utils.prom_client import promeConnect
import os, configparser
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd

env = load_dotenv('.env')
PROME_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


config = configparser.ConfigParser()
config.read(['query.cfg'])

# query config
nomad_cluster_config = config['nomad_cluster']

end_time = datetime.now()
start_time = end_time - timedelta(days=15)

def getNomadClientsDetail():
    prom = promeConnect(PROME_URL)
    query = nomad_cluster_config.get('nomad_client_details')
    result = prom.custom_query(query)

    nomad_clients_detail = {}
    
    for res in result:
        instance = res['metric']['instance'].split(':')[0]
        node_id = res['metric']['node_id']
        node_status = res['metric']['node_status']
        nomad_clients_detail[instance] = {
            "node_id": node_id,
            "status": node_status
        }

    return nomad_clients_detail

def getNomadAllocations():
    prom = promeConnect(PROME_URL)
    query = nomad_cluster_config.get('nomad_client_allocations')
    result = prom.custom_query(query)

    running_allocations = {}
    
    for res in result:
        instance = res['metric']['instance'].split(':')[0]
        running_allocations_per_node = res['value'][1]
        running_allocations[instance] = running_allocations_per_node

    print(running_allocations)
    return running_allocations

def getNomadCPUUsagePerNode():
    prom = promeConnect(PROME_URL)
    query = nomad_cluster_config.get('nomad_client_cpu_usage')
    result = prom.custom_query(query)

    nomad_cpu_usage = {}
    
    for res in result:
        instance = res['metric']['instance'].split(':')[0]
        nomad_cpu_usage_per_node = res['value'][1]
        nomad_cpu_usage[instance] = nomad_cpu_usage_per_node

    return nomad_cpu_usage

def getNomadMemoryUsagePerNode():
    prom = promeConnect(PROME_URL)
    query = nomad_cluster_config.get('nomad_client_memory_usage')
    result = prom.custom_query(query)

    nomad_memory_usage = {}
    
    for res in result:
        instance = res['metric']['instance'].split(':')[0]
        nomad_memory_usage_per_node = round(float(res['value'][1]), 2)
        nomad_memory_usage[instance] = nomad_memory_usage_per_node

    return nomad_memory_usage

def build_nomad_rows():
    details = getNomadClientsDetail()
    allocs = getNomadAllocations()
    cpu = getNomadCPUUsagePerNode()
    memory = getNomadMemoryUsagePerNode()

    rows = []

    for node_ip, meta in details.items():
        rows.append([
            node_ip,
            meta["node_id"],
            meta["status"],
            allocs.get(node_ip, 0),
            round(float(cpu.get(node_ip, 0)), 2),
            memory.get(node_ip, 0)
        ])

    return rows
