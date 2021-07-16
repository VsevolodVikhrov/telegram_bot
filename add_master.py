from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler, CommandHandler

from main import reply_markup, btn_list, logger
import mocks

# keep this line instead of MASTER_ADD = 0 so that more menu points can be added later
MASTER_ADD = range(1)

# i guess this file will also contain a function handling
# TODO: adding masters via external link (deep-linking)


def get_new_master(update: Update, context: CallbackContext) -> int:
    """Starts the conversation where user adds a master to his list of masters."""
    update.message.reply_text(text="Введите ник мастера, чтобы добавить его себе в список.\n"
                                   "Для выхода введите /cancel.", reply_markup=ReplyKeyboardRemove())
    return MASTER_ADD


def send_new_master(update: Update, context: CallbackContext) -> int:
    """Sends user's input to API and handles API's response. """
    # handling the case when user sends a text that matches one of
    # button messages
    if update.message.text in btn_list.values():
        return cancel(update, context)

    # TODO: input validation?

    master_name = update.message.text

    if submit_new_master(master_name):
        logger.info(f"User ID:{update.message.from_user.id} added master '{master_name}'.")
        return done(update, context)
    else:
        update.message.reply_text(text=f"Мастер не найден. Давайте попробуем снова.")
        return MASTER_ADD


def submit_new_master(master_name: str) -> bool:
    #
    # TODO: code for sending user's input to API goes here
    #
    return mocks.send_new_master(master_name)


def done(update: Update, context: CallbackContext) -> int:
    """Ends the conversation."""
    update.message.reply_text(text=f"Мастер добавлен!", reply_markup=reply_markup)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Exits the conversation."""
    update.message.reply_text(text=f"Операция отменена.", reply_markup=reply_markup)
    return ConversationHandler.END


# handler for driver code's updater.handler
conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters=Filters.regex(btn_list['add_master_btn']), callback=get_new_master)],
        states={
            MASTER_ADD: [
                MessageHandler(filters=Filters.text & ~Filters.command, callback=send_new_master)
            ],
        },
        fallbacks=[
            CommandHandler(command='cancel', callback=cancel),
            ]
)
