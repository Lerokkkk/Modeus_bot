# Modeus_bot
Modeus bot is a bot that takes scheduling data from the modeus site and provides it to the user in Google Calendar using the Telegram bot and GoogleApi

# Technologies Used:
- Aiogram - Asynchronous framework for Telegram Bot API
- Google API - Programmatic interfaces to Google Cloud Platform services
- SQLAlchemy - The Python SQL Toolkit and Object Relational Mapper
- Alembic - The lightweight database migration tool for usage
- Playwright - Used as a general purpose browser automation tool
- Asyncpg - An efficient, clean implementation of PostgreSQL server binary protocol for use with Python’s asyncio framework
# Installation:
## 1. Cloning a repository
`https://github.com/Lerokkkk/Modeus_bot.git`

`cd Modeus_bot`
## 2. Create Virtual Environment:
`python -m venv venv`
## 3. Activate Virtual Environment:
`venv\Scripts\activate`
## 4.Install Dependcies:
`pip install -r requirements.txt`
## 5. Run Migrations:
`alembic upgrade head`
## 6. Add .env and optimus-spring files
check .env-example and optimus-spring-example files
## 7. Run bot:
`python bot.py`

# Usage:
- Send "**/start**" to bot
- **Copy** link from bot and **paste** to Google Calendar settings
- Click on "**Ввести данные от Google Calendar**" button and send link from your Google Calendar
- Click on "**Ввести данные от Modeus**" button and send login and password from your Modeus account
- Click on "**Обновить пары**" button and check your Google Calendar
