# -*- coding: utf-8 -*-
import os
import asyncio
import json
import logging
import sys
import os
from os import getenv
from typing import Any, Dict, Optional, Union

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
import mysql.connector
from mysql.connector import (connection)
from mysqlx import errorcode

import AlarmCheck

s_datafile = 'data.txt'
k_userlist = 'user_list'
s_datafold = 'usersdata/'

host1 = 'ftp60.hostland.ru'
host2 = '185.26.122.60'
host3 = 'mysql60.hostland.ru'
config = {
    'user': 'host1676258',
    'password': '5c318172',  # 78pre11523
    'host': host3,
    'database': 'host1676258',
    'raise_on_warnings': True,
    'use_pure': False
}


def get_quest_link(f_num, f_id):
    quests = f'http://happystudents.online/z{f_num}.php?id={f_id}'
    if (f_num == -1):
        return -1
    return quests


def select_db(f_select):
    try:
        cnx = mysql.connector.connect(**config)
        print('succsess connect to mysql')
        select_movies_query = f_select
        with cnx.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            if (len(result) < 1):
                return -1
            for row in result:
                print(row)

            return result
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    cnx.close()


def get_db_id(f_id):
    f_sel_name = f"SELECT user_name,inviter,time FROM users2 WHERE user_id = {f_id}"
    result = select_db(f_sel_name)
    print(result)
    return result


get_db_id(49)


def get_db_quest(f_id):
    f_sel = f"SELECT vz1,vz2,vz3,vz4,vz5 FROM users2 WHERE user_id = {f_id}"
    result = select_db(f_sel)
    print(result)
    # result = get_quest_link(f_id,get_quest_num(result[0]))
    return get_quest_num(result[0])


def get_quest_num(f_qz):
    i = 1
    for q_qz in f_qz:
        if (q_qz == 0):
            return (i)
        i = i + 1
    return -1


# my_secret = os.environ['tg_token']
BOT_TOKEN = '5987762240:AAEJL7mIvrjhkCCsCZceMopE0d_W5T5OS-s'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

lang_ru = {
    'txt_lang': '🇷🇺RUS🇷🇺',
    'txt_input_id': 'Укажите свой ID от Бизнес воронки Happy Students',
    'txt_home': 'Здравствуйте, ',
    'txt_make_compet': 'Вы в данное время находитесь на этапе выполнения задания N. Чем быстрее выполните, тем быстрее у Вас не только создаётся автоматизированный, постоянно растущий бизнес, а также обеспечивается автоматический рост Вашего бизнеса. Выполнение задания не так сложно, как может Вам кажется.\n Приступайте выполнению: ',
    'home_2': 'Если имеются какие проблемы, можете в любое время связаться с Вашим куратором:',
    'kurator': 'Куратор',
    'admin': 'Админ',
    'txt_set_compl': '✉️Отправить выполненное задание✉️',
    'input_comp': 'Отправьте выполненное задание сообщением сюда',
    'sumbit_comp': 'Задание отправлено куратору',
    'error_ref_not_found': 'Реферал не присоединился к боту, невозможно отправить задание здесь',
    'home_alldone': 'Вы выполнили все 5 задания. Поздравляем. У Вас уже образован постоянно, автоматические расширяющийся Бизнес с возможностью дополнительной массовой рекламы любого Вашего ресурса. Ваш бизнес уже будет расширяться и количество Ваших покупателей будут постоянно расти, даже если Вы уже больше ничего не будете делать. Но мы предоставляем Вам еще программные средства, если хотите еще более ускорить темп роста Вашего бизнеса.\n Пожалуйста, получайте:\n http://happystudents.online/programs.zip '
}
lang_uz = {
    'txt_lang': '🇺🇿UZB🇺🇿',
    'txt_input_id': "Happy Students Business voronkasidagi o'z ID-ingizni kiriting",
    'txt_home': 'Salom ',
    'txt_make_compet': "Siz hozirda N-topshiriqni bajarish bosqichidasiz. Uni qanchalik tez bajarsangiz, shunchalik tez avtomatlashtirilgan, doimiy o‘sib borayotgan biznesni yaratibgina qolmay, balki biznesingizning avtomatik o‘sishini ham ta’minlaysiz. Vazifani bajarish siz o'ylagandek qiyin emas.\n Topshiriqni bajarishga kirishing:",
    'home_2': "Agar sizda biron bir muammo bo'lsa, istalgan vaqtda kuratoringizga murojaat qilishingiz mumkin:",
    'kurator': 'Kurator',
    'admin': 'Admin',
    'txt_set_compl': "✉️Topshiriqni jo'natish✉️",
    'input_comp': "Topshiriq N bajarilganligi haqidagi ma'lumotni ushbu chatga yuboring",
    'sumbit_comp': 'Kuratorzga yuborish!',
    'error_ref_not_found': " Ishtirokchi botga ulanmagan. Ma'lumot yuborish imkoniyati yo'q.",
    'home_alldone': "Siz barcha 5 ta vazifani bajardingiz. Tabriklaymiz. Siz allaqachon har qanday manbangizni qo'shimcha ommaviy reklama qilish imkoniyati bilan birga doimiy ravishda avtomatik ravishda kengayib borayotgan Biznesni yaratdingiz. Sizning biznesingiz doim  kengayib boradi va siz boshqa hech narsa qilmasangiz ham, mijozlaringiz soni doimiy ravishda o'sib boradi. Ammo biznesingiz rivojini yanada tezlashtirishni istasangiz, biz sizga ko'proq dasturiy vositalarni taqdim etamiz.\n Marhamat, qabul qiling:\n http://happystudents.online/programs.zip"
}
rus = 'rus'
uzb = 'uzb'
main_lang = {rus: lang_ru, uzb: lang_uz}

