## [VkBottle Bot [ 4 ] | Стейты и загрузчики](https://youtu.be/fx_1VSSiNOw)
__Работа со стейтами и загрузчиками__

### Стейты

*Код:* Из `vkbottle_types` импортируем класс BaseStateGroup, и из корня импортируем CtxStorage, он понадобится для хранения информации. \
Создаем класс с любым разумным названием и указываем *желаемые* атрибуты,
создаем обычную функцию и в декоратор передаем параметр `lev`, в него записываем желаемое слово, которое будет активировать цепочку, то есть это *отправная точка*.

Чтобы установить стейт, нужно прописать `await bot.state_dispenser.set(message.peer_id, Class.YOUR_STATE)`, передаем *peer_id* и *атрибут класса*. То есть мы говорим, что от сюда нужно будет прыгнуть в *эту точку (YOUR_STATE)*. Также в конце функции возвращаем какой-либо текст, это вместо `await message.answer()`, как я понял, это нужно для того, чтобы не *заглючил* стейт \
Дальше создаем еще одну функцию и передаем параметр `state`, в него передаем атрибут, который указали раннее.

Чтобы сохранить текст пользователя, который он напишет, воспользуемся `CtxStorage`,
он у меня объявлен в переменной `ctx`, так что обращаюсь к переменной и указываю метод `set`, здесь нам нужно передать *желаемый* атрибут и значение этому атрибуту, в нашем случае `message.text`.

С остальными стейтами также, в последнем стейте вы можете к примеру вывести все данные в чат или занести в базу данных. Чтобы завершить последний стейт, просто верните какой-либо текст *return*

```py
from vkbottle.bot import Bot, Message
from vkbottle_types import BaseStateGroup
from vkbottle import CtxStorage

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


bot.run_forever()
```


### Загрузчики (uploaders)

Из корня модуля импортируем классы загрузчиков, [см. в документации](https://github.com/vkbottle/vkbottle/blob/master/docs/tools/uploaders.md). \
Чтобы работать с загрузчиком, нужно иницилизировать его класс и передать ему API, `bot.api`. У каждого загрузчика есть метод `upload`, с помощью которого, вы сможете без проблем загрузить файлы.

```py
from vkbottle import PhotoMessageUploader, DocMessagesUploader, VoiceMessageUploader
```

Заносим класс в переменную, обращаемся к переменной и обращаемся к методу `upload`,
к примеру, если мы хотим загрузить фотку в сообщения, достаточно всего лишь передать ее название (или путь к ней). Но, если вы хотите загрузить документ в сообщения, то нужно будет указывать название *(title)*, сам файл и peer_id *message.peer_id*. Подробней смотреть в документации или в видео.

```py
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
```