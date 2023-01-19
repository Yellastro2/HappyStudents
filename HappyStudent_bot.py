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
  f_sel_name = f"SELECT user_name,ref FROM users2 WHERE user_id = {f_id}"
  result = select_db(f_sel_name)
  print(result)
  return result


get_db_id(49)


def get_db_quest(f_id):
  f_sel = f"SELECT vz1,vz2,vz3,vz4,vz5 FROM users2 WHERE user_id = {f_id}"
  result = select_db(f_sel)
  print(result)

  return result


def get_quest_link(f_id, f_qz):
  i = 1
  for q_qz in f_qz:
    if (q_qz == 1):
      return (i)
    i = i + 1


my_secret = os.environ['tg_token']
BOT_TOKEN = my_secret
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

lang_ru = {
  'txt_lang': '🇷🇺RUS🇷🇺',
  'txt_input_id': 'Введите ID пользователя сайта',
  'txt_home': 'Здравствуйте, ',
  'txt_make_compet': 'Выполните ваше задание:',
  'txt_set_compl': '✉️Отправить выполненное задание✉️',
  'input_comp': 'Отправьте выполненное задание сообщением сюда',
  'sumbit_comp': 'Задание отправлено куратору'
}
lang_uz = {
  'txt_lang': '🇺🇿UZB🇺🇿',
  'txt_input_id': 'Enter ID of site accout',
  'txt_home': 'Hello, ',
  'txt_make_compet': 'Make your competition:',
  'txt_set_compl': '✉️Send result✉️',
  'input_comp': 'Send competiton as message here',
  'sumbit_comp': 'Competition sendet to patron'
}
rus = 'rus'
uzb = 'uzb'
main_lang = {rus: lang_ru, uzb: lang_uz}

form_router = Router()


class Form(StatesGroup):
  ident = State()
  first_name = State()
  lang = State()
  like_bots = State()
  language = State()
  chat_id = State()
  home = State()
  input_comp = State()
  admin_enter = State()
  admin_post = State()


async def updateState(state, fkey, val, step):
  fchat_id = await state.get_data()
  fchat_id = fchat_id['chat_id']
  try:
    f = open(fchat_id, 'r')
  except FileNotFoundError as e:
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
    '''if (val == 'rus'):
      main_lang = lang_ru
    else:
      main_lang = lang_uz'''
  if (fkey == 'ident'):
    await state.update_data(ident=val)
  await state.set_state(step)


async def open_home(message, state):
  await state.set_state(Form.home)
  f_data = await state.get_data()
  f_lang = f_data['lang']
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

  await message.answer(main_lang[f_lang]['txt_home'] + f_name + '\n' +
                       main_lang[f_lang]['txt_make_compet'],
                       reply_markup=keyboard)


async def start_input_comp(message, state):
  f_data = await state.get_data()
  f_lang = f_data['lang']
  await state.set_state(Form.input_comp)
  print('start input competition')
  await message.answer(main_lang[f_lang]['input_comp'])


@form_router.message(Form.home,
                     F.text.casefold() == lang_uz['txt_set_compl'].casefold())
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
  await start_input_comp(message, state)


@form_router.message(Form.home,
                     F.text.casefold() == lang_ru['txt_set_compl'].casefold())
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
  await start_input_comp(message, state)


@form_router.message(Form.input_comp)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
  f_data = await state.get_data()
  f_lang = f_data['lang']
  await state.set_state(Form.home)
  print('get competition:')
  print(message.text)
  await message.answer(main_lang[f_lang]['sumbit_comp'])


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
  # await message.answer("Hello!")
  return False


s_datafile = 'data.txt'
k_userlist = 'user_list'


def save_data(f_data):
  fData = json.dumps(f_data)
  with open(s_datafile, "w") as my_file:
    my_file.write(fData)
    my_file.close()


@form_router.message(Command(commands=["start"]))
async def command_start(message: Message, state: FSMContext) -> None:
  print('start comand')
  fchat_id = message.chat.id
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
  #neef function from here
  if (fData):
    f_list = fData[k_userlist]
    if (f_list.count(fchat_id) < 1):
      f_list.append(fchat_id)
      fData[k_userlist] = f_list
      save_data(fData)
  else:
    fData = {k_userlist: [fchat_id]}
    save_data(fData)


#to here
  datafilename = str(message.chat.id) + '.json'
  print(message.chat.id)

  await state.update_data(chat_id=datafilename)
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
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
  fLang = 'rus'
  print('lang ', fLang)

  await updateState(state, 'lang', fLang, Form.ident)

  await req_id(message, state)


@form_router.message(Form.lang,
                     F.text.casefold() == lang_uz['txt_lang'].casefold())
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
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
  #f_name = f_name[2:-3]
  f_name = f_name[0]
  print(f_name)
  f_finname = f_name[2:-6]
  f_ref = f_name[-5:-3]
  print('write name')
  print(f_finname)
  print(f_ref)
  await updateState(state, 'ident', fId, Form.ident)
  await updateState(state, 'first_name', f_name, Form.first_name)

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
    f_file = open('data.txt', 'r')
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


async def main():
  dp.include_router(form_router)

  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
import sys


def init():

  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
