from vkbottle.user import User, Message

user = User("TOKEN")


@user.on.message(text="2022")
async def handler(message: Message):
	await message.answer("Happy New Year 🌲")


user.run_forever()