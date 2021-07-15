from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler, CommandHandler
import typing

import mocks


def get_category_keyboard(update: Update, context: CallbackContext):
    """Shows a catalogue of categories to add a master from."""
    inline_keyboard = get_buttons(callback_type="CATREQ", positions=mocks.get_catalogue_categories())
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    if update.message:
        update.message.reply_text(text="Доступные категории:", reply_markup=reply_markup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Доступные категории:", reply_markup=reply_markup)


def catalogue_branch_query_handler(update: Update, context: CallbackContext):
    """Handles updates after pressing buttons in catalogue menu."""
    query = update.callback_query
    query.answer()
    category = ''

    # TODO: handling different requests in separate functions

    if query.data.split('_')[0] == "CATREQ":
        category = query.data.split('_')[1]

    inline_keyboard = get_buttons(callback_type="MASTERSREQ", positions=mocks.get_category_masters(category))
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Мастера в этой категории:", reply_markup=reply_markup)


def get_buttons(callback_type: str, positions: typing.List) -> typing.List:
    """Gets a list of master/catalogue positions and processes them into a keyboard."""
    buttons = []
    for position in positions:
        buttons.append(InlineKeyboardButton(text=position, callback_data=f"{callback_type}_{position}"))
    row_length = 5
    inline_keyboard = [buttons[i:i + row_length] for i in range(0, len(buttons), row_length)]
    return inline_keyboard
