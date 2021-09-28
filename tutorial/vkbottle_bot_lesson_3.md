## [VkBottle Bot [ 3 ] | События сообщества и callback кнопка](https://youtu.be/hRTiOXwjxMw)
__Простой способ работы с событиями и callback кнопкной__

### События сообщества

*Переходим в свое сообщество* -> *Управление* -> *API usage* -> *LongPoll API* -> *Event types*, активируем нужные типы. К примеру *Group Join*, *Group Leave*

*Код:* Из корня модуля импортируем классы: *GroupEventType*, *GroupTypes*, *VKAPIError*. Последний класс понадобится для обработки ошибок. Все типы событий можно посмотреть в [оф. документации VK-API](https://vk.com/dev/groups_events).

```py
from vkbottle import GroupEventType, GroupTypes, VKAPIError
```

Прописываем новый декоратор `@bot.on.raw_event()`, передаем в него *GroupEventType.__GROUP_JOIN__* (обратите внимания, что тип записан верхнем регистром), указываем параметр `dataclass` и передаем класс *GroupTypes.__GroupJoin__*

Создаем асинхронную функцию с любым разумным названием, в параметры передаем `event: GroupTypes.GroupJoin`. В функции прописываем конструкцию *try except*, В блоке __*try*__ будем отправлять сообщение пользователю. В __*except*__ обратимся к классу *VKAPIError* и укажем номер ошибки *901*: `VKAPIError(901)`. Аналогично можно сделать и с ивентом *GroupLeave*

```py
@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
	try:
		await bot.api.messages.send(
			peer_id=event.object.user_id,
			message="Welcome to the club, buddy!",
			random_id=0
		)
	except VKAPIError(901):
		pass


@bot.on.raw_event(GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def group_leave_handler(event: GroupTypes.GroupLeave):
	try:
		await bot.api.messages.send(
			peer_id=event.object.user_id,
			message="So sorry...",
			random_id=0
		)
	except VKAPIError(901):
		pass
```

### Callback кнопка

*Код:* Импортируем из корня модуля классы: *Keyboard*, *Callback*, также нужно импортировать json, можем импортировать его из *vkbottle.modules* 

```py
from vkbottle import GroupEventType, GroupTypes, Keyboard, Callback
from vkbottle.modules import json
```

Создаем обычный хендлер сообщений, создаем клавиатуру, добавляем две *Callback* кнопки. В Callback кнопку передаем `label` и `payload`, и отправляем клавиатуру.

Создаем новый ивент: *MessageEvent*, внутри функции ставим условие: если в `payload` поступил текст *click*, то вызываем всплывающее уведомление, с помощью метода `messages.send_message_event_answer`, передаем параметры: *event_id*, *peer_id*, *user_id* и *event_data*. Это все мы можем взять из переменной `event`, которую мы указали в параметрах. В блоке *else* выполним теже самые действия, просто отправим другой текст.

```py
@bot.on.message(text="start")
async def handler(message: Message):
	keyboard = (
		Keyboard()
		.add(Callback("Click", {"cmd": "click"}))
		.add(Callback("Click 2", {"cmd": "click2"}))
	)

	await message.answer("callback button", keyboard=keyboard)

@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def message_event_handler(event: GroupTypes.MessageEvent):
	if event.object.payload["cmd"] == "click":
		await bot.api.messages.send_message_event_answer(
			event_id=event.object.event_id,
			peer_id=event.object.peer_id,
			user_id=event.object.user_id,
			event_data=json.dumps({"type": "show_snackbar", "text": "Test message"})
		)
	else:
		await bot.api.messages.send_message_event_answer(
			event_id=event.object.event_id,
			peer_id=event.object.peer_id,
			user_id=event.object.user_id,
			event_data=json.dumps({"type": "show_snackbar", "text": "Test message 2"})
		)
```
