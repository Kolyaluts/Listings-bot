from io import BytesIO
from app.bot_instance import bot
from aiogram import Router, F, types, Bot
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton,  ReplyKeyboardMarkup, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
import app.keyboard as kb
import json
from app.database import requests as rq
import base64
from aiogram.types import InputFile, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.database.requests import add_listing, get_listings, get_by_city_price, get_user, reg_user
from app.config import TOKEN
import aiohttp
from aiogram.types import BufferedInputFile
from app.photos import formating, download_image, resize_image
import app.texts as t
from PIL import Image
from io import BytesIO
router = Router()

index = 0


async def send_with_buttons(callback, state):
    try:
        state_data = await state.get_data()
        listings_list = state_data['dict_listings']
        index = state_data['index']
        if not listings_list:
            await callback.message.answer("Error1")
            return None
        if index is None:
            await callback.message.answer("Error2")
            return None

        try:
            t = listings_list[index]
        except:
            await callback.message.answer("Больше нет объявлений")
            await state.clear()
            return

        listing = await formating(t)

        if listing:
            await callback.message.answer_media_group(listing)
            # Need to continue with kb
            await callback.message.answer(text="Выберите опцию:", reply_markup=kb.listing_kb)

    except:
        await callback.message.answer("Больше нет объявлений")


class Listing_list(StatesGroup):
    dict_listings = State()
    index = State()


class Flat(StatesGroup):
    title = State()
    description = State()
    price = State()
    city = State()
    adres = State()
    img_qty = State()
    image1 = State()
    image2 = State()
    image3 = State()
    image4 = State()
    image5 = State()
    image6 = State()
    image7 = State()
    image8 = State()
    image9 = State()
    image10 = State()


class City(StatesGroup):
    name = State()


class City_by_price(StatesGroup):
    city = State()


class User_reg(StatesGroup):
    name = State()
    email = State()
    tg_id = State()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if not await get_user(message.from_user.id):
        await state.set_state(User_reg.name)
        await message.answer(text=t.reg_name, reply_markup=ReplyKeyboardRemove())
        return
    keyboard = kb.admin_reply_kb if message.from_user.username in {
        'kolya_luts', 'yurluts83'} else kb.main_kb

    await message.answer(text=t.welcome_text, reply_markup=keyboard)


