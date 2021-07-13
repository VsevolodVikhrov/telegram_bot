from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler
import mocks
import re


# блок обработки и отображения инлайн клавы со списком мастеров
def get_my_masters_keyboard(update: Update, context: CallbackContext):
    inline_keyboard = get_my_masters_btns()
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    if update.message:
        update.message.reply_text(text="Мои мастера:", reply_markup=reply_markup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Мои мастера:", reply_markup=reply_markup)


def get_my_masters_btns():
    my_masters = mocks.get_masters()
    inline_keyboard = []
    for master in my_masters:
        inline_keyboard.append([InlineKeyboardButton(text=master, callback_data=f"{master}_chosen_master")])
    return inline_keyboard


#  обработчик нажатия на кнопку инлайн клавы с именем мастера
def masters_branch_query_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    pushed_btn = query.data
    if "chosen_master" in pushed_btn:
        master = pushed_btn[0:-14]
        get_master_skills_keyboard(query, master)
    elif "back_to_my_masters" in pushed_btn:
        get_my_masters_keyboard(update, context)
    elif "skill_is" in pushed_btn:
        get_calendar_keyboard(query, pushed_btn)
    elif "delete_master" in pushed_btn:
        ask_delete_master(update, context)
    elif "approve_delete" in pushed_btn:
        delete_master(update, context)
    elif "decline_delete" in pushed_btn:
        master = pushed_btn[15:]
        get_master_skills_keyboard(query, master)


# блок обработки и отображения инлайн клавы с услугами мастера
def get_master_skills_keyboard(query, master):
    inline_keyboard = get_master_skills_btns(master)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Услуги мастера:", reply_markup=reply_markup)


def get_master_skills_btns(master):
    skills = mocks.get_skills(master)
    inline_keyboard = []
    for skill in skills:
        inline_keyboard.append([InlineKeyboardButton(text=skill, callback_data=f"{master}_skill_is_{skill}")])
    inline_keyboard.append([InlineKeyboardButton(text="Удалить мастера", callback_data=f"delete_master_{master}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back_to_my_masters")])
    return inline_keyboard


# блок обработки и отображения илнайн клавы с удалением мастера
def ask_delete_master(update, context):
    query = update.callback_query
    query.answer()
    master = query.data[14:]
    keyboard = [
            [InlineKeyboardButton(text="Да", callback_data=f"approve_delete_{master}"),
             InlineKeyboardButton(text="Нет", callback_data=f"decline_delete_{master}")],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"Вы действительно хотите удалить {master}?", reply_markup=reply_markup)


def delete_master(update, context):
    print("deleted")


# блок обработки и отображения инлайн клавы с календарем на услугу
def get_calendar_keyboard(query, master_and_skill):
    master = re.search(r"(.+?)(?=_skill_is_)", master_and_skill).group(1)
    skill = re.search(r"skill_is_(.+)", master_and_skill).group(1)
    inline_keyboard = get_calendar_btns(master, skill)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Доступные даты:", reply_markup=reply_markup)


def get_calendar_btns(master, skill):
    dates = mocks.get_dates(master, skill)
    date_buttons = []
    for date in dates:
        date_buttons.append(InlineKeyboardButton(text=date, callback_data=f"{master}_{skill}_{date}_date"))
    row_length = 5
    inline_keyboard = [date_buttons[i:i + row_length] for i in range(0, len(date_buttons), row_length)]
    return inline_keyboard



