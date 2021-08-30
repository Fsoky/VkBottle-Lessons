from vkbottle.bot import Bot, Message
from config import token

bot = Bot(token=token)


@bot.on.message(text="userinfo") # Обрабатывает сообщения лс и в беседе
async def message_handler(message: Message):
	user = await bot.api.users.get(message.from_id)
	await message.answer(f"Hello, {user[0].first_name} {user[0].last_name}")


@bot.on.private_message(text=["menu", "help"]) # Обрабатывает лс
async def private_message_handler(message: Message):
	await message.answer("Test")


@bot.on.chat_message() # Обрабатывает сообщения в беседе
async def chat_message_handler(message: Message):
	await message.answer(message.text)


@bot.on.private_message(text=["/buy <item>", "/buy"])
async def store_handler(message: Message, item=None):
	if item is not None:
		await message.answer(f"Was Bought: {item}")
	else:
		await message.answer("Вы указали аргумент пустым...")


bot.run_forever()