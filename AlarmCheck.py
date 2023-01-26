from datetime import datetime
import json

import HappyStudent_bot

    

async def check_users():
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
        if q_quest == -1 :
            print('user done all qw')
            continue
        #12.01.23
        q_timereg = datetime.strptime(q_reg, '%m.%d.%Y')
        q_dif = f_timecurent - q_timereg
        q_dif = q_dif.days
        if q_dif.days>(q_quest-1):
            await send_qw_notify(q_userdata['tg_id'],q_quest)
