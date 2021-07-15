import logging
import config
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CallbackQueryHandler
import my_masters, my_orders, add_master, catalogue


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


catalogue_btn = "Каталог"
add_master_btn = "Добавить мастера"
my_orders_btn = "Мои брони"
my_masters_btn = "Мои мастера"


def start_screen(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(f'User {user.username} with id:  {user.id} has joined ')
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
        one_time_keyboard=True,
        resize_keyboard=True, # параметр для пересчета размера кнопок
    )
    update.message.reply_text(text="Привет, друг!", reply_markup=reply_markup)  # отправка на апи телеги сообщения и клавы


def main():

    updater = Updater(token=config.BOT_TOKEN, use_context=True)   # подключение к боту
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex("/start"), callback=start_screen))  # добавление обработчика сообщений в очередь, в параметрах условие для выполнения и действие, которое выполнится
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex(my_masters_btn), callback=my_masters.get_my_masters_keyboard))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex(my_orders_btn), callback=my_orders.get_my_orders_keyboard))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=my_masters.masters_branch_query_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=my_orders.choose_order_inline))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex(my_orders_btn), callback=my_orders.get_my_orders_keyboard))

    
    updater.start_polling()   # начало стучания по апи телеги
    updater.idle()            # бесконечный цикл простукивания


if __name__ == '__main__':    # точка входа
    main()
