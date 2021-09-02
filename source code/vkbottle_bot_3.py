from vkbottle.bot import Bot, Message
from vkbottle import GroupEventType, GroupTypes, VKAPIError, Keyboard, Callback
from vkbottle.modules import json

from config import token

bot = Bot(token)


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


bot.run_forever()
