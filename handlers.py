from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import mocks


def get_my_masters_btns():
    my_masters = mocks.get_masters()
    inline_keyboard = []
    for master in my_masters:
        inline_keyboard.append([InlineKeyboardButton(text=master, callback_data=master)])
    return inline_keyboard

