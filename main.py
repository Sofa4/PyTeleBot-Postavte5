# Телеграм-бот v.004


import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types

#import urllib.request, json
#from urllib.request import urlopen

import requests
import bs4
import botGames  # бот-игры, файл botGames.py
from menuBot import Menu, Users  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню


api_key = '5105972662:AAG24fr382U1_hosO4Zrb-tv_BTakAV1MPk'

bot = telebot.TeleBot(api_key)  # Создаем экземпляр бота


# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands=['start'])
def command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAIaeWJEeEmCvnsIzz36cM0oHU96QOn7AAJUAANBtVYMarf4xwiNAfojBA")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)


# -----------------------------------------------------------------------
# Получение стикеров от юзера
@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

    # глубокая инспекция объекта
    # import inspect,pprint
    # i = inspect.getmembers(sticker)
    # pprint.pprint(i)


# -----------------------------------------------------------------------
# Получение аудио от юзера
@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)


# -----------------------------------------------------------------------
# Получение голосовухи от юзера
@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)


# -----------------------------------------------------------------------
# Получение фото от юзера
@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)


# -----------------------------------------------------------------------
# Получение видео от юзера
@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)


# -----------------------------------------------------------------------
# Получение документов от юзера
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")


# -----------------------------------------------------------------------
# Получение координат от юзера
@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)


