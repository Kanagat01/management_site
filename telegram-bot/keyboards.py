from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


btn1 = KeyboardButton("Изменить ФИО")
btn2 = KeyboardButton("Изменить количество опросов в неделю\n(от 1 до 5)")
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(btn1).add(btn2)

cancel = KeyboardButton("Отмена")
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel.add(cancel)

def create_rating_keyboard(callback_prefix: str) -> InlineKeyboardMarkup:
    inline_btn1 = InlineKeyboardButton("😫", callback_data=f"{callback_prefix}_1")
    inline_btn2 = InlineKeyboardButton("😔", callback_data=f"{callback_prefix}_2")
    inline_btn3 = InlineKeyboardButton("😐", callback_data=f"{callback_prefix}_3")
    inline_btn4 = InlineKeyboardButton("🙂", callback_data=f"{callback_prefix}_4")
    inline_btn5 = InlineKeyboardButton("😁", callback_data=f"{callback_prefix}_5")
    inline_btn6 = InlineKeyboardButton("😍", callback_data=f"{callback_prefix}_6")
    kb = InlineKeyboardMarkup()
    kb.row(inline_btn1, inline_btn2, inline_btn3, inline_btn4, inline_btn5, inline_btn6)
    return kb

kb_rate_comp = create_rating_keyboard("rate_comp")
kb_rate_colleague = create_rating_keyboard("rate_colleague")