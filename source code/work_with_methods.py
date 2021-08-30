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