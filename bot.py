import telebot
from config import TOKEN, currencies, signs
from extensions import APIException, Convert

bot = telebot.TeleBot(TOKEN) # Создание объекта бота

@bot.message_handler(commands=['start', 'help']) # Обработчик команд /start и /help
def hello_message(message): # Функция отправки приветственного сообщения с инструкцией по использованию бота
    text = '''Привет, помогу с конвертацией валют! 👋
Введи данные в формате <конвертирую это> <в это> <в количестве> через пробел.
Например: *Доллар Рубль 1*

*Список валют по кнопке /values*
'''
    bot.send_message(message.chat.id, text, parse_mode='Markdown') # Отправка сообщения пользователю с форматированием Markdown

@bot.message_handler(commands=['values']) # Обработчик команды /values
def list_of_currencies(message):
    text = '📋 *Список доступных валют:*\n\n'
    text += "\n".join(currencies.keys()) # Вывод валют из словаря в файле config.py

    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(content_types=['text', ]) # Обработчик сообщений с текстом.
def convert(message):
    try:
        values = message.text.split(' ') # Достаем элементы из сообщения пользователя
        if len(values) != 3: # Проверка, чтобы было правильное кол-во элементов
            raise APIException('Неверное кол-во параметров')

        base, quote, amount = values # Назначение переменны для конвертации
        base, quote = base.capitalize(), quote.capitalize() # Возможность пользователя ввести данные в любом регистре
        result = Convert.get_price(base, quote, amount) # Получение результата конвертации с помощью класса Convert и функции get_price()

    except APIException as e: # Обработчик ошибок при проблеме с конвертацией
        bot.reply_to(message, f'⚠️ Произошла ошибка пользователя *{type(e).__name__}:*\n_{e}_', parse_mode='Markdown') # Отправка ответа на сообщение с типом ошибки и ее текстом

    except Exception as e: # Обработчик остальных ошибок
        bot.send_message(message.chat.id, f'⚠️ Произошла ошибка *{type(e).__name__}:*\n_{e}_', parse_mode='Markdown')

    else: # Если всё хорошо, отправка пользователю результата конвертации с округлением до 4-х символов после запятой
        text = f'''Конвертация *{base}* —> *{quote}*
Кол-во валюты: *{signs[base]}{amount}*

Итого: *{signs[base]}{amount} = {signs[quote]}{round(result, 4)}*
'''
        bot.send_message(message.chat.id, text, parse_mode='Markdown')

bot.polling(none_stop=True) # Запуск бота

