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


    for res in result:
        node_ip = res['metric']['instance'].split(':')[0]
        nodename = res['metric']['nodename']

    return node_ip, nodename

def getTotalCPUCore():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('total_cpu_core')
    result = prom.custom_query(query)


    for res in result:
        node_ip = res['metric']['instance'].split(':')[0]
        total_core = res['value'][1]

    return node_ip, total_core

def getTotalCPUUsagePerNodes():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('cpu_usage_per_node')
    result = prom.custom_query_range(
        query,
        start_time=start_time,
        end_time=end_time,
        step='1h'
    )

    # print(result)

    for res in result:
        # cpu_percentages = [round(float(v[1]), 2) for v in res['values']]
        cpu_percentage = round(float(res['values'][0][1]), 2)

    return cpu_percentage

def getTotalMemoryinBytes():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('total_memory_size')
    result = prom.custom_query(query)

    for res in result:
        total_memory = res['value'][1]
        memory_in_gib = round(float(int(total_memory) / 1024 / 1024 / 1024), 2 )
        return memory_in_gib
    
def getTotalMemoryUsagePerNodes():
    prom = promeConnect(PROME_URL)
    query = node_query_config.get('memory_usage_per_node')
    result = prom.custom_query(query)

    for res in result:
        print(res)
        total_memory = res['value'][1]
        memory_percentage = round(float(total_memory), 2)
        return memory_percentage