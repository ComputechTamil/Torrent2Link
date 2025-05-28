import asyncio,re
from dotenv import load_dotenv
from os import getenv
from main import torrent2link
from aiogram import Bot,Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

load_dotenv(".env")
token=getenv("telegram_token")
bot=Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp=Dispatcher()
@dp.message(Command("start"))
async def welcome_message(message:Message):
    username=message.from_user.username or message.from_user.first_name
    await message.answer(f"Hello {username}! 👋 Welcome to Torrent2Link Bot.\nJust Send the Magnet Link I will Send the Direct Downloadable link!!")

MAGNET_REGEX = r"(magnet:\?xt=urn:btih:[a-zA-Z0-9]+[^ ]*)"
@dp.message()
async def handle_magnet(message: Message):
    match = re.search(MAGNET_REGEX, message.text)
    if match:
        magnet_link = match.group(1)
        await message.answer(
            f"🚀 <b>Direct Download Link:</b>\n\n"
            f"🔗 <a href='{torrent2link(magnet_link)}'>Click here to download</a>",
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    else:
        await message.answer(
            "⚠️ Please send a valid magnet link.\n\nExample:\n<code>magnet:?xt=urn:btih:123abc456def789...</code>",
            parse_mode="HTML")
async def main():
    print("Bot is running...")
    await dp.start_polling(bot)
if __name__=="__main__":
    asyncio.run(main())
