from utils.sheet import listWorksheets

async def build_meta_rows(headers):
    sheets = await listWorksheets(headers)
    rows = []

    for sheet_name in sheets:
        if sheet_name.startswith("Reports"):
            rows.append([sheet_name])

    return rows