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
		except VKAPIError[15]:
			await message.answer("Недостаточно прав...")
