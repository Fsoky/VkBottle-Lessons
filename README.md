# VkBottle Lessons
Исходный код с роликов по модулю VkBottle

## [VkBottle | Работа с методами](https://www.youtube.com/watch?v=KmfLUZb8GPQ)
__В этом видео-ролике автор рассказывает, как работать с методами вк-апи с помощью модуля VkBottle__

*Код:* Импортируется два модуля (asyncio, из VkBottle класс API). Asyncio понадобится для запуска асинхронных функций, а класс API для взаимодействия с методами Vk-API. В переменной `friend` получаем список своих друзей и в цикле перебираем список с ID'шниками друзей. Переменная `user`: получаем детальную информацию о пользователе, `status`: получаем статус пользователя. Выводим имя, фамилию и статус пользователя в консоль. `asyncio.run(handler())` - запускаем асинхронную функцию.

```py
import asyncio
from vkbottle import API

api = API("YOUR_TOKEN")


async def handler():
	friends = await api.friends.get()

	for friend in friends.items:
		user = await api.users.get(friend)
		status = await api.status.get(friend)
		
		print(f"{user[0].first_name} {user[0].last_name} | {status.text}")


asyncio.run(handler())
```

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

## [VkBottle [ 2 ] | Клавиатура, карусели](https://youtu.be/ed0sJjs-9YY)
__Демонстрация работы с клавиатурой и каруселью__

### Клавиатура

*Код:* Из корня модуля VkBottle импортируем классы: `Keyboard`, `KeyboardButtonColor`, `Text`, `OpenLink`, `Location`. Последние три класса отвечают за *тип кнопки*, все типы кнопок можете посмотреть в [оф. документации Vk-API](https://vk.com/dev/bots_docs_3?f=4.%2BBot%2Bkeyboards), или посмотреть документацию [VkBottle Keyboard.md](https://github.com/vkbottle/vkbottle/blob/master/docs/tools/keyboard.md). Также импортируется аттрибут `EMPTY_KEYBOARD`, *возвращает пустую клавиатуру (удаляет)*

В переменной `keyboard` иницилизируем класс `Keyboard(one_time=False, inline=False)`

C помощью метода `.add(action, color=None)` можно добавить кнопку в один ряд. \
Метод `.row()` позволяет перейти на следующую строчку. \
Прикрепить клавиатуру можно указав параметр `keyboard` в методе `answer()`.

```py
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Location, EMPTY_KEYBOARD

from config import token

bot = Bot(token)


@bot.on.private_message(text="menu")
async def handler(message: Message):
	keyboard = Keyboard()

	keyboard.add(Text("RED"), color=KeyboardButtonColor.NEGATIVE)
	keyboard.add(Text("GREEN"), color=KeyboardButtonColor.POSITIVE)
	keyboard.add(Text("BLUE"), color=KeyboardButtonColor.PRIMARY)
	keyboard.add(Text("WHITE"))

	keyboard.row()

	keyboard.add(OpenLink("https://vk.com/fsoky", "Vk group"))
	keyboard.add(Location())

	await message.answer("Keyboard", keyboard=keyboard)


bot.run_forever()
```

Еще один способ работы с клавиатурой *(builder)*. \
Открываем кортеж, и записываем класс `Keyboard()`, дальше можем обращаться к методам класса. Такой способ аналогичен варианту выше. Подробнее смотреть в [оф. документации VkBottle](https://github.com/vkbottle/vkbottle/blob/master/docs/tools/keyboard.md)

```py
keyboard = (
	Keyboard(inline=True)
	.add(Text("RED"), color=KeyboardButtonColor.NEGATIVE)
	.add(Text("GREEN"), color=KeyboardButtonColor.POSITIVE)
	.add(Text("BLUE"), color=KeyboardButtonColor.PRIMARY)
	.add(Text("WHITE"))
	.row()
	.add(OpenLink("https://vk.com/fsoky", "Vk group"))
	.add(Location())
)

await message.answer("Keyboard", keyboard=keyboard)
```

### Карусели
__Простая работа с каруселью *(template)*__

*Код:* Из корня модуля `VkBottle` импортируем функцию `template_gen` и класс `TemplateElement`. В функцию *template_gen* заносим класс *TemplateElement(title, description, photo_id, buttons, action)*. "Подробнее" смотреть в [оф. документации VkBottle](https://github.com/vkbottle/vkbottle/blob/master/docs/tools/template.md) или смотреть про карусели в [оф. документации Vk-API](https://vk.com/dev/bot_docs_templates?f=5.1.%2BCarousels).

Чтобы указать кнопки в элементе, нужно воспользоваться существующими классами `Keyboard` и указать тип кнопки, к примеру `Text`, в конце получаем JSON объект клавиатуры с помощью метода `get_json()`. Прикрепить карусель можно указав параметр `template` в методе `answer()`.
 
```py
from vkbottle import Keyboard, KeyboardButtonColor, Text, template_gen, TemplateElement
```

```py
@bot.on.private_message(text="carousel")
async def carousel_handler(message: Message):
	keyboard = Keyboard().add(Text("Button"), color=KeyboardButtonColor.NEGATIVE)
	carousel = template_gen(
		TemplateElement(
			"Test title",
			"Description",
			"-203980592_457239029",
			keyboard.get_json()
		)
	)

	await message.answer("Carousel", template=carousel)
```
