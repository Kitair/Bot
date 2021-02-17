from flask import Flask, request
import telebot
import os

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handlers(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет!')

@bot.message_handlers(commands=['help'])
def help(message):
    res = '/courses - список курсов \n' \
          '/planning - расписание курсов'
    bot.reply_to(message, res)

@bot.message_handlers(commands=['help'])
def courses(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    with open('courses.txt', 'r') as file:
        courses = [item.strip().split(',') for item in file]

        for title, link in courses:
            url_button = telebot.types.InlineKeyboardButton(text=title.strip(), url=link.strip(' \n'))
            keyboard.add(url_button)

    bot.send_message(message.chat.id, 'Привет, выбери кнопку', reply_markup=keyboard)

@bot.message_handlers(commands=['help'])
def planning(message):
    bot.reply_to(message, 'Это пока в разработке')


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot 17-02-2021", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://kitairbot.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
