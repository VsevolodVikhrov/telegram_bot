from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler, CommandHandler
from json import JSONDecodeError
import requests
import typing

from decorators import debug_decorator as debug_decorator
import mocks

URLS = {
    "catalogue": "http://127.0.0.1:8000/client/categories/",
    "client_info": "http://127.0.0.1:8000/client/add_master/",
}


def get_category_keyboard(update: Update, context: CallbackContext) -> None:
    """Shows a catalogue of categories to add a master from."""
    inline_keyboard = get_catalogue_buttons(row_length=2, callback_type="CATREQ",
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
def get_catalogue_categories(mock=mocks.get_catalogue_categories) -> typing.List:
    """Auxiliary function for getting a list of available services categories."""
    return requests.get(URLS["catalogue"]).json()


def catalogue_branch_query_handler(update: Update, context: CallbackContext) -> None:
    """Handles updates after pressing buttons in catalogue menu."""
    query = update.callback_query
    query.answer()

    # TODO: implement this as a dict
    # TODO: show a list of master's services

    if "CAT%CATREQ" in query.data:
        get_masters_list(query, query.data.split('_')[1])
    elif "CAT%CATBACK" in query.data:
        get_category_keyboard(update, context)
    elif "CAT%MASTERSREQ" in query.data:
        confirmation_message(query, query.data.split('_')[1], query.data.split('_')[2], query.data.split('_')[3])
    elif "CAT%CONFREQY" in query.data:
        add_master(query, query.data.split('_')[1], query.data.split('_')[2], str(update.effective_user.id))
    elif "CAT%CONFREQN" in query.data:
        get_masters_list(query, query.data.split('_')[1])


def get_masters_list(query, category: str) -> None:
    """Gets a list of masters providing services in the selected category."""
    try:
        inline_keyboard = get_master_buttons(row_length=5, callback_type="MASTERSREQ", category=category,
                                             positions=get_category_masters(mocks.get_category_masters, category))
    except JSONDecodeError:
        inline_keyboard = [[InlineKeyboardButton(text="Назад", callback_data="CAT%CATBACK")]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        query.edit_message_text(text="В данной категории нет мастеров.", reply_markup=reply_markup)
        return

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Мастера в этой категории:", reply_markup=reply_markup)


def confirmation_message(query, category: str, master: str, master_name: str) -> None:
    """Asks the user whether they want to confirm adding the master."""
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Да", callback_data=f"CAT%CONFREQY_{master}_{master_name}"),
            InlineKeyboardButton(text="Нет", callback_data=f"CAT%CONFREQN_{category}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text=f"Вы действительно хотите добавить мастера {master_name}?", reply_markup=reply_markup)


def add_master(query, master: str, master_name: str, user_id: str) -> None:
    """Retrieves user's info and appends new master to it."""
    user_info = get_user_info(user_id)
    if master not in user_info['master']:
        user_info['master'].append(master)
    requests.patch(URLS['client_info'] + user_id, json=user_info)
    query.edit_message_text(text=f"Мастер {master_name} добавлен!")


@debug_decorator
def get_category_masters(category_id: str, mock=mocks.get_category_masters) -> typing.List:
    """Auxiliary function for retrieving a list of masters who provide services under the specified category."""
    return requests.get(URLS["catalogue"] + category_id).json()


def get_catalogue_buttons(row_length: int, callback_type: str, positions: typing.Dict) -> typing.List:
    """Gets a list of catalogue positions and processes them into a keyboard."""
    buttons = []
    for position in positions:
        buttons.append(InlineKeyboardButton(text=position['category_name'],
                                            callback_data=f"CAT%{callback_type}_{position['id']}"))
    inline_keyboard = [buttons[i:i + row_length] for i in range(0, len(buttons), row_length)]
    return inline_keyboard


def get_master_buttons(row_length: int, callback_type: str, category: str, positions: typing.Dict) -> typing.List:
    """Gets a list of master positions and processes them into a keyboard."""
    buttons = []
    for position in positions:
        buttons.append(InlineKeyboardButton(text=position['nickname'],
                                            callback_data=f"CAT%{callback_type}_{category}_"
                                                          f"{position['id']}_{position['nickname']}"))
    inline_keyboard = [buttons[i:i + row_length] for i in range(0, len(buttons), row_length)]
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="CAT%CATBACK")])
    return inline_keyboard


def get_user_info(user_id: str) -> typing.Dict:
    """Auxiliary function for getting JSON-data of the user for further appendage of a new master to master list."""
    return requests.get(URLS['client_info'] + user_id).json()
