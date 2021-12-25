from typing import Tuple

from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule

from custom_rules import Permission

bot = Bot("TOKEN")
bot.labeler.custom_rules["permission"] = Permission


@bot.on.message(CommandRule("kick", ["/", "?"], 2))
async def handler(message: Message, args: Tuple[str]):
	await message.answer(f"{args[0]}")


# Если поставить эту функцию ниже sticker_handler - она не будет работать.
@bot.on.message(sticker=55350)
async def happy(message: Message):
	await message.answer("Happy New Year 🌲")


@bot.on.message(attachment="sticker")
async def sticker_handler(message: Message):
	await message.answer(f"Sticker ID: {message.attachments[0].sticker.sticker_id}")


@bot.on.message(func=lambda message: len(message.text) < 5)
async def text_handler(message: Message):
	await message.answer("Message less 5 symbols")


@bot.on.message(permission=1, text="debug")
async def debug_handler(message: Message):
	await message.answer("This function only for developers")


@bot.on.message(permission=403923317, text="debug2")
async def debug2_handler(message: Message):
	await message.answer("This function only for developers")


bot.run_forever()