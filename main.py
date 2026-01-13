import requests, asyncio, configparser
from datetime import datetime
from graph import Graph

site_id = "1fa7f76c-05a1-4781-afe1-151e983cfa90,396378f0-8843-431d-9b1b-17e4446766f0"
item_id = "01HZMN5BRTE5RUNY6F3FA3M2BTMFGUCCYK"
base_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{item_id}"



# Create table
# requests.post(
#     f"{base_url}/workbook/worksheets/Sheet1/tables/add",
#     headers=headers,
#     json={"address": "A10:D0", "hasHeaders": True}
# )

# # Add rows
# requests.post(
#     f"{base_url}/workbook/tables/Table1/rows/add",
#     headers=headers,
#     json={
#         "values": [
#             ["2026-01-12", "api-gateway", 72, "OK"]
#         ]
#     }
# )

config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])
azure_settings = config['azure']

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

async def postDataRow(tableName, headers):
    graph = Graph(azure_settings)
    # Adjust table column
    try:
        data = requests.post(
            f"{base_url}/workbook/tables/{tableName}/rows/add",
            headers=headers,
            json={
                "values": [
                    ["2026-01-12", "api-gateway", 72, "OK"]
                ]
            }
        )
        print(f"Successfully add data: {data}")
    except Exception as e:
        print("Error:", e)
    finally:
        await graph.client_credential.close()


async def main():
    graph = Graph(azure_settings)
    try:
        headers = await init(graph)
        # print(headers)

        generated_sheet = f"reports-{datetime.now().strftime("%Y-%m-%d")}"

        # Create sheet
        await createSheet(generated_sheet, headers)

        # Create table
        tableName = await createTable(generated_sheet, headers)

        # Adjust table column
        await adjustTableColumn(tableName, headers)

        # Create row data
        await postDataRow(tableName, headers)

    finally:
        await graph.client_credential.close()


asyncio.run(main())
