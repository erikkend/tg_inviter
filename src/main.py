import asyncio

from telethon.sync import TelegramClient
from credentials import api_id, api_hash


class UserInviter:
	def __init__(self):
		self.client = TelegramClient("Darkhan", api_id, api_hash)
		self.client.start()

	def get_group_users(self):
		self.client.get_dialogs()
		channel_entity = self.client.get_entity("💬 BLAUGRANA CHAT")
		print(channel_entity)
		parts = self.client.get_participants(channel_entity)
		for i in parts:
			print(i.username)

inviter = UserInviter()
inviter.get_group_users()
