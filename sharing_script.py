from pathlib import Path

from telethon import TelegramClient
import asyncio
import json
import os

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

k_data ="data.json"

# Use your own values from my.telegram.org
api_id = 29159012
api_hash = '70a7c7ae917b8131185eac17fb9c2d6b'
#bot_token = '5980438670:AAEiBilkGTEDaQQPq-w1EGDE2LuqDZh_lvw'
#bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
#dialogs =  bot.get_dialogs()
k_addus = 'a'
k_listus = 'l'

s_sess_dir= 'sessions/'


s_max = 50
m_userlist = []
m_chat = ""

def get_data():

  try:
    f = open(k_data, 'r')
  except FileNotFoundError as e:
    print('no data yet')
    return -1
  fData = False
  try:
    fData = json.load(f)
  except ValueError as e:
    print('chat data still empty')
    return -1
  m_chat = fData
  print(f'load data:\n{m_chat}')
  f.close()
  return m_chat



def set_data(f_param):
  try:
    f = open(k_data, 'r')
  except FileNotFoundError as e:
    f = open(k_data, 'x')
    f = open(k_data, 'r')
  fData = False
  try:
    fData = json.load(f)
  except ValueError as e:
    print('chat data still empty')
  f.close()
  if (fData):
    for q_key in f_param.keys():
      fData[q_key] = f_param[q_key]
  else:
    fData = f_param

  fData = json.dumps(fData)
  with open(k_data, "w") as my_file:
    my_file.write(fData)
    my_file.close()
  print(fData)


async def check_sessions():
  print('checking sessions')
  signin = True
  id = 0
  while signin:
    try:
        if not os.path.exists(s_sess_dir):
          path = os.path.join( s_sess_dir)
          os.mkdir(path)
      #async with TelegramClient(str(id), api_id, api_hash) as cli:
        print(f'check {id} session')
        if os.path.exists(s_sess_dir+str(id)+'.session'):
          try:
            cli = TelegramClient(s_sess_dir+str(id), api_id, api_hash)
            await cli.connect()
            print('cli create!')
            f_is = await cli.is_user_authorized()
            print('auth', f_is)
            signin = cli.is_connected()
            if(signin and f_is):
              print(f'user {id} is signed in')
              f_me = await cli.get_me()
              #print(f_me.stringify())
              print(f'name - {f_me.username}, trouble - {await cli.is_bot()}')
              m_userlist.append(cli)
            else:
              print(f'{id} session no connect')
              #signin = False
              os.remove(s_sess_dir+str(id)+'.session')
              #break
              '''f_phone = input('enter phone\n>>')
              await cli.send_code_request(f_phone)
              f_code = input('enter code\n>>')
              await cli.sign_in(f_phone,f_code)'''
          except Exception:
            print('session broken')
            os.remove(s_sess_dir+str(id)+'.session')
        id = id+1
        if(id>s_max):
          signin = False
    except KeyboardInterrupt as e:
      print('\ncancel\n')
      signin = False
m_code_cash = ''
async def new_session(f_phone = -1,f_code = -1):
  id = len(m_userlist)
  if f_phone == -1:
    try:
      async with TelegramClient('sessions/' + str(id), api_id, api_hash) as cli:
        await cli.connect()
        print('cli create!')
        f_is = await cli.is_user_authorized()
        print('auth', f_is)
        signin = cli.is_connected()
        if (signin and f_is):
          print(f'user {id} is signed in')
          f_me = await cli.get_me()
          # print(f_me.stringify())
          print(f'name - {f_me.username}, trouble - {await cli.is_bot()}')
          m_userlist.append(cli)
        else:
          print('no connect')
    except KeyboardInterrupt:
      return
  else:
    if f_code ==-1:
      f_cli = TelegramClient('sessions/' + str(id), api_id, api_hash)
      await f_cli.connect()
      m_code_cash= await f_cli.send_code_request(f_phone)
      m_userlist.append(f_cli)
    else:
      f_cli = m_userlist[len(m_userlist)-1]
      #TelegramClient('sessions/' + str(id), api_id, api_hash)
      #await f_cli.connect()
      await f_cli.sign_in(f_phone,f_code,phone_code_hash=None)
      m_userlist.append(f_cli)
    #os.remove(s_sess_dir+str(id)+'.session')


async def list_sessions():
  i = 0
  for q_cli in m_userlist:
    await q_cli.connect()
    print(q_cli.is_connected())
    q_me = await q_cli.get_me()
    q_body = f'user {i}: id - {q_me.id}, name - {q_me.username}'
    print(q_body)
    i = i+1


