from aiogram.types import BufferedInputFile
from aiogram.types import InputFile, InputMediaPhoto
import aiohttp
from PIL import Image
from io import BytesIO


async def formating(t):
    formatted_string = f"""
🏡 **Объявление о недвижимости:** 

🔹 **Название**: *{t[0]}*  
📜 **Описание**: _{t[1]}_  
💶 **Цена**: *{t[2]} €*  
📍 **Адрес**: `{t[3].capitalize()}`  
🌆 **Город**: *{t[4].capitalize()}*

Для получения дополнительной информации или для записи на просмотр, не стесняйтесь обращаться!
"""
    images = []
    for i in range(10):
        image_data = t[5 + i]  # Get image from database (raw bytes)
        if image_data:
            # Wrap bytes in BufferedInputFile
            buffered_file = BufferedInputFile(
                image_data, filename=f"image{i+1}.jpg")

            if i == 0:
                # First image gets the caption
                images.append(InputMediaPhoto(
                    media=buffered_file, caption=formatted_string, parse_mode="Markdown"))
            else:
                images.append(InputMediaPhoto(media=buffered_file))

    if images:
        return images


async def download_image(url):
    """Downloads and resizes an image to prevent exceeding Telegram's size limit."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                image_bytes = await response.read()

                # Resize before storing
                return resize_image(image_bytes)
    return None


def resize_image(image_bytes, max_size=(1200, 1200)):
    """Resizes an image while maintaining aspect ratio to reduce file size."""
    image = Image.open(BytesIO(image_bytes))
    image.thumbnail(max_size)  # Resize while maintaining aspect ratio

    # Convert resized image back to bytes
    img_byte_arr = BytesIO()
    # Adjust quality as needed
    image.save(img_byte_arr, format="JPEG", quality=70)
    return img_byte_arr.getvalue()
