from datetime import datetime
import json
import schedule
import HappyStudent_bot
from threading import Thread
import asyncio

    


def check_users():
  print('start notyfy thread')
  f_noti_thread = Thread(target = cycling)
  
  f_noti_thread.start()



def check():
    print('start check users')
    try:
        f = open(HappyStudent_bot.s_datafile, 'r')
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
            f = open(HappyStudent_bot.s_datafold+str(q_chatid)+'.json', 'r')
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
        q_quest = HappyStudent_bot.get_db_quest(q_base_id)
        print(q_quest)
        if q_quest == -1 :
            print('user done all qw')
            continue
        #12.01.23
        q_reg = q_reg[:6]+'20'+q_reg[-2:]
        print('reg time: '+q_reg)
        q_timereg = datetime.strptime(q_reg, '%d.%m.%Y')
        q_dif = f_timecurent - q_timereg
        q_dif = q_dif.days
        if q_dif.day>(q_quest-1):
            asyncio.run(HappyStudent_bot.send_qw_notify(q_userdata['tg_id'],q_quest))

def cycling():
  print("start notify cycle")
  f_starttime = datetime.now()
  while True:
    q_time = datetime.now()
    q_period = q_time-f_starttime
    if q_period.seconds>10:
      f_starttime=q_time
      check()



    #schedule.every().minute.at(":30").do(check, 'It is 01:00')
    