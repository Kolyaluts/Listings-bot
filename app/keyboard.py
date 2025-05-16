from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton,  ReplyKeyboardMarkup, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

admin_reply_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🏡 Просмотр объектов")],
    [KeyboardButton(text="📢 Продажа"),
     KeyboardButton(text="📞 Связаться с агентом")],
    [KeyboardButton(text="Добавить объект")]
], resize_keyboard=True)


main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🏡 Просмотр объектов")],
    [KeyboardButton(text="📢 Продажа"),
     KeyboardButton(text="📞 Связаться с агентом")]
], resize_keyboard=True)


cities = [
    "🏙️ Podgorica",
    "🌊 Budva",
    "⛵ Kotor",
    "✈️ Tivat",
    "🏖️ Bar",
    "🏰 Herceg Novi",
    "🏝️ Ulcinj",
    "🏛️ Cetinje",
    "⛰️ Nikšić"
]

city_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏙️ Подгорица", callback_data="city_podgorica"),
     InlineKeyboardButton(text="🌊 Будва", callback_data="city_budva")],
    [InlineKeyboardButton(text="⛵ Котор", callback_data='city_kotor'),
     InlineKeyboardButton(text="✈️ Тиват", callback_data="city_tivat")],
    [InlineKeyboardButton(text="🏖️ Бар", callback_data="city_bar"),
     InlineKeyboardButton(text="🏰 Херцег-Нови", callback_data="city_herceg novi")],
    [InlineKeyboardButton(text="🌍 Другое", callback_data="other")]
])

agents_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💬 Чат с агентом",
                          url="https://t.me/@yurluts83")]
])


sort_price_other = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Цена 🏷️", callback_data=f"sort_price_other"),
     InlineKeyboardButton(text="Все объявления", callback_data=f"show_all_other")]
])


sort_price_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="€0 - €100,000", callback_data="price_0_100000"),
     InlineKeyboardButton(text="€100,000 - €300,000", callback_data="price_100000_300000")],
    [InlineKeyboardButton(text="€300,000 и выше", callback_data="price_300000_above"),
     InlineKeyboardButton(text="Other price", callback_data="other_price")]
]
)


async def builser_price(tuples):
    added_cats = set()
    keyboard = InlineKeyboardBuilder()
    for t in tuples:
        if t[2] <= 100000 and "0_100000" not in added_cats:
            keyboard.button(
                text="€0 - €100,000", callback_data="price_0_100000")
            added_cats.add("0_100000")

        if t[2] > 100000 and t[2] <= 300000 and "100000_300000" not in added_cats:
            keyboard.button(
                text="€100,000 - €300,000", callback_data="price_100000_300000")
            added_cats.add("100000_300000")
        if t[2] >= 300000 and "300000_above" not in added_cats:
            keyboard.button(
                text="€300,000 and above", callback_data="price_300000_above")
            added_cats.add("300000_above")
    return keyboard.adjust(2).as_markup()


cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Cancel", callback_data='cancel')]
])


listing_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="◀️ Назад", callback_data='◀️ Назад'),
        InlineKeyboardButton(text="➡️ Далее", callback_data='➡️ Далее')]
])


listing_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="◀️ Назад", callback_data='◀️ Назад')]
])
