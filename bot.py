import logging

from environs import Env
from telethon import TelegramClient, events


logger = logging.getLogger("SpellsBot")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)
logger.setLevel("INFO")


env = Env()
env.read_env()
TELEGRAM_API_ID = env.int("TELEGRAM_API_ID")
TELEGRAM_API_HASH = env.str("TELEGRAM_API_HASH")
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")


bot = TelegramClient("cnc", TELEGRAM_API_ID, TELEGRAM_API_HASH).start(
    bot_token=TELEGRAM_BOT_TOKEN
)


@bot.on(events.NewMessage(pattern="/start"))
async def handler(event):
    await event.reply("Hey!")


@bot.on(events.NewMessage(pattern="/list"))
async def handler(event):
    await event.reply("List of puppets")


@bot.on(events.NewMessage(pattern=r"\/execute (?P<cmd>.*)"))
async def handler(event):
    cmd = event.pattern_match.group("cmd")
    await event.reply(f"Let's execute some {cmd}")


logger.info("BOT DEPLOYED. Ctrl+C to terminate")
bot.run_until_disconnected()