# -----------------------------------------------------------------------
# Получение контактов от юзера
@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    wrong_key = False

    chat_id = message.chat.id
    ms_text = message.text

    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, message.json["from"])

    result = goto_menu(chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if result:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    cur_menu = Menu.getCurMenu(chat_id)

    if cur_menu is not None:
        if ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню
            if ms_text == "Помощь":
                send_help(chat_id)

            elif ms_text == "Прислать собаку":
                bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка!")

            elif ms_text == "Прислать фильм":
                send_film(chat_id)

            elif ms_text == 'Прислать кофе':
                bot.send_photo(chat_id, photo=get_randomCoffee(), caption="Случайное Кофе")

            elif ms_text == "Новая игра":
                text_game = "❌ Игрок\n" \
                            "⭕ Компьютер"

                markup = types.InlineKeyboardMarkup()

                for i in range(3):
                    btn1 = types.InlineKeyboardButton(text="⬜", callback_data=f'field_{1 + i * 3}')
                    btn2 = types.InlineKeyboardButton(text="⬜", callback_data=f'field_{2 + i * 3}')
                    btn3 = types.InlineKeyboardButton(text="⬜", callback_data=f'field_{3 + i * 3}')

                    markup.add(btn1, btn2, btn3)

                sended_message = bot.send_message(chat_id, text=text_game, reply_markup=markup)

                gameTicTacToe = botGames.getGame(chat_id)
                gameTicTacToe.newGame(chat_id, sended_message.id)

            elif ms_text == "Стоп!":
                botGames.stopGame(chat_id)
                goto_menu(chat_id, "Выход")
                return


        elif cur_menu.getCurMenuName(chat_id) == 'Прислать гороскоп':
            zodiac_signs_list = ['овен', 'телец', 'близнецы', 'рак',
                                 'лев', 'дева', 'весы', 'скорпион',
                                 'стрелец', 'козерог', 'водолей', 'рыбы']

            user_sign = message.text.lower()

            if user_sign in zodiac_signs_list:
                send_horoscope(chat_id, user_sign)
            else:
                bot.send_message(chat_id, text="Вы ввели неверный знак Зодиака. Попробуйте еще раз")
        else:
            wrong_key = True

    else:  # ...........................................................................................................
        wrong_key = True

    if wrong_key:
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        goto_menu(chat_id, "Главное меню")


# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать параметр или несколько параметров в обработчик кнопки,
    # использовать методы Menu.getExtPar() и Menu.setExtPar()

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # Камень, ножницы, бумага
    if call.data == 'cb_rock':
        rsp_game_result(chat_id, message_id, 'Камень')

    elif call.data == 'cb_scissors':
        rsp_game_result(chat_id, message_id, 'Ножницы')

    elif call.data == 'cb_paper':
        rsp_game_result(chat_id, message_id, 'Бумага')

    # Крестики-нолики
    keyboard = call.message.reply_markup.keyboard

    if call.data[:-2] == 'field':
        field_number = int(call.data[-1]) - 1
        button = keyboard[field_number // 3][field_number % 3]

        tic_tac_toe_player_choice(chat_id, message_id, field_number, button)


def tic_tac_toe_player_choice(chat_id, message_id, field_number, button):
    gameTicTacToe = botGames.getGame(chat_id)

    if gameTicTacToe is None:  # если мы случайно попали в это меню, а объекта с игрой нет
        goto_menu(chat_id, "Выход")
        return

    if Menu.getCurMenuName(chat_id) == 'Крестики-нолики':
        if button.text == '⬜':
            game_end = gameTicTacToe.gameEndCheck(chat_id, message_id)

            if game_end == 0:
                # Ход игрока
                gameTicTacToe.playerChoice(chat_id, message_id, field_number)
                ttt_refresh_markup(chat_id, message_id, gameTicTacToe.getField(chat_id, message_id))

                # Проверка конца игры
                game_end = gameTicTacToe.gameEndCheck(chat_id, message_id)

                if game_end == 0:
                    # Ход компьютера
                    gameTicTacToe.computerChoice(chat_id, message_id)
                    ttt_refresh_markup(chat_id, message_id, gameTicTacToe.getField(chat_id, message_id))

                    game_end = gameTicTacToe.gameEndCheck(chat_id, message_id)

                if game_end != 0:
                    ttt_game_end_refresh(chat_id, message_id, game_end, gameTicTacToe)
    else:
        text_game = "❌ Игрок\n" \
                    "⭕ Компьютер"

        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=text_game, parse_mode='HTML', reply_markup=None)


def ttt_game_end_refresh(chat_id, message_id, win_side, game):
    field = game.getField(chat_id, message_id)

    if win_side == 1:
        text_game = "⠀⠀⠀⠀<b>Победа игрока</b>\n" \
                    "❌ Игрок⠀⠀⠀⠀⠀⠀🏆\n" \
                    "⭕ Компьютер⠀⠀😭"
    elif win_side == 2:
        text_game = "⠀⠀⠀⠀<b>Победа компьютера</b>\n" \
                    "❌ Игрок⠀⠀⠀⠀⠀⠀😭\n" \
                    "⭕ Компьютер⠀⠀🏆"
    else:
        text_game = "⠀⠀⠀⠀<b>Ничья</b>\n" \
                    "❌ Игрок⠀⠀⠀⠀⠀⠀😐\n" \
                    "⭕ Компьютер⠀⠀😐"

    game.editGameResult(chat_id, message_id, text_game)

    markup = types.InlineKeyboardMarkup()
    markup_row = []

    for i in range(9):
        if field[i] == 0:
            markup_row.append(types.InlineKeyboardButton(text="⬜", callback_data=f'field_{i + 1}'))

        elif field[i] == 1:
            markup_row.append(types.InlineKeyboardButton(text="❌", callback_data=f'field_{i + 1}'))

        else:
            markup_row.append(types.InlineKeyboardButton(text="⭕", callback_data=f'field_{i + 1}'))

        if i % 3 == 2:
            markup.add(*markup_row)
            markup_row = []

    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=text_game, parse_mode='HTML', reply_markup=markup)


def ttt_refresh_markup(chat_id, message_id, field):
    markup = types.InlineKeyboardMarkup()
    markup_row = []

    for i in range(9):
        if field[i] == 0:
            markup_row.append(types.InlineKeyboardButton(text="⬜", callback_data=f'field_{i + 1}'))

        elif field[i] == 1:
            markup_row.append(types.InlineKeyboardButton(text="❌", callback_data=f'field_{i + 1}'))

        else:
            markup_row.append(types.InlineKeyboardButton(text="⭕", callback_data=f'field_{i + 1}'))

        if i % 3 == 2:
            markup.add(*markup_row)
            markup_row = []

    text_game = "❌ Игрок\n" + \
                "⭕ Компьютер"

    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=text_game, parse_mode='HTML', reply_markup=markup)


