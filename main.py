import telebot

from config import TOKEN, currency
from extensions import Convertor, CurrencyException, UserDB

bot = telebot.TeleBot(TOKEN)
db = UserDB()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = r'''Вызовите команду /set
для выбора валюты для конвертации.
По умолчанию переводим  рубли в доллары.
Введите сумму.
    '''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['set'])
def set(message: telebot.types.Message):
    markup = telebot.types.InlineKeyboardMarkup()
    for vol, form in currency.items():
        button = telebot.types.InlineKeyboardButton(text=vol, callback_data=f'val1 {form}')
        markup.add(button)
    bot.send_message(chat_id=message.chat.id, text='Выберите валюту из которой будем\
 конвертировать', reply_markup=markup)
    markup = telebot.types.InlineKeyboardMarkup()
    for vol, form in currency.items():
        button = telebot.types.InlineKeyboardButton(text=vol, callback_data=f'val2 {form}')
        markup.add(button)
    bot.send_message(chat_id=message.chat.id, text='Выберите валюту в которую будем\
 конвертировать', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    v, vn = call.data.split()
    user_id = call.message.chat.id
    if v == "val1":
        db.change_from(user_id, vn)
        # vals[1] = (vn, vals[1][1])
    if v == "val2":
        db.change_to(user_id, vn)
    pair = db.get_pair(user_id)
        # vals[1] = (vals[1][0], vn)
    # bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f"Конвертируем из\
    #     {vals[1][0]} в {vals[1][1]}, укажите сумму")
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f"Конвертируем из\
 {pair[0]} в {pair[1]}, укажите сумму")


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    pair = db.get_pair(message.chat.id)
    values = [*pair, message.text.strip()]
    try:
        total = Convertor.get_price(values)
    except CurrencyException as e:
        bot.reply_to(message, f'Невозможно обработать сумму - {e}')
    else:
        text = f'{values[2]} {values[0]} равно {total} {pair[1]}'
        bot.reply_to(message, text)
    # values = message.text
    # try:
    #     result = Convertor.get_price(values)
    # except CurrencyException as e:
    #     bot.reply_to(message, f'Невозможно обработать сумму - {e}')
    # else:
    #     text = f'{values} {vals[1][0]} равно {result} {vals[1][1]}'
    #     bot.reply_to(message, text)


bot.polling(none_stop=True, interval=0)


