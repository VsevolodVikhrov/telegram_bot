from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler
import re
from decorators import get_data_source
from data_processing import make_order, get_service_info


# блок обработки и отображения инлайн клавы со списком мастеров
def get_my_masters_keyboard(update: Update, context: CallbackContext):
    """В зависимости от места вызова функции выполняется одна из веток,
    отображает клавиатуру"""
    inline_keyboard = get_my_masters_btns(update)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    if update.message:
        update.message.reply_text(text="Мои мастера:", reply_markup=reply_markup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Мои мастера:", reply_markup=reply_markup)


@get_data_source
def get_my_masters_btns(update, source):
    """Возвращает кнопки с мастерами пользователя в клавиатуру"""
    user = update.effective_user
    my_masters = source.get_masters(user)
    inline_keyboard = []
    for master in my_masters:
        inline_keyboard.append([InlineKeyboardButton(text=master['nickname'], callback_data=f"m%{master['id']}_chosen_master")])
    return inline_keyboard


def masters_branch_query_handler(update: Update, context: CallbackContext):
    """Обработчик callback_data инлайн кнопок для вызова соответствующих функций"""
    query = update.callback_query
    query.answer()
    pushed_btn = query.data
    if "chosen_master" in pushed_btn:
        get_master_skills_keyboard(query, pushed_btn)
    elif "back_to_my_masters" in pushed_btn:
        get_my_masters_keyboard(update, context)
    elif "service_is" in pushed_btn:
        get_service_description(query, pushed_btn)
    elif "skill_is" in pushed_btn:
        get_calendar_keyboard(query, pushed_btn)
    elif "delete_master" in pushed_btn:
        ask_delete_master(update, context)
    elif "approve_delete" in pushed_btn:
        delete_master(update, pushed_btn)
        get_my_masters_keyboard(update, context)
    elif "_dt_" in pushed_btn:
        get_time_keyboard(query, pushed_btn)
    elif "_dtm_" in pushed_btn:
        ask_booking_confirm(query, pushed_btn)
    elif "_dtmc" in pushed_btn:
        user = update.effective_user
        make_order(user, pushed_btn)
        update.callback_query.edit_message_text(text='Время успешно забронировано')


# блок обработки и отображения инлайн клавы с услугами мастера
def get_master_skills_keyboard(query, callback_data):
    """Отображает клавиатуру"""
    master_id = re.search(r"%(.+)_chosen", callback_data).group(1)
    inline_keyboard = get_master_skills_btns(master_id)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Услуги мастера:", reply_markup=reply_markup)


@get_data_source
def get_master_skills_btns(master_id, source):
    """Возвращает кнопки со скиллами мастера в клавиатуру"""
    skills = source.get_skills(master_id)
    inline_keyboard = []
    for skill in skills:
        inline_keyboard.append([InlineKeyboardButton(text=skill['title'], callback_data=f"m%{master_id}_service_is_{skill['id']}")])
    inline_keyboard.append([InlineKeyboardButton(text="Удалить мастера", callback_data=f"m%delete_master_{master_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="m%back_to_my_masters")])
    return inline_keyboard


def get_service_description(query, callback_data):
    master_id = re.search(r"m%(.+)_service_is_", callback_data).group(1)
    skill_id = re.search(r"_service_is_(.+)", callback_data).group(1)
    text = get_service_info(skill_id)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Показать доступные даты", callback_data=f"m%{master_id}_skill_is_{skill_id}")],
        [InlineKeyboardButton(text='Назад', callback_data=f"m%{master_id}_chosen_master")]
    ])
    query.edit_message_text(text=text, reply_markup=reply_markup)


# блок обработки и отображения илнайн клавы с удалением мастера
def ask_delete_master(update, context):
    """Отображает клавиатуру"""
    query = update.callback_query
    query.answer()
    master_id = re.search(r"delete_master_(.+)", query.data).group(1)
    keyboard = [
            [InlineKeyboardButton(text="Да", callback_data=f"m%approve_delete_{master_id}"),
             InlineKeyboardButton(text="Нет", callback_data=f"m%{master_id}_chosen_master")],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"Вы действительно хотите удалить мастера?", reply_markup=reply_markup)


@get_data_source
def delete_master(update, master_to_delete, source):
    user = update.effective_user
    master_id = re.search(r"m%approve_delete_(.+)", master_to_delete).group(1)
    source.remove_master(user, master_id)


# блок обработки и отображения инлайн клавы с календарем на услугу
def get_calendar_keyboard(query, master_and_skill):
    """Отображает клавиатуру"""
    master_id = re.search(r"m%(.+)_skill_is_", master_and_skill).group(1)
    skill_id = re.search(r"_skill_is_(.+)", master_and_skill).group(1)
    inline_keyboard = get_calendar_btns(master_id, skill_id)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Доступные даты:", reply_markup=reply_markup)


@get_data_source
def get_calendar_btns(master_id, skill_id, source):
    """Возвращает кнопки с календарем мастера в клавиатуру"""
    dates = source.get_dates(master_id, skill_id)
    date_buttons = []
    for date in dates:
        date_buttons.append(InlineKeyboardButton(text=date.strftime('%d.%m'), callback_data=f"m%{master_id}_mstr_{skill_id}_skl_{date}_dt_"))
    row_length = 5
    inline_keyboard = [date_buttons[i:i + row_length] for i in range(0, len(date_buttons), row_length)]
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data=f"m%{master_id}_chosen_master")])
    return inline_keyboard


# блок обработки и отображения инлайн клавы с доступным временем для записи на услугу
def get_time_keyboard(query, master_and_skill_and_date):
    """Отображает клавиатуру"""
    master_id = re.search(r"%(.+?)_mstr", master_and_skill_and_date).group(1)
    skill_id = re.search(r"mstr_(.+?)_skl", master_and_skill_and_date).group(1)
    date = re.search(r"skl_(.+?)_dt", master_and_skill_and_date).group(1)
    inline_keyboard = get_time_btns(master_id, skill_id, date)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text="Доступное время:", reply_markup=reply_markup)


@get_data_source
def get_time_btns(master_id, skill_id, date, source):
    """Возвращает кнопки со временем в клавиатуру"""
    datetimes = source.get_times(master_id, skill_id, date)
    time_buttons = []
    for datetime in datetimes:
        time_buttons.append(InlineKeyboardButton(text=datetime.strftime('%H:%M'), callback_data=f"m%{master_id}_mstr_{skill_id}_skl_{datetime}_dtm_"))
    row_length = 5
    inline_keyboard = [time_buttons[i:i + row_length] for i in range(0, len(time_buttons), row_length)]
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data=f"m%{master_id}_skill_is_{skill_id}")])
    return inline_keyboard


def ask_booking_confirm(query, callback_data):
    master_id = re.search(r"%(.+?)_mstr", callback_data).group(1)
    skill_id = re.search(r"mstr_(.+?)_skl", callback_data).group(1)
    time_info = re.search(r" (.+):", callback_data).group(1)
    datetime = re.search(r"skl_(.+)_dtm_", callback_data).group(1)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Забронировать", callback_data=f"m%{master_id}_mstr_{skill_id}_skl_{datetime}_dtmc")],
        [InlineKeyboardButton(text='Назад', callback_data=f"m%{master_id}_skill_is_{skill_id}")]
    ])
    query.edit_message_text(text=f"Забронировать на {time_info}?", reply_markup=reply_markup)
