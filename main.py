import requests, asyncio, configparser
from datetime import datetime
from utils.graph import Graph
from utils.sheet import createSheet, createTable, setTableColumns, postDataRow, listWorksheets
from nodes.nodes import build_nodes_rows
from nomad.nomad_client import build_nomad_rows
from nomad.nomad_jobs import build_job_rows
from nomad.nomad_allocs import build_allocs_rows
from utils.meta import build_meta_rows
from dotenv import load_dotenv

from utils.vault import get_azure_secret

load_dotenv()

# Load config files (non-secret)
config = configparser.ConfigParser()
config.read(["config.cfg", "config.dev.cfg"])


async def init(graph: Graph):
    token = await graph.get_app_only_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

async def main():
    azure_secrets = get_azure_secret()

    # Init Graph client
    graph = Graph(azure_secrets)
    try:
        headers = await init(graph)
        # print(headers)

        sheet_name = f"Reports_{datetime.now().strftime('%Y_%m_%d')}"
        meta_sheet = "meta"

        await createSheet(sheet_name, headers)
        await createSheet(meta_sheet, headers)


        meta_column = [
            "Report",
        ]


        meta_rows = await build_meta_rows(headers)

        meta_tables = await createTable(
            sheetName=meta_sheet,
            headers=headers,
            start_row=1,
            start_col=1,
            columns=meta_column
        )

        await setTableColumns(meta_tables, headers, meta_column)
        await postDataRow(meta_tables, headers, meta_rows)


        # Nodes Detail
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


        # Nomad Clients
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

        # Nomad Clients
        jobs_column = [
            "Job Name",
            "Task Group",
            "Namespace",
            "Running",
            "Completed",
            "Failed",
            "Starting"
        ]

        job_rows = build_job_rows()

        jobs_table = await createTable(
            sheetName=sheet_name,
            headers=headers,
            start_row=3,  # spacing
            start_col=12,
            columns=jobs_column
        )

        await setTableColumns(jobs_table, headers, jobs_column)
        await postDataRow(jobs_table, headers, job_rows)

        # Allocations
        allocations_column = [
            "Instance",
            "Job Name",
            "Group Name",
            "Task Name",
            "Namespace",
            "Allocations ID",
            "CPU",
            "Memory"
        ]

        allocation_rows = build_allocs_rows()

        allocs_tables = await createTable(
            sheetName=sheet_name,
            headers=headers,
            start_row=3,
            start_col=21,
            columns=allocations_column
        )

        await setTableColumns(allocs_tables, headers, allocations_column)
        await postDataRow(allocs_tables, headers, allocation_rows)


    finally:
        await graph.client_credential.close()


asyncio.run(main())
