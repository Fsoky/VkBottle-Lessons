## [VkBottle Bot [ 1 ] | Структура и декораторы](https://www.youtube.com/watch?v=9OulU1HnVQY)
__Автор показывает основную структуру кода и рассказывает о нескольких декораторах__

*Код:* Из модуля VkBottle импортируются два класса: `Bot` и `Message`, из файла config импортируется переменная `token`, это необязательно так как автор хотел спрятать свой токен, вы же можете указать токен напрямую в коде. Три декоратора для обработки сообщений:

`message` - обрабатывает личные сообщения и сообщения в беседе \
`private_message` - обрабатывает личные сообщения \
`chat_message` - обрабатывает сообщения беседы

Каждый декоратор может принимать аргументы, смотрите в [оф. документации](https://github.com/vkbottle/vkbottle/).

Аргументированные функции. Для работы с такими функциями, необходимо передать аргумент, пример: `text=["/buy <item>"]`. То есть открыть "ёлочки" `<>` и записать туда параметр, теперь нужно в самих параметрах функции указать параметр. Пример можете посмотреть [здесь](https://github.com/vkbottle/vkbottle/blob/master/examples/high-level/easy_bot.py) или в [этом ролике](https://www.youtube.com/watch?v=9OulU1HnVQY)
```py
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
```