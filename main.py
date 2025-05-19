from aiogram import Bot, Dispatcher, Router, F
import logging
import asyncio
from app.config import TOKEN
from aiogram.types import Message, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton,  ReplyKeyboardMarkup, CallbackQuery
from app.handlers import router
from app.database.models import async_main
from app.database import requests as rq
from app.bot_instance import bot, dp



# taskkill /F /IM python.exe
# this is to stop if bot is running in multiple terminals

# This is to sync with github
"""git add .
git commit -m "Your commit message here"
git push origin main"""


async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)
    # print("Bot is running!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

# Cities are in english need to change on russian, length of a description
# check try except in send with buttons
# when i pressed show all locked till last but didnt click next so no listings wasnt sent, than directly pressed sort by price and only onle listing was sent, from two, than no more listings was sent
# in guidance about adding listing i need to add how long title description... should be

