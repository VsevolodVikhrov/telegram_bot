from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler, CommandHandler
from json import JSONDecodeError
import requests
import typing

from decorators import debug_decorator as debug_decorator
import mocks

URLS = {
    "catalogue": "http://127.0.0.1:8000/client/categories/",
}


def get_category_keyboard(update: Update, context: CallbackContext):
    """Shows a catalogue of categories to add a master from."""
    inline_keyboard = get_buttons(row_length=2, callback_type="CATREQ",
                                  # positions argument function can't be called w/out passing `mock` argument
                                  positions=get_catalogue_categories(mock=mocks.get_catalogue_categories))
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    if update.message:
        update.message.reply_text(text="Доступные категории:", reply_markup=reply_markup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Доступные категории:", reply_markup=reply_markup)


@debug_decorator
def get_catalogue_categories(mock=mocks.get_catalogue_categories):
    """Auxiliary function for getting a list of available services categories."""
    return requests.get(URLS["catalogue"]).json()


def catalogue_branch_query_handler(update: Update, context: CallbackContext):
    """Handles updates after pressing buttons in catalogue menu."""
    query = update.callback_query
    query.answer()
    category = ''

    # TODO: handling different requests in separate functions

    if query.data.split('_')[0] == "CAT%CATREQ":
        category = query.data.split('_')[1]

    inline_keyboard = get_buttons(row_length=5, callback_type="MASTERSREQ",
                                  positions=get_category_masters(mocks.get_category_masters, str(category)))
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Мастера в этой категории:", reply_markup=reply_markup)


@debug_decorator
def get_category_masters(category_id, mock=mocks.get_category_masters):
    """Auxiliary function for retrieving a list of masters who provide services under the specified category."""
    try:
        masters = requests.get(URLS["catalogue"] + category_id).json()
    except JSONDecodeError:
        return [{
            'id': '0',
            'comment': 'В этой категории пока что нет мастеров.'
        }]
    return masters


def get_buttons(row_length: int, callback_type: str, positions: typing.Dict) -> typing.List:
    """Gets a list of master/catalogue positions and processes them into a keyboard."""
    buttons = []
    for position in positions:
        # because category names and master nicknames are stored under keys with different names and same indexes,
        # in field `text` we turn `position` dict into a list of keys, then get a value of the second (`name`) key
        buttons.append(InlineKeyboardButton(text=position[list(position)[1]],
                                            callback_data=f"CAT%{callback_type}_{position['id']}"))
    inline_keyboard = [buttons[i:i + row_length] for i in range(0, len(buttons), row_length)]
    return inline_keyboard
