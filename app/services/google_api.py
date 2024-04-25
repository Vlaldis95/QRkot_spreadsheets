from datetime import datetime

from aiogoogle import Aiogoogle

from .constants import (DRIVE_VER, FORMAT, PERMISSIONS_BODY, SHEETS_VER,
                        SPREADSHEET_BODY)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = PERMISSIONS_BODY
    service = await wrapper_services.discover('drive', DRIVE_VER)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    datetime_now = datetime.now().strftime(FORMAT)
    table_values = [
        ['Дата отчета', datetime_now],
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
            spreadsheetId=spreadsheet_id,
            range='A1:E50',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
