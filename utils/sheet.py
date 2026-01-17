import requests, asyncio, configparser
from datetime import datetime
from utils.graph import Graph

config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])

# Azure settings
azure_settings = config['azure']

# Sheet details
sheet_details = config['sheet']
site_id = sheet_details.get('site_id')
item_id = sheet_details.get('item_id')

# Base url builder
base_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{item_id}"

graph: Graph = Graph(azure_settings)

async def init(graph: Graph):
    token = await graph.get_app_only_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
async def listWorksheets(headers):
    graph = Graph(azure_settings)

    # List Worksheet
    try:
        res = requests.get(
            f"{base_url}/workbook/worksheets",
            headers=headers,
        )
        data = res.json()
        return [sheet["name"] for sheet in data.get("value", [])]
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()


async def createSheet(sheetName, headers):
    graph = Graph(azure_settings)
    # Create Worksheet
    try:
        requests.post(
            f"{base_url}/workbook/worksheets",
            headers=headers,
            json={"Name": sheetName}
        )
        print(f"Successfully create sheet with name: {sheetName}")
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()

def excel_col(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

async def createTable(sheetName, headers, start_row, start_col, columns):
    graph = Graph(azure_settings)
    # Create Table
    try:
        col_count = len(columns)
        end_col = excel_col(start_col + col_count - 1)

        address = f"{excel_col(start_col)}{start_row}:{end_col}{start_row}"

        res = requests.post(
            f"{base_url}/workbook/worksheets/{sheetName}/tables/add",
            headers=headers,
            json={
                "address": address,
                "hasHeaders": True
            }
        )

        return res.json()["name"]
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()

async def setTableColumns(tableName, headers, columns):
    graph = Graph(azure_settings)
    # Adjust table column
    try:
        requests.patch(
            f"{base_url}/workbook/tables/{tableName}/headerRowRange",
            headers=headers,
            json={"values": [columns]}
        )
        print("Successfully adjust the table column")
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()

async def postDataRow(tableName, headers, rows):
    graph = Graph(azure_settings)
    # Adjust table column
    try:
        data = requests.post(
            f"{base_url}/workbook/tables/{tableName}/rows/add",
            headers=headers,
            json={
                "values": rows
            }
        )
        print(f"Successfully add data")
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()