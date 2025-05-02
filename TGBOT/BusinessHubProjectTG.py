import telebot
import os

API_TOKEN = '' #your token
ADMIN_ID = #your id

SUBSCRIBERS_FILE = "subscribers.txt"

bot = telebot.TeleBot(API_TOKEN)

MESSAGE_FILE = 'answers.txt'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return set()
    with open(SUBSCRIBERS_FILE, 'r') as f:
        return set(map(int, f.read().splitlines()))
    
def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, 'w') as f:
        for user_id in subscribers:
            f.write(f"{user_id}\n")

def add_subscriber(user_id):
    subscribers = load_subscribers()
    if user_id not in subscribers:
        subscribers.add(user_id)
        save_subscribers(subscribers)

def remove_subscriber(user_id):
    subscribers = load_subscribers()
    if user_id in subscribers:
        subscribers.remove(user_id)
        save_subscribers(subscribers)

def get_answer_for_key(key):
    if not os.path.exists(MESSAGE_FILE):
        print(f"File is not found: {MESSAGE_FILE}")
        return None

    try:
        with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        sections = content.split("##")

        for section in sections:
            stripped_section = section.strip()
            if not stripped_section:
                continue

            lines = stripped_section.split('\n', 1)
            section_key = lines[0].strip()

            if section_key == key:
                if len(lines) > 1:
                    return lines[1].strip()
                else:
                    return "Информация по этому разделу пока отсутствует."

        print(f"Key '{key}' is not found in the file.{MESSAGE_FILE}")
        return None

    except Exception as e:
        print(f"Error reading file or parsing contents: {e}")
        return None

        

@bot.message_handler(commands=['start'])
def welcome(message):
    user_name = message.from_user.first_name 
    greeting = f"{user_name}"  

    bot.send_message(message.chat.id, f"Добро Пожаловать в Business Hub Project Bot, {greeting}! \nЗдесь вы можете получить информацию о Business Hub и его услугах.")

    menu(message)

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    about = telebot.types.KeyboardButton('📖О нас📖')
    structure = telebot.types.KeyboardButton('🛠Структура Проекта🛠')
    autors = telebot.types.KeyboardButton('🧑‍💻Авторы Проекта🧑‍💻')
    social = telebot.types.KeyboardButton('📱Соцсети📱')
    news = telebot.types.KeyboardButton('🗞Новостные рассылки🗞')
    presentation = telebot.types.KeyboardButton('📊Презентация📊')
    # donate = telebot.types.KeyboardButton('Донат')
    markup.add(about, structure, autors, social, news, presentation)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '📖О нас📖')
def about(message):
    answer = get_answer_for_key('О нас')
    if answer is not None: 
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Информация по запросу "О нас" не найдена или произошла ошибка при чтении файла.')

