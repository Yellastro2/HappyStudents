import tkinter
from datetime import datetime
import json
import schedule
from HappyStudent_bot import s_datafold,s_datafile,get_db_quest,send_qw_notify
from threading import Thread
import asyncio


def check_users():
    print('start notyfy thread')
    '''root = tkinter.Tk()
    root.after(5000, check)
    tkinter.mainloop()'''
    '''f_noti_thread = Thread(target = cycling)
  
  f_noti_thread.start()'''


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


'''import queue

#somewhere accessible to both:
callback_queue = queue.Queue()

def from_dummy_thread(func_to_call_from_main_thread):
    callback_queue.put(func_to_call_from_main_thread)

def from_main_thread_blocking():
    callback = callback_queue.get() #blocks until an item is available
    callback()

def from_main_thread_nonblocking():
    while True:
        try:
            callback = callback_queue.get(False) #doesn't block
        except queue.Empty: #raised when queue is empty
            break
        callback()'''


def cycling():
    print("start notify cycle")
    f_starttime = datetime.now()
    while True:
        q_time = datetime.now()
        q_period = q_time - f_starttime
        if q_period.seconds > 10:
            f_starttime = q_time
            check2()

        # schedule.every().minute.at(":30").do(check, 'It is 01:00')
