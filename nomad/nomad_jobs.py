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
nomad_cluster_config = config['nomad_job']

end_time = datetime.now()
start_time = end_time - timedelta(days=15)

def getRunningJobsAllocations():
    prom = promeConnect(PROME_URL)
    query = nomad_cluster_config.get('nomad_job_running_summary')
    result = prom.custom_query(query)

    jobs_allocations = {}

    print(result)
    
    # for res in result:
        # print(res)
        # instance = res['metric']['instance'].split(':')[0]
        # node_id = res['metric']['node_id']
        # node_status = res['metric']['node_status']
        # jobs_allocations[instance] = {
        #     "node_id": node_id,
        #     "status": node_status
        # }

    # print(jobs_allocations)
    # return jobs_allocations


getRunningJobsAllocations()
