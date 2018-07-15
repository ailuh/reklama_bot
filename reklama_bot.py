import config
import telebot
from telebot import types
import json
class Group_file:
    def __init__(self):
        with open('group_file.json', 'r', encoding='utf-8') as ids: #открываем файл на чтение
                self.data = json.load(ids) #загружаем из файла данные в словарь data
class Auth:
    def __init__(self):
        self.flag=[False,False,False,False,False,False,False,False,False,False]
        self.group_dict={}
    def set_flag(self, fl):
        self.flag[fl]=True
    def reset_flag(self, fl):
        self.flag[fl]=False
    def sost_flag(self):
        k=0
        for i in self.flag:
            print('Состояние флага {} - {}'.format(k, self.flag[i]))
            k+=1
    def reset_dist(self):
        for i in range (0, len(self.flag)):
            self.flag[i]=False
        self.group_dict.clear()
        
bot = telebot.TeleBot(config.token)
def keyb (args):
    print(args)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in args])
    return keyboard

@bot.message_handler(commands=['start'])
def start_mess(message): #Приветствие
    #загрузить из json
    with open('id_file.json', 'r', encoding='utf-8') as ids: #открываем файл на чтение
        data = json.load(ids) #загружаем из файла данные в словарь data
    #print(data)
    print(data)
    flag=True
    for i in data:
        if data[i]==message.from_user.id:
            flag=False
            break
    print(flag)
    if flag:
        with open('id_file.json', 'w', encoding='utf8') as outfile:
            data.update({message.from_user.first_name:message.from_user.id})
            print(data)
            json.dump(data, outfile)
    wel_keyb=('Рекламодателю','Заказчику','Правила','Отзывы')
    bot.send_message(message.chat.id, "Данный бот предназначен для покупки рекламы:", reply_markup=keyb(wel_keyb))
@bot.message_handler(commands=['distr'])
def distr_message(message):
    with open('id_file.json', 'r', encoding='utf8') as ids: #открываем файл на чтение
        data = json.load(ids)
        for i in data:
            bot.send_message(data[i], "Где деньги, лебовски?")
    
@bot.callback_query_handler(func=lambda a:True)
def check_answer(a):
    answer = a.data
    auten.sost_flag()
    outstr=('Предыдущая стр', 'Связаться', 'Следующая стр')
    if answer=='Правила':
        bot.send_message(a.message.chat.id, "Не материться")
    if answer=='Рекламодателю':
        bot.edit_message_text(
            chat_id=a.message.chat.id,
            message_id=a.message.message_id,
            text='Это первая страница',
            reply_markup=keyb(outstr)
            )
    if answer=="Подтвердить":
        outstr=('Подтвердить', 'Отменить')
        if auten.flag[1]:
            bot.send_message(a.message.chat.id, "Пароль веден корректно. Введите название группы:", reply_markup=keyb(outstr))
            auten.set_flag(2)
            auten.reset_flag(1)
        if auten.flag[3]:
            bot.send_message(a.message.chat.id, "Введите количество подписчиков:", reply_markup=keyb(outstr))
            auten.set_flag(4)
            auten.reset_flag(3)
        if auten.flag[5]:
            bot.send_message(a.message.chat.id, "Введите описание группы:", reply_markup=keyb(outstr))
            auten.set_flag(6)
            auten.reset_flag(5)
        if auten.flag[7]:
            with open('group_file.json', 'r', encoding='utf-8') as ids: #открываем файл на чтение
                data = json.load(ids) #загружаем из файла данные в словарь data
            with open('group_file.json', 'w', encoding='utf8') as outfile:
                data.append(auten.group_dict)
                print(data)
                json.dump(data, outfile)
            bot.edit_message_text(
                chat_id=a.message.chat.id,
                message_id=a.message.message_id,
                text='Данные успешно добавлены! Можете продолжать работу.',
                reply_markup=keyb(outstr)
                )
            auten.reset_dist()
    auten.sost_flag()
@bot.message_handler(commands=['group'])
def distr_message(message):
    outstr=('Подтвердить', 'Отменить')
    with open('group_file.json', 'r', encoding='utf8') as ids: #открываем файл на чтение
        data = json.load(ids)
    print(data)
    bot.send_message(message.chat.id, "Введите пароль", reply_markup=keyb(outstr))

@bot.message_handler(content_types=["text"])
def corr_pass(message):
    print(message.text)
    if message.text=='qwerty':
        print('Принял')
        auten.set_flag(1)
    print(auten.flag1)
    if auten.flag[2]:
        auten.group_dict["Group_name"]=message.text
        auten.set_flag(3)
        auten.reset_flag(2)
        print(auten.group_dict)
    if auten.flag[4]:
        auten.group_dict["Users"]=message.text
        auten.set_flag(5)
        auten.reset_flag(4)
        print(auten.group_dict)
    if auten.flag[6]:
        auten.group_dict["Description"]=message.text
        auten.set_flag(7)
        auten.reset_flag(6)
        print(auten.group_dict)
    
if __name__ == '__main__':
    auten=Auth()
    daten=Group_file()
    bot.polling(none_stop=True)
    