form_router = Router()


class Form(StatesGroup):
    ident = State()
    first_name = State()
    ref = State()
    lang = State()
    like_bots = State()
    language = State()
    chat_id = State()
    home = State()
    input_comp = State()
    admin_enter = State()
    admin_post = State()
    reg = State()


async def updateState(state, fkey, val, step):
    fchat_id = await state.get_data()
    fchat_id = s_datafold + str(fchat_id['chat_id']) + '.json'
    try:
        f = open(fchat_id, 'r')
    except FileNotFoundError as e:
        if not os.path.exists(s_datafold):
            os.mkdir(s_datafold)
        f = open(fchat_id, 'x')
        f = open(fchat_id, 'r')
    fData = False
    try:
        fData = json.load(f)
    except ValueError as e:
        print('chat data still empty')
    if (fData):
        fData[fkey] = val
    else:
        fData = {fkey: val}

    fData = json.dumps(fData)
    with open(fchat_id, "w") as my_file:
        my_file.write(fData)
        my_file.close()
    print(fData)
    if (fkey == 'lang'):
        await state.update_data(lang=val)
    if (fkey == 'ident'):
        await state.update_data(ident=val)
    if (fkey == 'first_name'):
        await state.update_data(first_name=val)
    if (fkey == 'ref'):
        await state.update_data(ref=val)
    if (fkey == 'reg'):
        await state.update_data(reg=val)
    await state.set_state(step)


async def get_chat_by_db_id(message, f_id):
    fData = False
    print('*' * 10 + '\n GET CHAT BY ID ' + str(f_id))
    try:
        f = open(s_datafile, 'r')
        fData = json.load(f)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        print('id data error')
        await message.answer('data file error')
    finally:
        f.close()
    print('data readet')
    print(fData)
    if (fData):
        for q_id in fData[k_userlist]:
            if (q_id['user_id'] == str(f_id)):
                f_refid = {'name': q_id['tg_name'],
                           'id': q_id['tg_id']}
                return f_refid
    return -1


async def send_qw_notify(f_id, f_qw):
    f_body = str(f_qw) + ' pora by vipolnit.'
    await bot.send_message(f_id, f_body)  # like this


