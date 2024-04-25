from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
LIST_TITLE = 'Отчет'
ROWS = 50
COLUMS = 4
SHEETS_VER = 'v4'
DRIVE_VER = 'v3'
SPREADSHEET_BODY = {
    'properties': {'title': 'Отчет',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': LIST_TITLE,
                               'gridProperties': {'rowCount': ROWS,
                                                  'columnCount': COLUMS}}}]}

PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}