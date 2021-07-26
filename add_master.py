import requests
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler, CommandHandler

from decorators import debug_decorator as debug_decorator
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

    if submit_new_master(mock=mocks.send_new_master, master=master_name):
        logger.info(f"User ID:{update.message.from_user.id} added master '{master_name}'.")
        return done(update, context)
    else:
        update.message.reply_text(text=f"Мастер не найден. Давайте попробуем снова.")
        return MASTER_ADD


@debug_decorator
def submit_new_master(mock=mocks.send_new_master, master='undefined') -> bool:
    #
    # TODO: code for sending user's input to API goes here
    #
    # post-request for getting master's id
    # if no master found, throw 404
    # else append this id to user's list

    # TODO: PLEASE REFACTOR THIS (magic numbers (urls), separate get/set logic)
    check_id = requests.get('http://127.0.0.1:8000/client/clients/add_master/get_id/',
                        json={"nickname": master}).json()
    if not check_id:
        return False
    else:
        user_info = requests.get('http://127.0.0.1:8000/client/clients/add_master/123123123').json()
        if check_id not in user_info['master']:
            user_info['master'].append(check_id)
        requests.put('http://127.0.0.1:8000/client/clients/add_master/123123123',
                     json=user_info)
        return True


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