def ttt_clear_markup(chat_id, fields_messages):
    for message_id in fields_messages[str(chat_id)].keys():
        bot.edit_message_text(chat_id=chat_id, message_id=int(message_id),
                              text=fields_messages[str(chat_id)][message_id],
                              parse_mode='HTML', reply_markup=None)


def rsp_game_result(chat_id, message_id, player_choice=None):
    gameRSP = botGames.getGame(chat_id)

    if gameRSP is None:  # если мы случайно попали в это меню, а объекта с игрой нет
        goto_menu(chat_id, "Выход")
        return

    if Menu.getCurMenuName(chat_id) == 'Камень, ножницы, бумага':
        victory_text = gameRSP.playerChoice(player_choice)

        round_result_text = f'⠀⠀⠀⠀<b>Игровой⠀раунд</b>' + '\n\n' + \
                            f'Игрок:    <b>{player_choice}</b>' + '\n' + \
                            f'Компьютер:    <b>{gameRSP.computerChoice}</b>'

        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=round_result_text, parse_mode='HTML', reply_markup=None)
        gameRSP.editGameResult(chat_id, message_id, round_result_text)

        bot.send_message(chat_id, text=victory_text)
        gameRSP.newGame(chat_id, message_id)

        rsp_game_start(chat_id)
    else:
        round_text = '⠀⠀⠀⠀<b>Игровой⠀раунд</b>' + '\n\n' + \
                     'Игрок:    <b>???</b>' + '\n' + \
                     'Компьютер:    <b>???</b>'

        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=round_text, parse_mode='HTML', reply_markup=None)


def rsp_game_start(chat_id):
    round_start_text = '⠀⠀⠀⠀<b>Игровой⠀раунд</b>' + '\n\n' + \
                       'Игрок:    <b>???</b>' + '\n' + \
                       'Компьютер:    <b>???</b>'

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text="Камень", callback_data='cb_rock')
    btn2 = types.InlineKeyboardButton(text="Ножницы", callback_data='cb_scissors')
    btn3 = types.InlineKeyboardButton(text="Бумага", callback_data='cb_paper')

    markup.add(btn1, btn2, btn3)

    sended_message = bot.send_message(chat_id, text=round_start_text, parse_mode='HTML', reply_markup=markup)

    gameRSP = botGames.newGame(chat_id, botGames.GameRPS(chat_id))  # создаём новый экземпляр игры
    gameRSP.newGame(chat_id, sended_message.id)


def rsp_clear_markup(chat_id, games_results):
    for message_id in games_results[str(chat_id)].keys():
        bot.edit_message_text(chat_id=chat_id, message_id=int(message_id),
                              text=games_results[str(chat_id)][message_id],
                              parse_mode='HTML', reply_markup=None)


# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu is not None and cur_menu.parent is not None:
        games = botGames.getGame(chat_id)

        if games is not None:
            if games.name == 'ттт':
                botGames.stopGame(chat_id)
                ttt_clear_markup(chat_id, games.games_results)

            elif games.name == 'кнб':
                botGames.stopGame(chat_id)
                rsp_clear_markup(chat_id, games.games_results)

        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu is not None:
        if target_menu.name == 'Прислать гороскоп':
            text = 'Отправьте знак зодиака, на который Вы хотите получить гороскоп'

            bot.send_message(chat_id, text=text, reply_markup=target_menu.markup)
        else:
            bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Камень, ножницы, бумага":
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу"

            bot.send_photo(chat_id, photo="https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg",
                           caption=text_game, parse_mode='HTML')

            rsp_game_start(chat_id)

        elif target_menu.name == "Крестики-нолики":
            text_game = "❌ Игрок\n" \
                        "⭕ Компьютер"

            markup = types.InlineKeyboardMarkup()

            for i in range(3):
                btn1 = types.InlineKeyboardButton(text="⬜", callback_data=f'field_{1 + i * 3}')
                btn2 = types.InlineKeyboardButton(text="⬜", callback_data=f'field_{2 + i * 3}')
                btn3 = types.InlineKeyboardButton(text="⬜", callback_data=f'field_{3 + i * 3}')

                markup.add(btn1, btn2, btn3)

            sended_message = bot.send_message(chat_id, text=text_game, reply_markup=markup)

            gameTicTacToe = botGames.newGame(chat_id, botGames.gameTicTacToe(chat_id))  # создаём новый экземпляр игры
            gameTicTacToe.newGame(chat_id, sended_message.id)

        return True
    else:
        return False


