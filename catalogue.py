from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler, CommandHandler
import typing

import mocks


def get_category_keyboard(update: Update, context: CallbackContext):
    inline_keyboard = get_categories_buttons()
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    if update.message:
        update.message.reply_text(text="Доступные категории:", reply_markup=reply_markup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Доступные категории:", reply_markup=reply_markup)


def catalogue_branch_query_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    category = ''

    # TODO: handling different requests in separate functions

    if query.data.split('_')[0] == "CATREQ":
        category = query.data.split('_')[1]

    inline_keyboard = get_masters_buttons(category)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Мастера в этой категории:", reply_markup=reply_markup)


# TODO: refactor duplicate code below

def get_masters_buttons(category) -> typing.List:
    masters = mocks.get_category_masters(category)
    masters_buttons = []
    for master in masters:
        masters_buttons.append(InlineKeyboardButton(text=master, callback_data=f"MASTERSREQ_{master}"))
    row_length = 5
    inline_keyboard = [masters_buttons[i:i + row_length] for i in range(0, len(masters_buttons), row_length)]
    return inline_keyboard


def get_categories_buttons() -> typing.List:
    categories = mocks.get_catalogue_categories()
    categories_buttons = []
    for cat in categories:
        categories_buttons.append(InlineKeyboardButton(text=cat, callback_data=f"CATREQ_{cat}"))
    row_length = 5
    inline_keyboard = [categories_buttons[i:i + row_length] for i in range(0, len(categories_buttons), row_length)]
    return inline_keyboard