@bot.message_handler(func=lambda message: message.text == '🛠Структура Проекта🛠')
def handle_structure_project_text(message):
    try:
        with open("IMAGES/structure.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        print("Structure file not found.")
        bot.send_message(message.chat.id, "Изображение структуры не найдено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке изображения: {e}")

    answer = get_answer_for_key('Структура Business Hub Project')
    if answer is not None:
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Информация по запросу "Структура Business Hub Project" не найдена в файле или произошла ошибка при чтении.')

@bot.message_handler(func=lambda message: message.text == '🧑‍💻Авторы Проекта🧑‍💻')
def handle_authors_text(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    flipuk = telebot.types.InlineKeyboardButton('Разработчик')
    chfr = telebot.types.InlineKeyboardButton('Дизайнер')
    back = telebot.types.InlineKeyboardButton('⬅️Назад⬅️')
    markup.add(flipuk, chfr, back)
    bot.send_message(message.chat.id, 'Авторы проекта:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Разработчик')
def handle_flipuk_text(message):

    answer = get_answer_for_key('Разработчик')

    flipuk4_image_path = os.path.join(BASE_DIR, "IMAGES", "Flipuk4.png")
    try:

        with open(flipuk4_image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=answer if answer else None)

    except FileNotFoundError:
        print(f"Photo not found on route: {flipuk4_image_path}")
        bot.send_message(message.chat.id, "Фото не найдено.")

        if answer:
             bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {e}")
        if answer:
             bot.send_message(message.chat.id, answer)

    if answer is None and not os.path.exists(flipuk4_image_path):
         bot.send_message(message.chat.id, 'Информация по запросу "Разработчик" не найдена (фото или текст).')


@bot.message_handler(func=lambda message: message.text == 'Дизайнер')
def handle_chfr_text(message):

    answer = get_answer_for_key('Дизайнер')

    CHFR2_image_path = os.path.join(BASE_DIR, "IMAGES", "CHFR2.png")
    try:

        with open(CHFR2_image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=answer if answer else None)

    except FileNotFoundError:
        print(f"Photo not found on route: {CHFR2_image_path}")
        bot.send_message(message.chat.id, "Фото не найдено.")

        if answer:
             bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {e}")
        if answer:
             bot.send_message(message.chat.id, answer)

    if answer is None and not os.path.exists(CHFR2_image_path):
         bot.send_message(message.chat.id, 'Информация по запросу "Дизайнер" не найдена (фото или текст).')

@bot.message_handler(func=lambda message: message.text == '📱Соцсети📱')
def handle_chfr_text(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    tg = telebot.types.KeyboardButton('✈️Telegram✈️')
    ig = telebot.types.KeyboardButton('📸Instagram📸')
    gt = telebot.types.KeyboardButton('😺Github😺')
    mail = telebot.types.KeyboardButton('📪Mail📪')
    back = telebot.types.KeyboardButton('⬅️Назад⬅️')
    markup.add(tg, ig, gt, mail, back)
    bot.send_message(message.chat.id, 'Выберите соцсети:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '✈️Telegram✈️')
def handle_tg_button(message):
    answer = get_answer_for_key('ТГ')
    if answer is not None: 
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Информация по запросу "✈️Telegram✈️" не найдена или произошла ошибка при чтении файла.')

@bot.message_handler(func=lambda message: message.text == '📸Instagram📸')
def handle_tg_button(message):
    answer = get_answer_for_key('ИНСТ')
    if answer is not None: 
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Информация по запросу "📸Instagram📸" не найдена или произошла ошибка при чтении файла.')

@bot.message_handler(func=lambda message: message.text == '😺Github😺')
def handle_tg_button(message):
    answer = get_answer_for_key('ГТ')
    if answer is not None: 
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Информация по запросу "😺Github😺" не найдена или произошла ошибка при чтении файла.')

@bot.message_handler(func=lambda message: message.text == '📪Mail📪')
def handle_tg_button(message):
    answer = get_answer_for_key('Мыло')
    if answer is not None: 
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Информация по запросу "📪Mail📪" не найдена или произошла ошибка при чтении файла.')


@bot.message_handler(func=lambda message: message.text == '🗞Новостные рассылки🗞')
def news(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    sb = telebot.types.KeyboardButton('✅Подписаться на рассылку✅')
    unsb = telebot.types.KeyboardButton('❌Отписаться с рассылки❌')
    back = telebot.types.KeyboardButton('⬅️Назад⬅️')
    markup.add(sb, unsb, back)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '✅Подписаться на рассылку✅')
def subscribe(message):
    add_subscriber(message.chat.id)
    bot.send_message(message.chat.id, '✅Вы успешно подписались на рассылку!')

@bot.message_handler(func=lambda message: message.text == '❌Отписаться с рассылки❌')
def unsubscribe(message):
    remove_subscriber(message.chat.id)
    bot.send_message(message.chat.id, '❌Вы успешно отписались с рассылки!')

@bot.message_handler(commands=['send'])
def send_news(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ У вас нет прав на выполнение этой команды.")
        return
    
    text = message.text.partition(' ')[2].strip()
    if not text:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, укажите сообщение после команды /send.")
        return

    subscribers = load_subscribers()
    success = 0
    fail = 0

    for user_id in subscribers:
        try:
            bot.send_message(user_id, f"📰 {text}")
            success += 1
        except:
            fail += 1

    bot.send_message(message.chat.id, f"📤 Рассылка завершена. Успешно: {success}, ошибок: {fail}")



@bot.message_handler(func=lambda message: message.text == '⬅️Назад⬅️')
def handle_back_button(message):
    menu(message)



bot.polling()
