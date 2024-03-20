import asyncio

import gspread
from oauth2client.service_account import ServiceAccountCredentials


async def update_google_sheet(cell: str, value: str):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open("users_counter")
    worksheet = spreadsheet.sheet1

    await asyncio.to_thread(worksheet.update, cell, [[value]])
