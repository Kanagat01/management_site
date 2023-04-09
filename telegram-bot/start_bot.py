from aiogram.utils import executor
from create_bot import dp, bot
from keyboards import kb_rate_comp, kb_rate_colleague
from handlers import register_handlers
from datetime import datetime
import aiohttp
import schedule
import asyncio
import tracemalloc


base_url = 'http://skanagat101.pythonanywhere.com'  # 'http://127.0.0.1:8000'


async def get_company_feedback():
    weekday = datetime.now().weekday()

    if weekday in [0, 1, 2, 3, 4]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{base_url}/api/employees/') as response:
                if response.status == 200:
                    employees = await response.json()
                    for employee in employees:
                        if employee['surveys_for_week'] - 1 >= weekday:
                            await bot.send_message(int(employee['telegram_id']), f'Как вы оцениваете ваш рабочий день сегодня ?', reply_markup=kb_rate_comp)


async def get_colleague_feedback():
    weekday = datetime.now().weekday()
    day = datetime.today().day
    week_lst = [range(1, 8), range(1, 15), range(1, 22), range(1, 29)]

    if weekday == 2:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{base_url}/api/feedback_settings/') as response:
                if response.status == 200:
                    objs = await response.json()
                    for obj in objs:
                        if day in week_lst[obj['surveys_for_month'] - 1]:
                            await bot.send_message(int(obj['employee2_tg_id']), f"Как вы оцениваете свою работу с коллегой {obj['employee1_fullname']} ?", reply_markup=kb_rate_colleague)


async def on_startup(_):
    print("Бот вышел в онлайн")

    schedule.every().day.at("17:00").do(
        lambda: asyncio.create_task(get_company_feedback()))
    schedule.every().day.at("17:00").do(
        lambda: asyncio.create_task(get_colleague_feedback()))

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    register_handlers(dp)
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup(None))
    tracemalloc.start()
    executor.start_polling(dp, loop=loop)
