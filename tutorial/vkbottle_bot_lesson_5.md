## [VkBottle Bot [ 5 ] | Разделение кода](https://www.youtube.com/watch?v=YXFzX-CiQ_4)
__Разделение кода на файлы__

### Основной файл

*Код:* Из `vkbottle.bot` импортируем класс `Bot` и функцию `load_blueprints_from_package`. Создаем цикл для "обработки" директории с доп. файлами. \
Перед началом следовало создать папку, где будут храниться доп. файлы: `md blueprints`. В цикле обращаемся к методу `load` и передаем переменную *bot*.
В конце прописываем `bot.run_forever()`.

```py
from vkbottle.bot import Bot, load_blueprints_from_package

bot = Bot("TOKEN")
for bp in load_blueprints_from_package("blueprints"):
	bp.load(bot)

bot.run_forever()
```

### Дополнительные файлы (Команды для чата)

*Код:* Импортируем классы `Blueprint` и `Message` из `vkbottle.bot`, также дополнительно импортируем класс `VKAPIError` из корня *vkbottle*, и модуль `re` для регулярных выражений. *Класс Blueprint работает также, как и класс `Bot`* \
Создаем обычную функцию, которая будет служить командой для кика. Мы будем ее использовать так: */kick @ansqqq*, чтобы кикнуть пользователя с чата. Для того, чтобы получить ID пользователя необходимо достать его из такой строчки *(ссылки)*: [1234|ansqqq], для этого воспользуемся модулем `re` и простым регулярным выражением, которое позволит достать цифры: `re.findall(r"[0-9]+", member)[0]`. Дальше делаем небольшую обработку ошибки, можно сделать еще больше исключений, но это на ваше усмотрение. Обращаемся к *API*, к методу `messages.remove_chat_user`, передаем чат-ID и пользователя, которого желаем изгнать. В нашем случае это переменная *member*, которая хранит в себе ID пользователя. Готово.

```py
import re

from vkbottle.bot import Blueprint, Message
from vkbottle import VKAPIError

bp = Blueprint("Commands for chat")


@bp.on.chat_message(text=["/kick", "/kick <member>"])
async def kick_handler(message: Message, member=None):
	if member is None:
		await message.answer("Укажите пользователя")
	else:
		try:
			member = re.findall(r"[0-9]+", member)[0]
			await bp.api.messages.remove_chat_user(message.chat_id, int(member))
		except VKAPIError(15):
			await message.answer("Недостаточно прав...")
```

### Дополнительные файлы (Команды для личных сообщений)

*Код:* Из импортов оставим только классы `Blueprint` и `Message`. Создаем обычную функцию, которая будет служить обработкой математических операций. Обычный калькулятор, результат заносим в переменную *result*, и вне условий выводим сообщение в чат: `await message.answer(result)`. Также чтобы при вводе неучитывался регистр, стоит сделать так: `bp.vbml_ignore_case = True`.

```py
from vkbottle.bot import Blueprint, Message

bp = Blueprint("Commands for direct messages")
bp.vbml_ignore_case = True # Дает возможность неучитывать регистр (math, MaTh, MATH)


@bp.on.private_message(text=["math <a:int> <operator> <b:int>"])
async def math_handler(message: Message, a: int, operator, b: int):
	if operator == "+":
		result = a + b
	elif operator == "-":
		result = a - b
	elif operator == "/":
		result = a / b
	elif operator == "*":
		result = a * b
	else:
		result = "Wrong operator."

	await message.answer(result)
```