@router.message(User_reg.name)
async def user_name_reg(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.answer(text=t.reg_email)
    await state.set_state(User_reg.email)


@router.message(User_reg.email)
async def user_email_reg(message: Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    await state.set_state(User_reg.tg_id)
    await state.update_data(tg_id=message.from_user.id)
    user_state = await state.get_data()
    await reg_user(user_state)
    await message.answer("Вы зарегистрированы.")
    await start(message, state)


@router.message(F.text == "📢 Продажа")
async def sell_property(message: Message):
    await message.answer(text=t.sale_text, reply_markup=kb.agents_kb)


@router.message(F.text == "📞 Связаться с агентом")
async def contact_agent(message: Message):
    await message.answer(text=t.contact_agent, reply_markup=kb.agents_kb)


@router.message(F.text == "Добавить объект")
async def add_listings(message: Message, state: FSMContext):
    await state.set_state(Flat.title)
    await message.answer(text="Теперь вы можете ввести все данные.", reply_markup=ReplyKeyboardRemove())
    await message.answer("Введите заголовок, 30 символов.", reply_markup=kb.cancel_kb)


@router.message(Flat.title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.lower().strip())
    await state.set_state(Flat.description)
    await message.answer("Введите описание, 800 символов.")


@router.message(Flat.description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.lower().strip())
    await state.set_state(Flat.price)
    await message.answer("Введите цену.")


@router.message(Flat.price)
async def add_price(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price=message.text.lower().strip())
        await state.set_state(Flat.adres)
        await message.answer("Введите адрес, 30 символов")
    else:
        await message.answer("Цена должна быть числом, пожалуйста, введите снова.")


@router.message(Flat.adres)
async def add_adres(message: Message, state: FSMContext):
    await state.update_data(adres=message.text.lower().strip())
    await state.set_state(Flat.city)
    await message.answer("Введите город, 40 символов.")


@router.message(Flat.city)
async def add_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.lower().strip())
    await state.set_state(Flat.img_qty)
    await message.answer(text="📷 Введите количество изображений (от 1 до 10).")


@router.message(Flat.img_qty)
async def img_qty(message: Message, state: FSMContext):
    await state.update_data(img_qty=message.text.lower().strip())
    await state.set_state(Flat.image1)
    await message.answer("Отправьте столько изображений, сколько вы указали.")


photos_list = []
images_dict = {}


@router.message(F.photo, StateFilter(Flat.image1))
async def add_img1(message: Message, state: FSMContext, bot: Bot):
    global photos_list, images_dict
    photo = message.photo[-1]
    photos_list.append(photo)
    image_data = await state.get_data()
    if len(photos_list) != int(image_data['img_qty']):
        await message.answer(text="Обработка...")
    else:

        for idx, image in enumerate(photos_list, start=1):
            file_id = image.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path

            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

            image_bytes = await download_image(file_url)
            if image_bytes is None:
                await message.answer(f"⚠️ Failed to download image {idx}.")
                continue  # Skip this image if download fails

            images_dict[f"image{idx}"] = image_bytes  # Store image as bytes

        state_data = await state.get_data()
        await add_listing(state_data, images_dict)
        keyboard = kb.admin_reply_kb if message.from_user.username in {
            'kolya_luts', 'yurluts83'} else kb.main_kb
        await message.answer(text="Объявление добавлено.", reply_markup=keyboard)

        await state.clear()
        images_dict.clear()
        photos_list.clear()
        return None


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text="You canceled adding listing", reply_markup=kb.admin_reply_kb)


@router.message(F.text == "🏡 Просмотр объектов")
async def listings(message: Message):
    global index
    index = 0
    await message.answer(text="""🗺 Выберите город для просмотра объявлений:

🌆 Выберите город, в котором вы ищете недвижимость.""", reply_markup=kb.city_kb)


@router.callback_query(F.data.startswith("city_"))
async def show_listings(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    city_price = callback.data[5:]
    await state.set_state(City_by_price.city)
    await state.update_data(city=callback.data[5:])

    listings_list = await get_listings(city_price)
    if listings_list:
        count = len(listings_list)
        keyboard = kb.sort_price_other
        await callback.message.answer(f"✅ Найдено {count} объявлений в {city_price.capitalize()}.\nХотите отсортировать их по цене?", reply_markup=keyboard)

    else:
        await callback.message.answer(f"🚫 В {city_price.capitalize()} пока нет доступных объявлений. Попробуйте позже! 🏡")


@router.callback_query(F.data == "other")
async def other_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название города (латиницей), например: Podgorica", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await state.set_state(City_by_price.city)


@router.message(City_by_price.city)
async def search_by_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.lower().strip())
    city_state = await state.get_data()
    city_price = city_state['city']

    if not city_price:
        await message.answer("⚠️ Пожалуйста, сначала выберите город!", reply_markup=kb.city_kb)
        return  # Stop execution if city is missing

    listings_list = await get_listings(city_price)
    if listings_list:
        count = len(listings_list)
        await message.answer(f"✅ Найдено {count} объявлений в {city_price.capitalize()}.\n"
                             "Хотите отсортировать их по цене?", reply_markup=kb.sort_price_other)
    else:
        await message.answer(f"🚫 В {city_price.capitalize()} нет объявлений с такой ценой на данный момент. Пожалуйста, попробуйте позже! 🏡")


