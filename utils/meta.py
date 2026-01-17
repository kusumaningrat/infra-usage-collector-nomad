from utils.sheet import listWorksheets

async def build_meta_rows(headers):
    sheets = await listWorksheets(headers)
    rows = []

    for sheet in sheets:
        # print(sheet)
        if sheet.startswith("Reports"):
            rows.append([sheet])

    return rows