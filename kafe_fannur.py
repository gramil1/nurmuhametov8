import telebot, os
import datetime
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

# Словарь для хранения меню (замените на ваше меню)
menu = {
    "1. Кофе": {"price": 150, "description": "Классический кофе"},
    "2. Чай": {"price": 100, "description": "Черный чай"},
    "3. Кофе латте": {"price": 200, "description": "Кофе латте"},
    "4. Сэндвич": {"price": 250, "description": "Сэндвич с ветчиной и сыром"},
}

#bot = telebot.TeleBot(TOKEN)

# Функция для отображения меню
def display_menu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for item in menu:
        keyboard.add(telebot.types.KeyboardButton(item))
    keyboard.add(telebot.types.KeyboardButton("Оформить заказ"))
    bot.send_message(message.chat.id, "Меню:", reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    display_menu(message)

@bot.message_handler(func=lambda message: True)
def handle_menu_choice(message):
    if message.text in menu:
        item_name = message.text
        item_data = menu[item_name]
        bot.send_message(message.chat.id, f"{item_name}: {item_data['description']} - {item_data['price']} руб.")
    elif message.text == "Оформить заказ":
        # Здесь должен быть код для обработки заказа.
        bot.send_message(message.chat.id, "Введите номер заказа")
        bot.register_next_step_handler(message, process_order)
    else:
      bot.send_message(message.chat.id, "Не найдено. Пожалуйста, выберите из меню.")



def process_order(message):
  try:
    order_number = int(message.text)
    bot.send_message(message.chat.id, f"Ваш заказ: {order_number}")
  except ValueError:
    bot.send_message(message.chat.id, "Некорректный номер заказа. Пожалуйста, введите число.")


bot.polling(none_stop=True, interval=0)
