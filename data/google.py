import gspread
from oauth2client.service_account import ServiceAccountCredentials

from data.config import CREDENTIALS_FILE, spreadsheet_id

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scopes)
client = gspread.authorize(credentials)

local = {}


async def get_local_data(sheet_name: str = spreadsheet_id):
    global local
    sheet = client.open_by_key(sheet_name).get_worksheet(0)
    langs = sheet.get_all_values()[0]
    data = sheet.get_all_values()[1:]
    for x in range(len(data)):
        valiable_name = data[x][0]
        append_data = {}
        for y in range(1, len(data[x])):
            append_data[langs[y]] = data[x][y]
        local[valiable_name] = append_data