from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler
import re
from decorators import get_data_source


# блок обработки и отображения инлайн клавы со списком мастеров
def get_my_masters_keyboard(update: Update, context: CallbackContext):
    """В зависимости от места вызова функции выполняется одна из веток,
    отображает клавиатуру"""
    inline_keyboard = get_my_masters_btns()
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    if update.message:
        update.message.reply_text(text="Мои мастера:", reply_markup=reply_markup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Мои мастера:", reply_markup=reply_markup)


@get_data_source
def get_my_masters_btns(source):
    """Возвращает кнопки с мастерами пользователя в клавиатуру"""
    my_masters = source.get_masters()
    inline_keyboard = []
    for master in my_masters:
        inline_keyboard.append([InlineKeyboardButton(text=master, callback_data=f"m%{master}_chosen_master")])
    return inline_keyboard


def masters_branch_query_handler(update: Update, context: CallbackContext):
    """Обработчик callback_data инлайн кнопок для вызова соответствующих функций"""
    query = update.callback_query
    query.answer()
    pushed_btn = query.data
    if "chosen_master" in pushed_btn:
        master = re.search(r"%(.+)_chosen", pushed_btn).group(1)
        get_master_skills_keyboard(query, master)
    elif "back_to_my_masters" in pushed_btn:
        get_my_masters_keyboard(update, context)
    elif "skill_is" in pushed_btn:
        get_calendar_keyboard(query, pushed_btn)
    elif "delete_master" in pushed_btn:
        ask_delete_master(update, context)
    elif "approve_delete" in pushed_btn:
        delete_master(update, context)
    elif "_dt__" in pushed_btn:
        get_time_keyboard(query, pushed_btn)


# блок обработки и отображения инлайн клавы с услугами мастера
def get_master_skills_keyboard(query, master):
    """Отображает клавиатуру"""
    inline_keyboard = get_master_skills_btns(master)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Услуги мастера:", reply_markup=reply_markup)


@get_data_source
def get_master_skills_btns(master, source):
    """Возвращает кнопки со скиллами мастера в клавиатуру"""
    skills = source.get_skills(master)
    inline_keyboard = []
    for skill in skills:
        inline_keyboard.append([InlineKeyboardButton(text=skill, callback_data=f"m%{master}_skill_is_{skill}")])
    inline_keyboard.append([InlineKeyboardButton(text="Удалить мастера", callback_data=f"m%delete_master_{master}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="m%back_to_my_masters")])
    return inline_keyboard


# блок обработки и отображения илнайн клавы с удалением мастера
def ask_delete_master(update, context):
    """Отображает клавиатуру"""
    query = update.callback_query
    query.answer()
    master = re.search(r"delete_master_(.+)", query.data).group(1)
    keyboard = [
            [InlineKeyboardButton(text="Да", callback_data=f"m%approve_delete_{master}"),
             InlineKeyboardButton(text="Нет", callback_data=f"m%{master}_chosen_master")],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"Вы действительно хотите удалить {master}?", reply_markup=reply_markup)


def delete_master(update, context):
    # TODO запрос в БД на удаление
    print("deleted")


# блок обработки и отображения инлайн клавы с календарем на услугу
def get_calendar_keyboard(query, master_and_skill):
    """Отображает клавиатуру"""
    master = re.search(r"m%(.+)_skill_is_", master_and_skill).group(1)
    skill = re.search(r"_skill_is_(.+)", master_and_skill).group(1)
    inline_keyboard = get_calendar_btns(master, skill)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Доступные даты:", reply_markup=reply_markup)


@get_data_source
def get_calendar_btns(master, skill, source):
    """Возвращает кнопки с календарем мастера в клавиатуру"""
    dates = source.get_dates(master, skill)
    date_buttons = []
    for date in dates:
        date_buttons.append(InlineKeyboardButton(text=date, callback_data=f"m%{master}_mstr_{skill}_skl_{date}_dt__"))
    row_length = 5
    inline_keyboard = [date_buttons[i:i + row_length] for i in range(0, len(date_buttons), row_length)]
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data=f"m%{master}_chosen_master")])
    return inline_keyboard


# блок обработки и отображения инлайн клавы с доступным временем для записи на услугу
def get_time_keyboard(query, master_and_skill_and_date):
    """Отображает клавиатуру"""
    master = re.search(r"%(.+?)_mstr", master_and_skill_and_date).group(1)
    skill = re.search(r"mstr_(.+?)_skl", master_and_skill_and_date).group(1)
    date = re.search(r"skl_(.+?)_dt", master_and_skill_and_date).group(1)
    inline_keyboard = get_time_btns(master, skill, date)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Доступное время:", reply_markup=reply_markup)


@get_data_source
def get_time_btns(master, skill, date, source):
    """Возвращает кнопки со временем в клавиатуру"""
    times = source.get_times(master, skill, date)
    time_buttons = []
    for time in times:
        time_buttons.append(InlineKeyboardButton(text=time, callback_data=f"m%{master}_mstr_{skill}_skl_{date}_dt_{time}"))
    row_length = 5
    inline_keyboard = [time_buttons[i:i + row_length] for i in range(0, len(time_buttons), row_length)]
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data=f"m%{master}_skill_is_{skill}")])  #назад к календарю
    return inline_keyboard


