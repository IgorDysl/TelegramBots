import telebot
from random import randint
from game_cities_bot_cities import citiess

cities = citiess

def last_cor_chr(word):
    word = word.lower()
    l = ''
    for i in word[::-1]:
        if i not in 'ьыъё':
            l = i
            break

    return l

def correct(word, uword):
    word = word.lower()
    uword = uword.lower()
    l = last_cor_chr(word)
    ul = uword[0]
    print(l, ul)
    if ul == l:
        return True
    else:
        return False

def choose_word(word):
    word = word.lower()
    lst = last_cor_chr(word)
    try:
        source = cities[lst]
        rand = randint(0, len(source))
    except:
        pass


    return cities[lst].pop(rand)

def delete_users_word(word):
    wrd = word
    word = word.lower()
    source = cities[word[0]]
    if wrd in cities[word[0]]:
        cities[word[0]].pop(cities[word[0]].index(wrd))
        return True
    else:
        return False

bot = telebot.TeleBot('1360448945:AAGtY3SkJSWK2BHJIpbiPrIRG7DsxX2zrKo')

users_word = ''
word_of_bot = 'word'
been = False

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Привет, я введи название города и игра начнётся')

@bot.message_handler(commands=['end'])
def end_message(message):
    cities = citiess
    bot.send_message(message.from_user.id, 'Будет скучно, обрвщвйтесь')
@bot.message_handler(content_types=['text'])
def text_message(message):
    users_word = message.text
    word_of_bot = ''
    nw = choose_word(users_word)
    out = ''
    iss = True
    if been:
        if correct(users_word, word_of_bot):
            pass
        else:
            out += 'Вы ааели начали слово не с той буквы'
            iss = False
        if delete_users_word(users_word):
            pass
        else:
            if not out:
                out += 'Такого города нет в моей базе'
                iss = False
    else:
        if delete_users_word(users_word):
            be = True
        else:
            if not out:
                out += 'Такого города нет в моей базе'
                iss = False
    if iss:
        out = choose_word(users_word)
        word_of_bot = out
    bot.send_message(message.from_user.id, out)

bot.polling(none_stop=True, interval=0)