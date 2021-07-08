from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
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


def main():
    updater = Updater(token='1673248618:AAEpAdZVNcFsL10GTYNCh1NikdCI6tsgPBk', use_context=True)   # подключение к боту
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex("/start"), callback=start_screen))  # добавление обработчика сообщений в очередь, в параметрах условие для выполнения и действие, которое выполнится

    updater.start_polling()   # начало стучания по апи телеги
    updater.idle()            # бесконечный цикл простукивания


if __name__ == '__main__':    # точка входа
    main()