s_chat_path = 'chat_path/'
async def set_chat(f_chatid = -1):
  if f_chatid==-1:
    f_chatid = input('set id or link or whatever..\n>>')
  #print(bot.is_connected())
  if len(m_userlist)<1:
    f_res = await check_sessions()
    if f_res == 404 or len(m_userlist)<1:
      return 404
  async with m_userlist[0] as cli:
  #async with bot as cli:
    await cli.connect()
    f_save = get_data()
    #если будут проблемы, добавь условие или инт или стр на чатайди
    #и делай в первом случае через PeerChannel
    channel = await cli.get_entity(f_chatid)
    user_list = cli.iter_participants(entity=channel)
    f_user_list =[]
    async for _user in user_list:
      if not _user.deleted:
        print(_user.username)
        if _user.username != None:
          f_user_list.append(_user.username)
    if len(f_user_list)>0:
      if not os.path.exists(s_chat_path):
        os.mkdir(s_chat_path)
      f_json_users = json.dumps(f_user_list)
      with open(s_chat_path+f_chatid[13:]+'.json', "w+") as my_file:
        my_file.write(f_json_users)
        my_file.close()
    '''print('found somethick')
    print('find chat: '+channel.title)
    m_chat = channel.id
    f_title_ch= channel.username
    print(f_title_ch)
    f_save["main_chat"].append(f_title_ch)
    set_data(f_save)'''
    

async def send_test():
  f_chat = input("enter chat id")

  f_cli = m_userlist[0]
  await f_cli.connect()
  await f_cli.send_message(f_chat,"это тест")

import time
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
f_dict = ['hello','hi','lol','wtf']

s_body_spam = '''Совершенно новая технология автоматизации бизнеса в течение несколько дней. Выполняя 5 заданий компании, создаёшь источник постоянного крупного дохода. Происходит:
1)  постоянное увеличение количества платежеспособных покупателей для продажи торговой программы, деньги от которых прямиком поступают на Ваш кошелек;
2)  получение неограниченные по количеству инвестиций на Ваш бизнес;
3)  бесконечная целевая реклама любого Вашего бизнеса.
Если хочешь обрашайся в личку с запросом "хочу ссылку на регистрацию в Happy Students". С уважением, @N'''

s_bask_path = 'basket/'

async def start_spam():
  is_contin = True
  i = 0
  f_list_chats = os.listdir(s_chat_path)
  if len(f_list_chats)<1:
    print('ERROR 404 - NO CHAT SCANNED YET')
  f_chat_path = f_list_chats[0]
  try:
    f_targets_fl = open(f_chat_path,'r')
    f_targets = json.load(f_targets_fl)
    f_targets_fl.close()
  except Exception as e:
    print(e)
    print('error')
  print(f_list_chats)
  while is_contin:
    #придумать ему какое то ограничение на юсера
    if len(m_userlist)>=i+1:
      print('ERROR 505 - USERS OVER FOR TODAY')
      break
    q_user = m_userlist[i]
    await q_user.connect()
    f_me = await q_user.get_me()
    for q in range(10):
      if len(f_targets)<1:
        Path(s_chat_path+f_chat_path).rename(s_bask_path+f_chat_path)
        #тут вот чето надо сделать
        start_spam()
        return
      q_trg = f_targets[0]
      m_ch_cli = await q_user.get_entity(q_trg)
      await q_user.send_message(m_ch_cli, q_body)
      q_body = s_body_spam.replace('@N',f_me.username)
      print(f'send msg {q_body} from user {f_me.username}')
      f_targets.remove(q_trg)
      time.sleep(600)
      #target_group_entity = InputPeerChannel(m_ch_cli.id, m_ch_cli.access_hash)
      # f_peep_user = InputPeerUser(f_me.id,f_me.access_hash)
      #await q_user(JoinChannelRequest(target_group_entity))
    i = i+1




async def cycle():
  if len(m_userlist) < 1:
    print('add at least one user')
    await new_session()
    await cycle()
    return
  '''m_chat = get_data().get('main_chat', '')
  if m_chat == '':
    print('need to set some chat')
    await set_chat()
    await cycle()
    return
  print(m_chat)
  m_ch_cli = m_userlist[0]
  await m_ch_cli.connect()
  m_ch_cli = await m_ch_cli.get_entity((m_chat))
'''
  f_com = input(f'''Group_Spawner startet
Users signin - {len(m_userlist)}
Use Ctrl+c to exit from any command
Use comand \n"{k_addus}" - for check sessions and add more
"l" - for print users list
"sc" - for scan some chat to logic data
"s" - to start flood
>>''')
  f_run = ''
  if (f_com == k_addus):
    f_run = new_session
  elif (f_com == k_listus):
    f_run = list_sessions
  elif (f_com == 'c'):
    f_run = set_chat
  elif (f_com == 't'):
    f_run = send_test
  elif (f_com == 's'):
    f_run = start_spam
  else:
    print('wrong command!')
    await cycle()
  try:
    await f_run()
  except KeyboardInterrupt as e:
    print('\ncancel\n')
    signin = False
  await cycle()


# cycle()
# The first parameter is the .session file name (absolute paths allowed)
async def run():
  await check_sessions()
  await cycle()


asyncio.run(run())
