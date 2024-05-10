import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = ('Чтобы узнать цену валюты, отправьте сообщение боту в формате:\n'
            '<имя валюты, цену которой хочете узнать> '
            '<имя валюты, в которой хотите узнать цену> '
            '<количество первой валюты>\n'
            'Например: доллар рубль 10\n'
            'Используйте команду /values, чтобы увидеть все доступные валюты.')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = 'Доступные валюты: доллар, евро, рубль.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        base, quote, amount = message.text.split(' ')
        amount = float(amount)
        price = CurrencyConverter.get_price(base, quote, amount)
        bot.send_message(message.chat.id, f'Цена {amount} {base} в {quote} составляет {price}')
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя: {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Неизвестная ошибка: {e}')

if __name__ == '__main__':
    bot.polling(none_stop=True)
