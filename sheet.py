import requests, asyncio, configparser
from datetime import datetime
from graph import Graph




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

async def createTable(sheetName, headers):
    graph = Graph(azure_settings)
    # Create Table
    try:
        table = requests.post(
            f"{base_url}/workbook/worksheets/{sheetName}/tables/add",
            headers=headers,
            json={
                "address": "C3:F3", 
                "hasHeaders": True,
                }
        )
        tables = table.json()
        table_name = tables['name']
        print(f"Successfully create table: {table_name}")
        return table_name
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()

async def adjustTableColumn(tableName, headers):
    graph = Graph(azure_settings)
    # Adjust table column
    try:
        requests.patch(
                f"{base_url}/workbook/tables/{tableName}/headerRowRange",
                headers=headers,
                json={
                    "values": [["Date", "adasd", "asd", "Status"]]
                }
            )
        print("Successfully adjust the table column")
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()

async def postDataRow(tableName, headers, datas = []):
    graph = Graph(azure_settings)
    # Adjust table column
    try:
        data = requests.post(
            f"{base_url}/workbook/tables/{tableName}/rows/add",
            headers=headers,
            json={
                "values": [
                    datas
                ]
            }
        )
        print(f"Successfully add data: {data}")
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()