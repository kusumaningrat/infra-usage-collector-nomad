import requests, asyncio, configparser
from datetime import datetime
from utils.graph import Graph
from utils.sheet import createSheet, createTable, setTableColumns, postDataRow
from nodes.nodes import build_nodes_rows
from nomad.nomad_client import build_nomad_rows

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

        sheet_name = f"reports-{datetime.now().strftime('%Y-%m-%d')}"
        await createSheet(sheet_name, headers)

        nodes_columns = [
            "NodeName",
            "NodeIP",
            "Total CPU",
            "CPU Usage (%)",
            "Total Memory (GiB)",
            "Memory Usage (%)"
        ]

        nodes_rows = build_nodes_rows()

        nodes_table = await createTable(
            sheetName=sheet_name,
            headers=headers,
            start_row=3,
            start_col=3,
            columns=nodes_columns
        )

        await setTableColumns(nodes_table, headers, nodes_columns)
        await postDataRow(nodes_table, headers, nodes_rows)

        nomad_columns = [
            "NodeIP",
            "Nomad Node ID",
            "Status",
            "Running Allocations",
            "Nomad CPU Usage (%)",
            "Nomad Memory Usage (%)"
        ]

        nomad_rows = build_nomad_rows()

        nomad_table = await createTable(
            sheetName=sheet_name,
            headers=headers,
            start_row=len(nodes_rows) + 6,  # spacing
            start_col=3,
            columns=nomad_columns
        )

        await setTableColumns(nomad_table, headers, nomad_columns)
        await postDataRow(nomad_table, headers, nomad_rows)

    finally:
        await graph.client_credential.close()


asyncio.run(main())
