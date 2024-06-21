import asyncio
import datetime
import json
import os
from aiofiles import open as async_open
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = './services/optimum-spring-405211-066ddb81ace7.json'

    def __init__(self, dir, calendar_id):
        self.calendar_id = calendar_id
        self.dir = str(dir)

        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH, scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=credentials)

    async def find_newest_file(self):
        print('Вошли в функцию find_newest_file класса GoogleCalendar')
        folder_path = os.path.join('.', 'users_data', self.dir, 'json_calendar')
        print(folder_path)
        newest_file = None
        max_creation_time = 0
        json_list = list()

        for file_name in os.listdir(path=folder_path):
            file_path = os.path.join(folder_path, file_name)
            creation_time = os.path.getctime(file_path)
            if creation_time > max_creation_time:
                max_creation_time = creation_time
                newest_file = file_path
        print(f'Найден файл {newest_file} для {self.dir}')
        return newest_file

    async def find_max_and_min_time(self):
        newest_file = await self.find_newest_file()
        if newest_file is None:
            return None
        max_time = datetime.datetime.strptime('0001-01-01T00:00:00+05:00', "%Y-%m-%dT%H:%M:%S%z")
        min_time = datetime.datetime.strptime('9999-12-31T23:59:59+05:00', "%Y-%m-%dT%H:%M:%S%z")
        async with async_open(newest_file, 'r', encoding='utf-8') as file:
            json_string = await file.read()

            json_schedule = json.loads(json_string)
        for i in json_schedule:
            min_time = min(min_time, datetime.datetime.strptime(i['start']['dateTime'], "%Y-%m-%dT%H:%M:%S%z"))
            max_time = max(max_time, datetime.datetime.strptime(i['end']['dateTime'], "%Y-%m-%dT%H:%M:%S%z"))

        return min_time.isoformat('T'), max_time.isoformat('T')

    async def print_newest_json(self):
        newest_file = await self.find_newest_file()
        print(newest_file)
        async with async_open(newest_file, 'r', encoding='utf-8') as file:
            json_string = await file.read()

            json_schedule = json.loads(json_string)

        for i in json_schedule:
            print(i)

    async def add_event(self, event):
        return self.service.events().insert(calendarId=self.calendar_id, body=event).execute()

    async def add_events(self):
        newest_file = await self.find_newest_file()

        async with async_open(newest_file, 'r', encoding='utf-8') as file:
            json_string = await file.read()
            json_schedule = json.loads(json_string)

        for i in json_schedule:
            await self.add_event(i)
            print(f'Добавлено {i["summary"]} для {self.dir}')

    async def get_events(self, timemin, timemax):
        events = self.service.events().list(calendarId=self.calendar_id,
                                            timeMin=timemin,
                                            timeMax=timemax).execute()
        return events

    async def delete_events(self, timemin, timemax):
        events = await self.get_events(timemin, timemax)
        print('Найдены эвенты, ща удаляться будут')
        for event in events['items']:
            event_summary = event['summary']
            self.service.events().delete(calendarId=self.calendar_id, eventId=event['id']).execute()
            print(f'Удалено мероприятие {event_summary} для {self.dir}')
