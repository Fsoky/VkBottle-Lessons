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

### Клавиатура (payload)

*Код:* В класс `Text` передаем второй аргумент *payload*, как словарь. Теперь можем указать второй декоратор и в параметр `payload` передать словарь, который указали ранее. Теперь если мы нажмем на кнопку, нас перекинет в функцию где указан этот *payload*.

В коде ниже, если мы нажмем на кнопку *Store*, нас перекинет в функцию `store_handler`, а там будет кнопка *back*, нажав на нее, нас перекинет обратно в функцию `handler`

```py
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from config import token

bot = Bot(token)


@bot.on.private_message(text="menu")
@bot.on.private_message(payload={"cmd": "menu"})
async def handler(message: Message):
	keyboard = Keyboard(one_time=True).add(Text("Store", {"cmd": "store"}))
	await message.answer("MENU", keyboard=keyboard)


@bot.on.private_message(text="store")
@bot.on.private_message(payload={"cmd": "store"})
async def store_handler(message: Message):
	keyboard = Keyboard(one_time=True).add(Text("Back", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
	await message.answer("STORE", keyboard=keyboard)


bot.run_forever()
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