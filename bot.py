import asyncio,re
from dotenv import load_dotenv
from os import getenv
from main import torrent2link
from aiogram import Bot,Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

load_dotenv(".env")
token="7733043091:AAGMiqkDRxKfwwFwjWHaMV6ew-dC5jy5rPk"
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
        
async def on_startup(app: web.Application):
    await bot.set_webhook("https://torrent2link.onrender.com/webhook")

def main():
    # Create aiohttp application
    app = web.Application()
    
    # Register webhook handler
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_handler.register(app, path="/webhook")
    
    # Setup application
    setup_application(app, dp, bot=bot)
    
    # Add startup callback
    app.on_startup.append(on_startup)
    
    # Add health check endpoint
    async def health_check(request):
        return web.Response(text="OK")
    app.router.add_get("/health", health_check)
    
    # Run app (Render requires port 10000)
    web.run_app(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()
