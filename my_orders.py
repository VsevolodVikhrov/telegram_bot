import re
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import mocks


def get_my_orders_keyboard(update: Update, context: CallbackContext):
    """
    В зависимости от вызова функции с парметра update либо query будет по разному доставаться user.id,
    а так же используя разные методы для отрисовки клавиатуры, используя функцию get_my_orders_buttons
    """
    if update.message:
        user = update.message.from_user
        keyboard = get_my_orders_buttons(user.id)
        if isinstance(keyboard, str):
            update.message.reply_text(text=keyboard)
        else:
            update.message.reply_text(text="Мои брони:", reply_markup=keyboard)
    else:
        query = update.callback_query
        query.answer()
        user = query.from_user
        query.edit_message_text(text="Мои брони:", reply_markup=get_my_orders_buttons(user.id))


def get_my_orders_buttons(user_id: int):
    """
    Функция проверяет список заказов, если заказы есть строит и возвращает клавиатуру/список с заказами,
    если список пустой возврщается сообщение: "У вас еще нет заказов".
    """
    orders = mocks.get_orders(user_id)
    inline_keyboard = []
    if bool(orders):
        for order in orders:
            inline_keyboard.append([InlineKeyboardButton(text=order, callback_data=f'mrdr%chosen_order__{order}')])
        keyboard = InlineKeyboardMarkup(inline_keyboard)
    else:
        keyboard = 'У вас еще нет заказов'
    return keyboard


def choose_order_inline(update: Update, context: CallbackContext):
    """
    QueryHandler для обработки всех callback_data в данной фиче ветке "Мои брони".
    Используя regex извлекается название заказа и в зависимости от метк в callback_data вызываются
    соответсвующие функции обработчики.
    """
    query = update.callback_query
    query.answer()
    pushed_btn = query.data
    '(.+)__'
    order = re.search(r'__(.+)', pushed_btn).group(1)
    if 'chosen_order' in pushed_btn:
        get_order_info(query, order)
    elif 'approve_delete' in pushed_btn:
        approve_delete(update, context)
        get_my_orders_keyboard(update, context)
    else:
        key = pushed_btn[:-len(order)]
        function = {
            'mrdr%back_to_my_orders__': get_my_orders_keyboard,
            'mrdr%delete_order__': ask_delete_order,
            'mrdr%decline_delete__': get_my_orders_keyboard,
        }
        function[key](update, context)


def get_order_info(query, order):
    """
    Функция для вывода информации о заказе и отрисовке клавиатуры с 2 вариантами нажатия "Отменить заказ"
    или "Вернуться к списку заказов"
    """
    order_info = mocks.get_order(order)
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton(text='Отменить заказ', callback_data=f'mrdr%delete_order__{order}')])
    inline_keyboard.append([InlineKeyboardButton(text='Вернуться к списку заказов',
                                                 callback_data=f'mrdr%back_to_my_orders__{order}')])
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(text=f'Your master : {order_info[0]}\n'
                                 f'Your chosen service: {order}\n'
                                 f'Price : {order_info[1]}\n'
                                 f'Date : {order_info[2]}\n'
                                 f'Time: {order_info[3]}',
                            reply_markup=reply_markup
                            )


def ask_delete_order(update, contex):
    """
    Функция для обработки запроса "Удалить мастера" отрисовывает клавиатуру с 2 кнопками "Да" и "Нет"
    """
    query = update.callback_query
    query.answer()
    order = re.search(r'__(.+)', query.data).group(1)
    keyboard = [
            [InlineKeyboardButton(text="Да", callback_data=f"mrdr%approve_delete__{order}"),
             InlineKeyboardButton(text="Нет", callback_data=f"mrdr%decline_delete__{order}")],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"Вы действительно хотите удалить {order}?", reply_markup=reply_markup)


def approve_delete(update, context):
    """
    Фунцкия обработки подтверждения удаления заказа
    """
    print('delete')

