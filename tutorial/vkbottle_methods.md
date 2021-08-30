## [VkBottle | Работа с методами](https://www.youtube.com/watch?v=KmfLUZb8GPQ)
__В этом видео-ролике автор рассказывает, как работать с методами вк-апи с помощью модуля VkBottle__

*Код:* Импортируется два модуля (asyncio, из VkBottle класс API). Asyncio понадобится для запуска асинхронных функций, а класс API для взаимодействия с методами Vk-API. В переменной `friend` получаем список своих друзей и в цикле перебираем список с ID'шниками друзей. Переменная `user`: получаем детальную информацию о пользователе, `status`: получаем статус пользователя. Выводим имя, фамилию и статус пользователя в консоль. `asyncio.run(handler())` - запускаем асинхронную функцию.

```py
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
```