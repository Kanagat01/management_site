from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from create_bot import bot
from keyboards import *
import aiohttp


employee_id, company, fullname, surveys_for_week = '', '', '', ''


class Registration(StatesGroup):
    company = State()
    telegram_id = State()
    telegram_nickname = State()
    fullname = State()

class newFullname(StatesGroup):
    fullname = State()

class newNumOfsurveys(StatesGroup):
    surveys_for_week = State()

async def get_info(tg_id):
    objs = await send_request('employees/', data='', method='get')  
    for obj in objs: # type: ignore
        if obj['telegram_id'] == tg_id:
            global employee_id, company, fullname, surveys_for_week
            employee_id = obj['id']
            company = obj['company']
            fullname = obj['fullname']
            surveys_for_week = obj['surveys_for_week']


async def send_request(url, data, method="post"):
    url = f'http://127.0.0.1:8000/api/{url}'
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        if method == "post":
            async with session.post(url, json=data, headers=headers) as response:
                return response.status
        elif method == "put":
            async with session.put(url, json=data, headers=headers) as response:
                return response.status
        else:
            async with session.get(url, headers=headers) as response:
                return await response.json()
            

async def command_start(message: types.Message):
    greeting = "Вас приветствует бот bot_name. Здесь вы можете оценить насколько вам нравится работа в компании, а также оценить работу с коллегами."
    await bot.send_message(message.from_user.id, greeting)
    objs = await send_request('employees/', data='', method='get')
    telegram_ids = [obj['telegram_id'] for obj in objs] # type: ignore

    if message.from_user.id not in telegram_ids:
        await Registration.company.set()
        text = "Для того чтобы зарегистрироваться введите код вашей компании."
        await bot.send_message(message.from_user.id, text)
    else:
        await bot.send_message(message.from_user.id, "С возвращением!", reply_markup=kb_menu)


async def set_company(message: types.Message, state: FSMContext):
    objs = await send_request('companies/', data='', method='get')
    companies = [obj['code'] for obj in objs] # type: ignore
    try:
        if int(message.text) not in companies:
            await message.reply("Компании с таким кодом не существует! Попробуйте еще...")
        else:
            chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
            username = chat_member.user.username
            async with state.proxy() as data:
                data['company'] = message.text
                data['telegram_nickname'] = username
                data['telegram_id'] = message.from_user.id
            await Registration.next()
            await Registration.next()
            await Registration.next()
            await bot.send_message(message.from_user.id, "Теперь введите свое ФИО.")
    except:
        await message.reply("Введите число, код вашей компании!")


async def set_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    data = await state.get_data()
    status_code = await send_request('employees/', data, "post")

    if status_code in [200, 201]:
        await message.answer("Отлично, вы зарегистрированы!", reply_markup=kb_menu)
        await state.finish()
    else:
        await message.answer('Ошибка выполнения запроса. Попробуйте еще...')


async def cancel(message: types.Message):
    await bot.send_message(message.from_user.id, "Изменения отменены", reply_markup=kb_menu)


async def cancelState(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, "Изменения отменены", reply_markup=kb_menu)


async def new_name(message: types.Message):
    await get_info(message.from_user.id)
    await newFullname.fullname.set()
    await bot.send_message(message.from_user.id, f"Ваше ФИО {fullname}. Введите новое ФИО", reply_markup=kb_cancel)


async def save_new_name(message: types.Message, state: FSMContext):
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    username = chat_member.user.username
    async with state.proxy() as data:
        data['fullname'] = message.text

    data1 = await state.get_data()
    data2 = {
        'company': company,
        'telegram_nickname': username,
        'telegram_id': message.from_user.id
    }
    data = data1 | data2
    status_code = await send_request(f'employees/{employee_id}/', data, "put")
    if status_code in [200, 201]:
        await message.answer(f"Новое ФИО {message.text} сохранено", reply_markup=kb_menu)
        await state.finish()
    else:
        await message.answer(f"{status_code} Что-то пошло не так! Попробуйте еще...", reply_markup=kb_cancel)


async def num_of_surveys(message: types.Message):
    await get_info(message.from_user.id)
    await newNumOfsurveys.surveys_for_week.set()
    await message.answer(f"Количество опросов: {surveys_for_week}. Введите новое количство(от 1 до 5)", reply_markup=kb_cancel)


async def save_num_of_surveys(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5: 
        chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        username = chat_member.user.username

        async with state.proxy() as data:
            data['surveys_for_week'] = message.text

        data1 = await state.get_data()
        data2 = {
            'fullname': fullname,
            'company': company,
            'telegram_nickname': username,
            'telegram_id': message.from_user.id
        }
        data = data1 | data2
        status_code = await send_request(f'employees/{employee_id}/', data, "put")

        if status_code in [200, 201]:
            await message.answer(f"Новое количество опросов {message.text} сохранено", reply_markup=kb_menu)
            await state.finish()
        else:
            await message.answer("Что-то пошло не так! Попробуйте еще...", reply_markup=kb_cancel)
    else:
        await bot.send_message(message.from_user.id, "Введите число от 1 до 5", reply_markup=kb_cancel)


async def callback_query_handler(callback_query: CallbackQuery):
    type = callback_query.data.split('_')[1]
    evaluation = int(callback_query.data.split('_')[2])
    await get_info(callback_query.from_user.id)

    if type == 'comp':
        url = 'company_evaluation/'
        data = {'employee': callback_query.from_user.id, 'evaluation': evaluation, 'company': company}

    else:
        url = 'employee_evaluation/'
        objs = await send_request('feedback_settings/', '', "get")
        for obj in objs: # type: ignore
            if int(obj['employee2_tg_id']) == callback_query.from_user.id:
                evaluation_employee = obj['employee1_fullname']
                break
        objs = await send_request('employees/', '', "get")
        for obj in objs:  # type: ignore
            if evaluation_employee == obj['fullname']: # type: ignore
                evaluation_employee = obj['telegram_id']
                break

        
        data = {
            'evaluator': callback_query.from_user.id, 
            'evaluation_employee': evaluation_employee, # type: ignore 
            'evaluation': evaluation, 
            'company': company}

    status_code = await send_request(url, data=data, method="post")

    if status_code == 201:
        await bot.answer_callback_query(callback_query.id, text='Спасибо за вашу оценку!')
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id)
    else:
        await bot.answer_callback_query(callback_query.id, text='Не удалось сохранить вашу оценку. Попробуйте позже.')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"], state=None)
    dp.register_message_handler(set_company, state=Registration.company)
    dp.register_message_handler(set_fullname, state=Registration.fullname)
    dp.register_message_handler(cancel, Text(equals="Отмена"))
    dp.register_message_handler(cancelState, Text(equals="Отмена"), state=newFullname.fullname)
    dp.register_message_handler(cancelState, Text(equals="Отмена"), state=newNumOfsurveys.surveys_for_week)
    dp.register_message_handler(new_name, Text(equals="Изменить ФИО"), state=None)
    dp.register_message_handler(num_of_surveys, Text(equals="Изменить количество опросов в неделю\n(от 1 до 5)"), state=None)
    dp.register_message_handler(save_new_name, state=newFullname.fullname)
    dp.register_message_handler(save_num_of_surveys, state=newNumOfsurveys.surveys_for_week)
    dp.register_callback_query_handler(callback_query_handler, lambda c: 'rate' in c.data)