# -----------------------------------------------------------------------
def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Панасенко Софья, 1-МД-5")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/ave_satanas_bitch")
    markup.add(btn1)
    img = open('author.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in Users.activeUsers:
        bot.send_message(chat_id, Users.activeUsers[el].getUserHTML(), parse_mode='HTML')


# -----------------------------------------------------------------------
def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n\n" \
               f"<b>Год:</b> {film['Год']}\n" \
               f"<b>Страна:</b> {film['Страна']}\n"

    if film['Жанр'] != '':
        info_str += f"<b>Жанр:</b> {film['Жанр']}\n"

    if film['Продолжительность'] != '':
        info_str += f"Продолжительность: {film['Продолжительность']}"

    if film['Режиссёр'] != '':
        info_str += f"<b>Режиссёр:</b> {film['Режиссёр']}\n"

    if film['Актёры'] != '':
        info_str += f"<b>Актёры:</b> {film['Актёры']}"

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)

# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()

    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')

    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm

# -----------------------------------------------------------------------
def send_horoscope(chat_id, sign):
    zodiac_signs_dict = {
        'овен': 'aries', 'телец': 'taurus',
        'близнецы': 'gemini', 'рак': 'cancer',
        'лев': 'leo', 'дева': 'virgo',
        'весы': 'libra', 'скорпион': 'scorpio',
        'стрелец': 'sagittarius', 'козерог': 'capricorn',
        'водолей': 'aquarius', 'рыбы': 'pisces'
    }

    horoscope = get_randomHoroscope(zodiac_signs_dict[sign])

    horoscope_text = \
        f"<b>Знак Зодиака:</b> {sign}\n\n" \
        f"<b>Текущая дата: </b>{horoscope['current_date']}\n" \
        f"<b>Описание:</b> {horoscope['description']}\n" \
        f"<b>Совместимость:</b> {horoscope['compatibility']}\n" \
        f"<b>Настроение:</b> {horoscope['mood']}\n" \
        f"<b>Цвет:</b> {horoscope['color']}\n" \
        f"<b>Счастливое число:</b> {horoscope['lucky_number']}\n" \
        f"<b>Счастливое время:</b> {horoscope['lucky_time']}\n"

    bot.send_message(chat_id, text=horoscope_text, parse_mode='HTML')


# -----------------------------------------------------------------------
def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url

# ---------------------------------------------------------------------
def get_randomHoroscope(sign):
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator(source='en', target='ru')

    url = 'https://aztro.sameerkumar.website/'

    params = (
        ('sign', sign),
        ('day', 'today')
    )

    req_horoscope = requests.post(url, params=params).json()

    for key in req_horoscope.keys():
        if key == 'lucky_number':
            break

        req_horoscope[key] = translator.translate(req_horoscope[key])

    return req_horoscope

# ---------------------------------------------------------------------
def get_randomCoffee():
    url = "https://coffee.alexflipnote.dev/random.json"

    req_coffee = requests.get(url)

    if req_coffee.status_code == 200:
        r_json = req_coffee.json()
        url = r_json['file']

    return url


# ---------------------------------------------------------------------
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, interval=0)  # Запускаем бота

    except Exception as e:
        print(e)
