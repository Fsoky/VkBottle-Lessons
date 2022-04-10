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

	await message.answer(str(result))