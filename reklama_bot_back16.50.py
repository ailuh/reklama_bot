import config
import telebot
from telebot import types
import json

bot = telebot.TeleBot(config.token)

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
    markup = types.ReplyKeyboardMarkup()
    markup.row('Рекламодателю')
    markup.row('Заказчику')
    markup.row('Правила','Отзывы')
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=markup)
@bot.message_handler(commands=['distr'])
def distr_message(message):
    with open('id_file.json', 'r', encoding='utf8') as ids: #открываем файл на чтение
        data = json.load(ids)
        for i in data:
            bot.send_message(data[i], "Где деньги, лебовски?")
    
@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    answer = message.text
    if answer=='Правила':
        bot.send_message(message.chat.id, "Не материться")
    print(message.from_user.first_name)
    print(message.from_user.id)
    print(answer)
        
if __name__ == '__main__':
    bot.polling(none_stop=True)
