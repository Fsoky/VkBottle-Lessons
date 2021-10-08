from vkbottle.bot import Bot, Message
from vkbottle_types import BaseStateGroup
from vkbottle import CtxStorage, PhotoMessageUploader, DocMessagesUploader, VoiceMessageUploader

from config import token

bot = Bot(token)
ctx = CtxStorage()


class RegData(BaseStateGroup):

	NAME = 0
	AGE = 1
	ABOUT = 2


@bot.on.message(lev="/reg")
async def reg_handler(message: Message):
	await bot.state_dispenser.set(message.peer_id, RegData.NAME)
	return "Введите ваше имя"


@bot.on.message(state=RegData.NAME)
async def name_handler(message: Message):
	ctx.set("name", message.text)
	await bot.state_dispenser.set(message.peer_id, RegData.AGE)
	return "Введите ваш возраст"


@bot.on.message(state=RegData.AGE)
async def age_handler(message: Message):
	ctx.set("age", message.text)
	await bot.state_dispenser.set(message.peer_id, RegData.ABOUT)
	return "Введите информацию о себе"


@bot.on.message(state=RegData.ABOUT)
async def about_handler(message: Message):
	name = ctx.get("name")
	age = ctx.get("age")
	about = message.text

	await message.answer(f"{name}\n{age}\n{about}")
	return "Регистрация прошла успешно"


@bot.on.message(text="up")
async def upload_handler(message: Message):
	"""Команда со второй половины видео"""

	photo_upd = PhotoMessageUploader(bot.api)
	doc_upd = DocMessagesUploader(bot.api)
	voice_upd = VoiceMessageUploader(bot.api)

	# Укажите ваши файлы, которые желаете загрузить

	photo = await photo_upd.upload("source.jpg")
	doc = await doc_upd.upload("title.txt", "source.txt", peer_id=message.peer_id)
	voice = await voice_upd.upload("title.wav", "source.wav", peer_id=message.peer_id)

	await message.answer(attachment=photo)
	await message.answer(attachment=doc)
	await message.answer(attachment=voice)


bot.run_forever()