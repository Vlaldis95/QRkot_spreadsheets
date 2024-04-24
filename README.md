# Проект приложение для благотворительного фонда "добрые дела для котиков"

Фонд собирает пожертвования для осуществления добрых дел в пользу братьев наших меньших - ветеринарное лечение, корм, игрушки, обустройство жилища. Это не весь список, добрых дел может быть больше! 
Отчет по закрытым сборам сохраняется в гугл таблицы автоматически!

Проект содержит модели "Пожертвования", "Пользователи", "Проекты"
В модели "Пользователи" есть разграничение прав.
В модели "Пожертвования" настроен процесс инвестирования


## Стек использованных технологий 
*  Python
*  FastApi
*  Pydantic
*  Alembic
*  SQLAlchemy
*  Google cloud platfom: Google Sheets Api, Google Drive Api

## Как запустить проект
Клонировать репозиторий к себе на компьютер

```
git clone https://github.com/Vlaldis95/cat_charity_fund
```

Создать и активировать виртуальное окружение

```
python -m venv venv

source venv/Scripts/activate
```
Обновить версию менеджера установщика пакетов и установить зависимости:

```
python -m pip install --upgrade pip

pip install -r requirements.txt
```
Необходимо создать файл .env и прописать в нем ключи:

```
APP_TITLE=Кошачий благотворительный фонд
APP_DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET
FIRST_SUPERUSER_EMAIL=admin@adm.ru
FIRST_SUPERUSER_PASSWORD=string
```
Применить миграции создав новую БД:

```
alembic upgrade head
```
Запуск проекта:
```
uvicorn app.main:app --reload
```
Документацию по API можно посмотреть по адресу:

```
http://127.0.0.1:8000/docs
```
# Чтобы добавить сохранение отчетов в Google Sheets:
Необходимо в .env прописать следующие ключи:
```
TYPE
PROJECT_ID
PRIVATE_KEY_ID
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\-----END PRIVATE KEY-----\n"
CLIENT_EMAIL
CLIENT_ID
AUTH_URI
TOKEN_URI
AUTH_PROVIDER_X509_CERT_URL
CLIENT_X509_CERT_URL
```
Далее файл необходимо заполнить согласно полученного Json ключа в Google Cloud Platform создав сервисный аккаунт. https://console.cloud.google.com/projectselector2/home/dashboard

И подключить Google Drive API и Google Sheets API.

## автор проекта:
:white_check_mark: Владислав Лукьяненко (https://github.com/Vlaldis95)