@form_router.message(Command(commands=["home"]))
async def open_home(message, state) -> None:
    await state.set_state(Form.home)
    f_data = await state.get_data()
    try:
        f_lang = f_data['lang']
    except KeyError as e:
        await command_start(message, state)
        return
    kb = [
        [KeyboardButton(text=main_lang[f_lang]['txt_set_compl'])],
    ]
    id = f_data['ident']

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder=main_lang[f_lang]['txt_home'])
    print('id what entered')
    print(id)
    f_name = f_data['first_name']
    f_qwnum = get_db_quest(id)
    f_qwforlink = f_qwnum
    if (f_lang == 'uzb'):
        f_qwforlink = str(f_qwforlink) + 'uz'
    f_link = get_quest_link(f_qwforlink, id)
    print(f_link)
    print(message.from_user.id)
    f_refid = f_data['ref']
    f_curator = await get_chat_by_db_id(message, f_refid)
    f_admin = await get_chat_by_db_id(message, 1)

    if (f_curator == -1):
        f_curator = 'not in Telegram'
    else:
        q_name = f_curator["name"]
        q_id = f_curator["id"]
        f_curator = f"<a href='tg://user?id={q_id}'>@{q_name}</a>"
    if (f_admin == -1):
        f_admin = 'not in Telegram'
    else:
        q_name = f_admin["name"]
        q_id = f_admin["id"]
        f_admin = f"<a href='tg://user?id={q_id}'>@{q_name}</a>"
    if (f_qwnum == -1):
        f_body = main_lang[f_lang]['home_alldone']
    else:

        f_body = main_lang[f_lang]['txt_make_compet'].replace('N', str(f_qwnum)) + '\n' + f_link + '\n' + \
                 main_lang[f_lang]['home_2']
    await message.answer(main_lang[f_lang]['txt_home'] + f_name + '\n' +
                         f_body + '\n\n' +
                         main_lang[f_lang]['kurator'] + ' - ' + f_curator + '\n' +
                         main_lang[f_lang]['admin'] + ' - ' + f_admin,
                         parse_mode='HTML',
                         reply_markup=keyboard)


async def start_input_comp(message, state):
    f_data = await state.get_data()
    f_lang = f_data['lang']
    id = f_data['ident']
    f_qwnum = get_db_quest(id)
    await state.set_state(Form.input_comp)
    print('start input competition')
    f_body = main_lang[f_lang]['input_comp'].replace('N', str(f_qwnum))
    await message.answer(f_body)


@form_router.message(Command(commands=["send_competition"]))
@form_router.message(Form.home,
                     F.text.casefold() == lang_uz['txt_set_compl'].casefold())
@form_router.message(Form.home,
                     F.text.casefold() == lang_ru['txt_set_compl'].casefold())
async def command_sendcomp(message: Message, state: FSMContext) -> None:
    await start_input_comp(message, state)


@form_router.message(Form.input_comp)
async def send_competition(message: Message, state: FSMContext) -> None:
    f_data = await state.get_data()
    f_lang = f_data['lang']
    await state.set_state(Form.home)
    print('get competition:')
    print(message.text)
    resp = get_db_id(f_data['ref'])

    f_chatid = await get_chat_by_db_id(message, f_data['ref'])
    if (f_chatid == -1):
        await message.answer(main_lang[f_lang]['error_ref_not_found'])
        return
    f_body = f_data['first_name'] + 'прислал(а) вам задание на проверку:\n ' + message.text
    await bot.send_message(int(f_chatid['id']), f_body)
    await message.answer(main_lang[f_lang]['sumbit_comp'])
    return


