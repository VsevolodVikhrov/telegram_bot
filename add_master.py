import requests
import typing
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler, CommandHandler

from decorators import debug_decorator as debug_decorator
from main import reply_markup, btn_list, logger
import mocks

# list of urls
URLS = {
    "get_master_id": 'http://127.0.0.1:8000/client/add_master/get_id/',
    "add_master": 'http://127.0.0.1:8000/client/add_master/',
}

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

    if submit_new_master(mock=mocks.send_new_master, master=master_name, user_id=str(update.message.from_user.id)):
        logger.info(f"User ID:{update.message.from_user.id} added master '{master_name}'.")
        return done(update, context)
    else:
        update.message.reply_text(text=f"Мастер не найден. Давайте попробуем снова.")
        return MASTER_ADD


@debug_decorator
def submit_new_master(user_id, mock=mocks.send_new_master, master='undefined') -> bool:
    master_id = get_master_id(master)
    if not master_id:
        return False
    else:
        user_info = get_user_info(user_id)
        if master_id not in user_info['master']:
            user_info['master'].append(master_id)
        requests.patch(URLS['add_master'] + user_id, json=user_info)
        return True


def get_master_id(master: str) -> typing.Dict:
    """Auxiliary function for getting master's ID for further appendage to user's master list."""
    return requests.get(URLS['get_master_id'], json={"nickname": master}).json()


def get_user_info(user_id: str) -> typing.Dict:
    """Auxiliary function for getting JSON-data of the user for further appendage of a new master to master list."""
    return requests.get(URLS['add_master'] + user_id).json()


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