@router.callback_query(F.data == "sort_price_other")
async def sent_sorted(callback: CallbackQuery, state: FSMContext):
    try:
        city_state = await state.get_data()
        city = city_state['city']
    except:
        await callback.message.answer("⚠️ Пожалуйста, сначала выберите город!", reply_markup=kb.city_kb)
        return  # Stop execution if city is missing

    listings_list = await get_listings(city)

    if not listings_list:
        return await callback.message.answer("Error")
    keyboard = await kb.builser_price(listings_list)
    await callback.message.answer(text="🔹 Выберите опцию:",
                                  reply_markup=keyboard)


@router.callback_query(F.data == "price_0_100000")
async def price_1(callback: CallbackQuery, state: FSMContext):
    try:
        city_state = await state.get_data()
        city_price = city_state['city']
    except:
        await callback.message.answer("⚠️ Пожалуйста, сначала выберите город!", reply_markup=kb.city_kb)
        return  # Stop execution if city is missing

    listings_list = await get_by_city_price(city_price, 0, 100000)
    if listings_list:
        await state.set_state(Listing_list.index)
        await state.update_data(dict_listings=listings_list, index=0)
        await send_with_buttons(callback, state)
    else:
        await callback.message.answer(f"🚫 В {city_price.capitalize()} нет объявлений с такой ценой на данный момент. Пожалуйста, попробуйте позже! 🏡")


@router.callback_query(F.data == "price_100000_300000")
async def price_2(callback: CallbackQuery, state: FSMContext):
    try:
        city_state = await state.get_data()
        city_price = city_state['city']
    except:
        await callback.message.answer("⚠️ Пожалуйста, сначала выберите город!", reply_markup=kb.city_kb)
        return  # Stop execution if city is missing
    listings_list = await get_by_city_price(city_price, 100000, 300000)
    if listings_list:
        await state.set_state(Listing_list.index)
        await state.update_data(dict_listings=listings_list, index=0)
        await send_with_buttons(callback, state)
    else:
        await callback.message.answer(f"🚫 В {city_price.capitalize()} нет объявлений с такой ценой на данный момент. Пожалуйста, попробуйте позже! 🏡")


@router.callback_query(F.data == "price_300000_above")
async def price_3(callback: CallbackQuery, state: FSMContext):
    try:
        city_state = await state.get_data()
        city_price = city_state['city']
    except:
        await callback.message.answer("⚠️ Пожалуйста, сначала выберите город!", reply_markup=kb.city_kb)
        return  # Stop execution if city is missing

    listings_list = await get_by_city_price(city_price, 300000, 9999999999999)
    if listings_list:
        await state.set_state(Listing_list.index)
        await state.update_data(dict_listings=listings_list, index=0)
        await send_with_buttons(callback, state)
    else:
        await callback.message.answer(f"🚫 В {city_price.capitalize()} нет объявлений с такой ценой на данный момент. Пожалуйста, попробуйте позже! 🏡")


@router.callback_query(F.data.startswith("show_all_"))
async def send_all(callback: CallbackQuery, state: FSMContext):
    try:
        city_state = await state.get_data()
        city_price = city_state['city']
    except:
        await callback.message.answer("⚠️ Пожалуйста, сначала выберите город!", reply_markup=kb.city_kb)
        return  # Stop execution if city is missing
    listings_list = await get_listings(city_price)
    await state.set_state(Listing_list.index)
    await state.update_data(dict_listings=listings_list, index=0)
    await send_with_buttons(callback, state)


@router.callback_query(F.data == "➡️ Далее")
async def next_listing(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        index = state_data['index']
        
    except KeyError:
        await callback.message.answer("⚠️ Пожалуйста, сначала выберите город!", reply_markup=kb.city_kb)
        return
    await state.update_data(index=index + 1)
    await send_with_buttons(callback, state)


@router.callback_query(F.data == "◀️ Назад")
async def back_to_main(callback: CallbackQuery):
    keyboard = kb.admin_reply_kb if callback.from_user.username in {
        'kolya_luts', 'yurluts83'} else kb.main_kb

    await callback.message.answer(text=t.welcome_text, reply_markup=keyboard)
