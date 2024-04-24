from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

DATETIME_NOW = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
FILE_TITLE = f'Отчет от {DATETIME_NOW}'
LIST_TITLE = 'Отчет'
ROWS = 50
COLUMS = 4
SHEETS_VER = 'v4'
DRIVE_VER = 'v3'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    spreadsheet_body = {
        'properties': {'title': FILE_TITLE,
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': LIST_TITLE,
                                   'gridProperties': {'rowCount': ROWS,
                                                      'columnCount': COLUMS}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', DRIVE_VER)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', SHEETS_VER)

    table_values = [
        ['Дата отчета', DATETIME_NOW],
        ['Рейтинг проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for object in projects:
        new_row = [
            object.name,
            str(object.close_date - object.create_date),
            object.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E50',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )