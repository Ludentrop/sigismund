import os

from sheets_connection import auth, get_data

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils import executor
from sigismund import bot, dp
from const import *


scheduler = AsyncIOScheduler()


def connect_to_sheets():
    try:
        creds = auth()
        row = get_data(creds)
    except Exception:
        row = 0

    return row


def update(date):
    with open('date.txt', 'w+') as file:
        last_date = file.read()

        if date != last_date.strip():
            file.write(date)

            return 1
        return 0


def create_message():
    data = connect_to_sheets()

    date = data[0]

    if update(date):
        new_order = f'{data[1]} {data[2]}, {data[3]}\n\n{data[4]}\n\nHave you ever worked with a therapist: {data[5]}\nEmail: {data[6]}'
    else:
        new_order = 'Google is limiting!'

    return new_order


text = create_message()


async def send_message_to_groups():
    await bot.send_message(chat_id=chat_id, text=text)


def schedule_jobs():
    scheduler.add_job(send_message_to_groups, 'interval', seconds=15)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=schedule_jobs())
