import config
import handlers
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler


catalogue_btn = "Каталог"
add_master_btn = "Добавить мастера"
my_orders_btn = "Мои брони"
my_masters_btn = "Мои мастера"


def start_screen(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(  # Добавляем клаву
        keyboard=[  # добавляем на клаву кнопки
            [
                KeyboardButton(text=my_orders_btn),
                KeyboardButton(text=catalogue_btn),
            ],
            [
                KeyboardButton(text=add_master_btn),
                KeyboardButton(text=my_masters_btn)
            ]
        ],
        resize_keyboard=True  # параметр для пересчета размера кнопок
    )
    update.message.reply_text(text="Привет, друг!", reply_markup=reply_markup)  # отправка на апи телеги сообщения и клавы


def get_my_masters_keyboard(update: Update, context: CallbackContext):
    inline_keyboard = handlers.get_my_masters_btns()
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text(text="Мои мастера:", reply_markup=reply_markup)


def main():
    updater = Updater(token=config.BOT_TOKEN, use_context=True)   # подключение к боту
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex("/start"), callback=start_screen))  # добавление обработчика сообщений в очередь, в параметрах условие для выполнения и действие, которое выполнится
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex(my_masters_btn), callback=get_my_masters_keyboard))

    updater.start_polling()   # начало стучания по апи телеги
    updater.idle()            # бесконечный цикл простукивания


if __name__ == '__main__':    # точка входа
    main()
