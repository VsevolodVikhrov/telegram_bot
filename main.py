from logging import basicConfig, getLogger, INFO
import config
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CallbackQueryHandler, ConversationHandler
import my_masters, my_orders, add_master, catalogue


basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=INFO
)
logger = getLogger(__name__)

# add further buttons here so that exception handling in add_masters.py works
btn_list = {
    'catalogue_btn': "Каталог",
    'add_master_btn': "Добавить мастера",
    'my_orders_btn': "Мои брони",
    'my_masters_btn': "Мои мастера",
}

reply_markup = ReplyKeyboardMarkup(  # Добавляем клаву
        keyboard=[  # добавляем на клаву кнопки
            [
                KeyboardButton(text=btn_list['my_orders_btn']),
                KeyboardButton(text=btn_list['catalogue_btn']),
            ],
            [
                KeyboardButton(text=btn_list['add_master_btn']),
                KeyboardButton(text=btn_list['my_masters_btn'])
            ]
        ],
        resize_keyboard=True  # параметр для пересчета размера кнопок
    )


def start_screen(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Привет, друг!", reply_markup=reply_markup)  # отправка на апи телеги сообщения и клавы


def main() -> None:
    updater = Updater(token=config.BOT_TOKEN, use_context=True)   # подключение к боту
    updater.dispatcher.add_handler(add_master.conv_handler)
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex("/start"), callback=start_screen))  # добавление обработчика сообщений в очередь, в параметрах условие для выполнения и действие, которое выполнится
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex(btn_list['my_masters_btn']), callback=my_masters.get_my_masters_keyboard))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=my_masters.choose_master_inline))

    updater.start_polling()   # начало стучания по апи телеги
    updater.idle()            # бесконечный цикл простукивания


if __name__ == '__main__':    # точка входа
    main()
