import config
from bot_class import PizzaBot

from telebot import TeleBot

bot = TeleBot(config.TOKEN)
handler = PizzaBot()


@bot.message_handler()
def answer(message):
    bot.send_message(message.chat.id, handler.get_response(message.chat.id, message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
