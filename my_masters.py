from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

import mocks


def get_my_masters_keyboard(update: Update, context: CallbackContext):
    inline_keyboard = get_my_masters_btns()
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text(text="Мои мастера:", reply_markup=reply_markup)


#  обработчик нажатия на кнопку инлайн клавы с именем мастера
def choose_master_inline(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=query.data)


def get_my_masters_btns():
    my_masters = mocks.get_masters()
    inline_keyboard = []
    for master in my_masters:
        inline_keyboard.append([InlineKeyboardButton(text=master, callback_data=master)])
    return inline_keyboard
