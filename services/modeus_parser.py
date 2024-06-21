import asyncio
import datetime
import time

from fake_useragent import UserAgent
import os
import json
from aiofiles import open as async_open
from playwright.async_api import async_playwright, Playwright, expect


class Parser:
    def __init__(self, dir, user_login, user_password):
        self.dir = str(dir)
        self.user_login = user_login
        self.user_password = user_password

    @staticmethod
    async def modeus_time_to_google_time(string: str):
        return f'{string[0:4]}-{string[4:6]}-{string[6:11]}:{string[11:13]}:{string[13:]}+05:00'

    async def get_data_selen(self):
        try:
            async with async_playwright() as playwright:
                chromium = playwright.chromium
                browser = await chromium.launch(headless=False, timeout=60000)
                url = 'https://utmn.modeus.org/'
                page = await browser.new_page(user_agent=UserAgent().random)
                page.set_default_timeout(50_000)
                
                await page.goto(url)
                print('Главная страница')
                await page.get_by_placeholder("proverka@example.com").fill(self.user_login)
                await page.get_by_placeholder("Пароль").fill(self.user_password)
                await page.get_by_role("button", name='Вход').click()
                print('Заходим в личный кабинет')
                download_button = page.locator(
                    'body > app-root > modeus-root > div > div > mds-schedule-calendar-display > div > div > div > div > div > div > div.main-calendar-form.screen-only > div:nth-child(5) > button')
                await download_button.wait_for(state='visible')
                async with page.expect_download() as download_info:
                    time.sleep(2)
                    if await download_button.is_disabled():
                        await browser.close()
                    await download_button.click()

                download = await download_info.value
                p = os.path.join('.', 'users_data', self.dir, 'modeus_calendar/')
                print(p)
                await download.save_as(p + download.suggested_filename)
        except Exception as e:
            print(f'Ошибка {e}')
        finally:
            await browser.close()

    async def find_newest_file(self):
        print("Current working directory:", os.getcwd())
        folder_path = os.path.join('.', 'users_data', self.dir, 'modeus_calendar')
        print(folder_path)
        newest_file = None
        max_creation_time = 0
        print(f'Нашли папку для {self.dir}')
        for file_name in os.listdir(path=folder_path):
            file_path = os.path.join(folder_path, file_name)
            creation_time = os.path.getctime(file_path)
            if creation_time > max_creation_time:
                max_creation_time = creation_time
                newest_file = file_path
        print(f'Нашли файл {self.dir} - {newest_file}')
        return newest_file

    async def parsing_file(self):
        print(f'Зашли в функцию parsing_file для {self.dir}')
        newest_file = await self.find_newest_file()
        if newest_file is None:
            return False
        json_list = list()
        async with async_open(newest_file, 'r', encoding='utf-8') as file:
            print(f'Открыли файл {newest_file} для {self.dir}')
            temp_dict = {}

            for i in await file.readlines():
                if i.startswith('DTSTART'):
                    temp_dict['start'] = {
                        'dateTime': await Parser.modeus_time_to_google_time(' '.join(i[-16:].split()))
                    }

                elif i.startswith('DTEND'):
                    temp_dict['end'] = {
                        'dateTime': await Parser.modeus_time_to_google_time(' '.join(i[-16:].split()))
                    }

                elif i.startswith('SUMMARY'):
                    temp_dict['summary'] = (' '.join(i[8:].split()))
                elif i.startswith('LOCATION'):
                    temp_dict['location'] = (' '.join(i[9:].split()))
                elif i.startswith('DESCRIPTION'):
                    raw_string = ' '.join(i[12:i.find('Посмотреть') - 4].split())
                    finally_string = str()
                    for i in raw_string:
                        if i not in {"\\", 'n'}:
                            finally_string += i
                    temp_dict['description'] = finally_string
                if len(temp_dict) == 5:
                    json_list.append(temp_dict.copy())
                    temp_dict.clear()

        f = os.path.join('.', 'users_data', self.dir, 'json_calendar', datetime.datetime.now().strftime("%H_%M_%S") + '.json')
        print(f)
        async with async_open(f, 'w', encoding='utf-8') as file:
            await file.write(json.dumps(json_list))

        print(f'Json файл сохранен для {self.dir}')
        return True

