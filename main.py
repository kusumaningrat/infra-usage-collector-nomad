import requests, asyncio, configparser
from datetime import datetime
from graph import Graph
from sheet import createSheet, createTable, adjustTableColumn, postDataRow
from nodes import getNodesDetail, getTotalCPUCore, getTotalCPUUsagePerNodes, getTotalMemoryinBytes, getTotalMemoryUsagePerNodes

config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])

# Azure settings
azure_settings = config['azure']
graph: Graph = Graph(azure_settings)

async def init(graph: Graph):
    token = await graph.get_app_only_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

async def main():
    graph = Graph(azure_settings)
    try:
        headers = await init(graph)
        # print(headers)

        generated_sheet = f"reports-{datetime.now().strftime("%Y-%m-%d")}"

        rows = []

        nodes = getNodesDetail()
        cpu_total = getTotalCPUCore()
        cpu_usage = getTotalCPUUsagePerNodes()
        mem_total = getTotalMemoryinBytes()
        mem_usage = getTotalMemoryUsagePerNodes()
        
        for node_ip, nodename in nodes.items():
            rows.append([
                nodename,
                node_ip,
                cpu_total.get(node_ip, 0),
                cpu_usage.get(node_ip, 0),
                mem_total.get(node_ip, 0),
                mem_usage.get(node_ip, 0)
            ])


        # Create sheet
        await createSheet(generated_sheet, headers)

        # Create table
        tableName = await createTable(generated_sheet, headers)

        # Adjust table column
        await adjustTableColumn(tableName, headers)

        # Create row data
        await postDataRow(tableName, headers, rows)

    finally:
        await graph.client_credential.close()


asyncio.run(main())
