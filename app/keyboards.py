from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.requests import get_user

user_categories = ["1-4","5-8","9-11"]

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='мойайди')],
    [KeyboardButton(text="моеимя")]
])

#user_button = InlineKeyboardMarkup(keyboard=[
#    [KeyboardButton(text="Узнать про себя")]
#])


async def user_categories_keyboard():
    categories_kb = InlineKeyboardBuilder()

    for category in user_categories:
        categories_kb.add(InlineKeyboardButton(text=category,callback_data=f"category_{category}"))
    return categories_kb.adjust(2).as_markup()