async def chose_lang(message, state):
    print('chat data empty')
    await state.set_state(Form.lang)
    print('start')
    kb = [
        [
            KeyboardButton(text=lang_ru['txt_lang']),
            KeyboardButton(text=lang_uz['txt_lang'])
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   one_time_keyboard=True,
                                   resize_keyboard=True,
                                   input_field_placeholder="Выберите язык")
    await message.answer("Выбрать язык", reply_markup=keyboard)
    return False


def save_data(f_data):
    fData = json.dumps(f_data)
    print(fData)
    with open(s_datafile, "w") as my_file:
        my_file.write(fData)
        my_file.close()


@form_router.message(Command(commands=["start"]))
async def command_start(message: Message, state: FSMContext) -> None:
    print('start comand')
    fchat_id = message.chat.id
    message.from_user.username

    datafilename = s_datafold + str(message.chat.id) + '.json'
    print(message.chat.id)

    await state.update_data(chat_id=message.chat.id)
    try:
        with open(datafilename, "r") as f:
            fDataStr = f.read()
        fData = json.loads(fDataStr)
    except (ValueError, AttributeError, FileNotFoundError) as e:
        await chose_lang(message, state)
        return
    f.close()
    print('find chat data')
    print(fData)
    try:
        await state.update_data(lang=fData['lang'])
    except (AttributeError, KeyError) as e:
        await chose_lang(message, state)
        return
    try:
        await state.update_data(ident=fData['ident'])
        await state.update_data(ref=fData['ref'])
    except (AttributeError, KeyError) as e:
        await state.set_state(Form.ident)
        await req_id(message, state)
        return
    try:
        await state.update_data(first_name=fData['first_name'])
    except (AttributeError, KeyError) as e:
        await chose_lang(message, state)
        return
    await open_home(message, state)


async def req_id(message, state):
    f_data = await state.get_data()
    f_lang = f_data['lang']
    text = main_lang[f_lang]['txt_input_id']
    await message.reply(
        text,
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.lang,
                     F.text.casefold() == lang_ru['txt_lang'].casefold())
async def chose_rus_lang(message: Message, state: FSMContext) -> None:
    fLang = 'rus'
    print('lang ', fLang)

    await updateState(state, 'lang', fLang, Form.ident)

    await req_id(message, state)


@form_router.message(Form.lang,
                     F.text.casefold() == lang_uz['txt_lang'].casefold())
async def chose_uzb_lang(message: Message, state: FSMContext) -> None:
    fLang = 'uzb'
    print('lang ', fLang)
    await updateState(state, 'lang', fLang, Form.ident)

    await req_id(message, state)


@form_router.message(Form.ident)
async def process_read_id(message: Message, state: FSMContext) -> None:
    print('id entered: ' + message.text)
    fId = message.text
    f_name = get_db_id(fId)
    print('get name from db')
    print(f_name)
    if (f_name == -1):
        print('wrong')
        await message.reply('wrong id. try again')
        return
    # f_name = f_name[2:-3]
    f_name = f_name[0]
    print(f_name)
    f_finname = f_name[0]
    f_ref = f_name[1]
    print('write name')
    print(f_finname)
    print(f_ref)
    f_regdate = f_name[2]
    print('reg time: ', f_regdate)
    await updateState(state, 'ident', fId, Form.ident)
    await updateState(state, 'first_name', f_finname, Form.ident)
    await updateState(state, 'ref', f_ref, Form.ident)
    await updateState(state, 'reg', f_regdate, Form.ident)

    try:
        f = open(s_datafile, 'r')
    except FileNotFoundError as e:
        f = open(s_datafile, 'x')
        f = open(s_datafile, 'r')
    fData = False
    try:
        fData = json.load(f)
    except ValueError as e:
        print('bot data still empty')
    finally:
        f.close()
    fchat_id = message.chat.id
    f_tgid = message.from_user.id
    f_username = message.from_user.username
    if (fData):
        f_list = fData[k_userlist]
        isusercontain = False
        is_changed = False
        for q_user in f_list:
            if (q_user['user_id'] == fId):
                if (q_user['chat_id'] != fchat_id):
                    q_user['chat_id'] = fchat_id
                    is_changed = True
                if (q_user['tg_name'] != f_username):
                    q_user['tg_name'] = f_username
                    is_changed = True
                if (q_user['tg_id'] != f_tgid):
                    q_user['tg_id'] = f_tgid
                    is_changed = True
                isusercontain = True
        if (not isusercontain):
            f_list.append({'chat_id': fchat_id,
                           'user_id': fId,
                           'tg_name': f_username,
                           'tg_id': f_tgid})
            is_changed = True
        if (is_changed):
            fData[k_userlist] = f_list
            save_data(fData)
    else:
        fData = {k_userlist: [{'chat_id': fchat_id,
                               'user_id': fId,
                               'tg_name': f_username,
                               'tg_id': f_tgid}]}
        save_data(fData)

    await open_home(message, state)


'''
@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker and etc.)
    """
    print('get msg ')
    print(message.text)
    try:
        # Send copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
'''


@form_router.message(Command(commands=["cancel"]))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    print(current_state)
    data = await state.get_data()
    print(data['lang'])
    if current_state is None:
        return
    # print(state.lang)
    logging.info("Cancelling state %r", current_state)
    fchat_id = s_datafold + str(data['chat_id']) + '.json'
    if os.path.exists(fchat_id):
        os.remove(fchat_id)
    else:
        print("The file does not exist")

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(F.text.casefold() == "admin")
async def command_isAdmin(message: Message, state: FSMContext) -> None:
    print('req admin access')
    await state.set_state(Form.admin_enter)

    await message.answer("Введите пароль админа:")


mPass = '123'


@form_router.message(Form.admin_enter)
async def process_admin_enter(message: Message, state: FSMContext) -> None:
    print('print entered: ' + message.text)
    count = await state.get_data()
    try:
        count = count['admin_enter']
    except KeyError as e:
        count = 0
    fPass = message.text
    if (fPass == mPass):
        print('pass correct')
        await state.set_state(Form.admin_post)
        await message.answer("Введите сообщение для рассылки:")
    else:
        count = count + 1
        if (count > 5):
            await message.answer("Ошибка. Попробуйте позже")
            return
        await state.update_data(admin_enter=count)
        await message.answer("Неверный пароль. Попробуйте еще")


@form_router.message(Form.admin_post)
async def process_post(message: Message, state: FSMContext) -> None:
    print('print entered: ' + message.text)
    try:
        f_file = open(s_datafile, 'r')
        f_data = json.load(f_file)
    except (FileExistsError, ValueError) as e:
        await bot.send_message(message.from_user.id,
                               "Данные пользователей не найдены")  # like this
        return
    finally:
        f_file.close()
    user_list = f_data[k_userlist]
    for x in user_list:
        await bot.send_message(x, message.text)  # like this
    await bot.send_message(message.chat.id, 'Рассылка сделана')  # like this


import datetime


def check2():
    print('start check users')
    try:
        f = open(s_datafile, 'r')
    except FileNotFoundError as e:
        print('users not found at data.txt')
        return
    try:
        fData = json.load(f)
    except ValueError as e:
        print('bot data broken')
        return
    finally:
        f.close()
    f_timecurent = datetime.now()
    for q_userdata in fData['user_list']:
        q_chatid = q_userdata['chat_id']
        try:
            f = open(s_datafold + str(q_chatid) + '.json', 'r')
        except FileNotFoundError as e:
            print('chat data not found')
            continue
        try:
            q_json = json.load(f)
        except ValueError as e:
            print('chat data broken')
            continue
        f.close()
        q_reg = q_json['reg']
        q_base_id = q_json['ident']
        q_quest = get_db_quest(q_base_id)
        print(q_quest)
        if q_quest == -1:
            print('user done all qw')
            continue
        # 12.01.23
        q_reg = q_reg[:6] + '20' + q_reg[-2:]
        print('reg time: ' + q_reg)
        q_timereg = datetime.strptime(q_reg, '%d.%m.%Y')
        q_dif = f_timecurent - q_timereg
        q_dif = q_dif.days
        if q_dif > (q_quest - 1):
            asyncio.run(send_qw_notify(q_userdata['tg_id'], q_quest))


async def main():
    dp.include_router(form_router)
    await check2()
    await dp.start_polling(bot)
    print('wtf')


def init():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


if __name__ == "__main__":
    init()

init()
