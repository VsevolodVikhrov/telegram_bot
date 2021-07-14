from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler

import main
import mocks
MASTER_ADD, MASTER_CHECK = range(2)

# TODO: i guess this file will also contain a function handling
# TODO: adding masters via external link









def get_add_master(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(text="Введите ник мастера, чтобы добавить его себе в список:")
    return MASTER_ADD

    # TODO: getting user's input in a way that all commands won't be read as a username, but is this even necessary?
    # updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex("/start"), callback=start_screen))


def send_new_master(update: Update, context: CallbackContext) -> int:
    print('22')
    master_name = update.message.text

    # code for sending the username to the server goes here

    if mocks.send_new_master(master_name):
        return done(update, context)
    else:
        update.message.reply_text(text=f"Мастер не найден. Давайте попробуем снова.")
        return MASTER_CHECK


def wrong_username(update: Update, context: CallbackContext) -> int:
    master_name = update.message.text
    if mocks.send_new_master(master_name):
        done(update, context)
    else:
        return MASTER_CHECK


def done(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(text=f"Мастер добавлен!")
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(text=f"Операция отменена.")
    return ConversationHandler.END


conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters=Filters.regex(main.add_master_btn), callback=get_add_master)],
        states={
            MASTER_ADD: [
                MessageHandler(filters=Filters.text & ~Filters.command, callback=send_new_master)
            ],
            MASTER_CHECK: [
                MessageHandler(filters=Filters.text & ~Filters.command, callback=wrong_username)
            ],
        },
        fallbacks=[MessageHandler(filters=Filters.regex('cancel'), callback=cancel)]
)
