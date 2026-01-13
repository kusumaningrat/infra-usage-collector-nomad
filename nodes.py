from prom_client import promeConnect
import os, configparser
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd

env = load_dotenv('.env')
PROME_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


config = configparser.ConfigParser()
config.read(['query.cfg'])

# query config
node_query_config = config['nodes']

end_time = datetime.now()
start_time = end_time - timedelta(days=15)

def getNodesDetail():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('nodes_detail')
    result = prom.custom_query(query)

    nodes = {}

    for res in result:
        node_ip = res['metric']['instance'].split(':')[0]
        nodename = res['metric']['nodename']
        nodes[node_ip] = nodename

    return nodes

def getTotalCPUCore():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('total_cpu_core')
    result = prom.custom_query(query)

    total_cpu = {}

    for res in result:
        node_ip = res['metric']['instance'].split(':')[0]
        total_core = res['value'][1]
        total_cpu[node_ip] = total_core

    return total_cpu

def getTotalCPUUsagePerNodes():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('cpu_usage_per_node')
    result = prom.custom_query_range(
        query,
        start_time=start_time,
        end_time=end_time,
        step='1h'
    )

    cpu_usage = {}

    for res in result:
        # cpu_percentages = [round(float(v[1]), 2) for v in res['values']]
        node_ip = res['metric']['instance'].split(':')[0]
        cpu_percentage = round(float(res['values'][0][1]), 2)
        cpu_usage[node_ip] = cpu_percentage

    return cpu_usage

def getTotalMemoryGiB():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('total_memory_size')
    result = prom.custom_query(query)

    memory_total = {}

    for res in result:
        node_ip = res['metric']['instance'].split(':')[0]
        memory_in_gib = float(res['value'][1]) / 1024**3
        memory_total[node_ip] = round(memory_in_gib)

    return memory_total
    
def getTotalMemoryUsagePerNodes():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('memory_usage_per_node')
    result = prom.custom_query(query)

    memory_usage = {}

    for res in result:
        node_ip = res['metric']['instance'].split(':')[0]
        total_memory = res['value'][1]
        memory_percentage = round(float(total_memory), 2)
        memory_usage[node_ip] = memory_percentage

    return memory_usage
        
getTotalMemoryGiB()