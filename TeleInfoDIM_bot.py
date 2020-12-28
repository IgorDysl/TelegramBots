import telebot
import fuzzywuzzy.fuzz as fw
from random import choice
import requests
from bs4 import BeautifulSoup
from pyowm import OWM
import sqlite3

def right_sclon(N, n11, np1, n115, np15m,  n59):
    x = N % 10
    c = N % 100 - x
    if x == 1:
        if c == 10:
            return f'{N} {n11}'
        else:
            return f'{N} {np1}'
    elif x > 1 and x < 5:
        if c == 10:
            return f'{N} {n115}'
        else:
            return f'{N} {np15m}'
    elif x > 4 or x == 0:
        return f'{N} {n59}'

bot = telebot.TeleBot('1401550057:AAHEaeyqRgqCURfrbQAIRk5Ln2y4zncwIvU')

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.add(
                 telebot.types.InlineKeyboardButton('/help'),
                 telebot.types.InlineKeyboardButton('Привет'),
                 telebot.types.InlineKeyboardButton('Пока'),
                 telebot.types.InlineKeyboardButton('Как дела?'),
                 telebot.types.InlineKeyboardButton('Какой любимый цвет?')
                 )
    out = 'Привет, Я - telegram bot, я я помогу тебе в поиске информации,'
    out += ' прогноза погоды, могу считать буджет и просто общаться. Для'
    out += ' подробного описания всех моих команд, напишите /help.'
    bot.send_message(message.from_user.id, out, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.add(telebot.types.InlineKeyboardButton('/start'),
                 telebot.types.InlineKeyboardButton('/weather'),
                 telebot.types.InlineKeyboardButton('/news'),
                 telebot.types.InlineKeyboardButton('/money'),
                 telebot.types.InlineKeyboardButton('/communicate'))
    out = 'Команды:\n'
    out += '/start - начать переписку со мной\n'
    out += '/weather - узнать погоду\n'
    out += '/news - узнать новости\n'
    out += '/money - работа с деньгами (расчет буджета, записной книжки с покупками)\n'
    out += '/communicate - общаться'

    bot.send_message(message.from_user.id, out, reply_markup=keyboard)

@bot.message_handler(commands=['news'])
def news_message(message):
    req = requests.get('https://yandex.ru/news').text
    bs = BeautifulSoup(req, 'html.parser')
    b = list(map(lambda x: x.text, bs.findAll('h2', class_='mg-card__title')))
    for i in b:
        bot.send_message(message.from_user.id, i)

@bot.message_handler(commands=['weather'])
def weather_message(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Тюмень', callback_data='Tyumen'),
                 telebot.types.InlineKeyboardButton('Москва', callback_data='Moscow'),
                 telebot.types.InlineKeyboardButton('Санкт-Петербург',
                                                    callback_data='Saint Petersburg'),
                 telebot.types.InlineKeyboardButton('Казань', callback_data='Kasan'),
                 telebot.types.InlineKeyboardButton('Омск', callback_data='Omsk'),
                 telebot.types.InlineKeyboardButton('Нижний Новгород',
                                                    callback_data='Nizhny Novgorod'),
                 telebot.types.InlineKeyboardButton('Ростов-на-Дону',
                                                    callback_data='Rostov-on-Don'),
                 telebot.types.InlineKeyboardButton('Челябинск',
                                                    callback_data='Chelyabinsk'),
                 telebot.types.InlineKeyboardButton('Екатеринбург',
                                                    callback_data='Yekaterinburg'),
                 telebot.types.InlineKeyboardButton('Самара', callback_data='Samara')
                 )
    out = 'Выберите город'
    bot.send_message(message.from_user.id, out, reply_markup=keyboard)

@bot.message_handler(commands=['money'])
def money_message(message):
    conn = sqlite3.connect("TeleInfoDim_bot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE money
                          (id INTEGER, count_money INTEGER)
                       """)
    except:
        pass
    cursor.execute(f"SELECT * FROM money WHERE id = {message.from_user.id}")
    res = cursor.fetchall()
    try:
        count_money = res[0][1]
        out = f'У вас в кошельке {right_sclon(count_money, "рублей", "рубль", "рублей", "рублей", "рублей")}'
    except:
        out = 'Теперь, введите число, которое соответствует изменению в деньгах (валюта - ₽) со знаком '
        out += 'минус (если он требуется) после решётки. Пример: #100 - добавить 100 рублей '
        out += '#-100 - отнять 100 рублей от текущего состояния'
    bot.send_message(message.from_user.id, out)

@bot.message_handler(commands=['communicate'])
def communicate_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.add(
                 telebot.types.InlineKeyboardButton('/help'),
                 telebot.types.InlineKeyboardButton('Привет'),
                 telebot.types.InlineKeyboardButton('Пока'),
                 telebot.types.InlineKeyboardButton('Как дела?'),
                 telebot.types.InlineKeyboardButton('Какой любимый цвет?')
                 )
    out = 'Давай общаться'

    bot.send_message(message.from_user.id, out, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda x: '' in x.data)
def weather_city_message(message):
    city = message.data
    owm = OWM('7e9311da0428e311ec8aabbcc3a913f9')
    manager = owm.weather_manager()
    observation = manager.weather_at_place(city)
    view = observation.weather
    out = f'Город: {city}' \
          f'\nТемпература: {view.temperature("celsius").get("temp")}°C' \
          f'\nМинимальная температура: {view.temperature("celsius").get("temp_min")}°C' \
          f'\nМаксимальная температура: {view.temperature("celsius").get("temp_max")}°C' \
          f'\nОщущается как: {view.temperature("celsius").get("feels_like")}°C' \
          f'\nВлажность: {view.humidity}%' \
          f'\nОблачность: {view.clouds}%' \
          f'\nАтмосферное давление: {view.pressure["press"]} мм рт. ст.' \
          f'\nСтатус: {view.status}'
    bot.send_message(message.from_user.id, out)

@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text.lower()[0] == '#':
        conn = sqlite3.connect("TeleInfoDim_bot.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM money WHERE id = {message.from_user.id}")
        res = cursor.fetchall()
        idd = message.from_user.id
        chislo = message.text[1:]
        if len(res) == 0:
            cursor.execute(f'''INSERT INTO money VALUES ({int(idd)}, {int(chislo)}''')
        else:
            cursor.execute(f'''UPDATE money SET count_money = {res[0][1] + int(chislo)}
WHERE id = {int(idd)}''')
        conn.commit()
    else:
        modes = {
                 1: ['привет', 'Вечер Добрый!', 'Здрасте', 'Hello', 'Здравствуйте'],
                 2: ['пока', 'Good bye!', 'Пока', 'Буду ждать'],
                 3: ['как дела?', 'Прекрасно', 'Хорошо', 'Всё OK'],
                 4: ['какой любимый цвет?', 'Зелёный', 'Синий', 'Розовый', 'Белый'],
                 5: ['обморожение', 'Согреть пораженные участки кожи (дыханием, '
                    'осторожным растиранием мягкой шерстяной тканью или руками); '
                    'наложить согревающую ватно-марлевую повязку в несколько слоев.'],
                 6: ['Переохлаждение', 'В самую первую очередь следует зайти '
                    'в теплое помещение, после чего разогреваем тело при помощи '
                    'растираний.']
                 }
        mode = -1
        out = ''
        text = message.text.lower().strip()
        for i, j in modes.items():
            if text == j[0] or fw.ratio(text, j[0]) >= 70 or \
            j[0] in text:
                mode = i
                out = choice(j[1:])
        if not out:
            out = 'Я не понял, что вы написали'
        bot.send_message(message.from_user.id, out)

bot.polling(none_stop=True, interval=0)