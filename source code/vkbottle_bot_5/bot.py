from vkbottle.bot import Bot, load_blueprints_from_package

bot = Bot("TOKEN")
for bp in load_blueprints_from_package("blueprints"):
	bp.load(bot)

bot.run_forever()