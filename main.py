import telebot
from config import TOKEN
from extensions import ExchangeException, ExchangeHandler


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для получения курса валют ввудите команду в формате: \n <имя валюты> ' \
           '<в какую валюту конвертировать> <количество переводимой валюты>\n' \
           'Для вывода списка доступной валюты введите команду /values'
    # вернуть содержимое text вместе с отправленным сообщением
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    text += '\n'.join(currency.keys())
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convertion(message: telebot.types.Message):
    try:
        # переводим строку в список по пробелам
        values = message.text.split(' ')

        if len(values) != 3:
            raise ExchangeException('Нужно ввести три параметра')
        # разбираем список на переменные
        quote, base, amount = values
        total_base = ExchangeHandler.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # сразу умножаем на количество
        text = f'Цена за {amount} {quote} в {base} - {round(total_base * float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
