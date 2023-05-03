import asyncio
import time
import random

from telethon.sync import TelegramClient
from credentials import API_ID, API_HASH
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError


class UserInviter:
	def __init__(self, api_id, api_hash):
		self.client = TelegramClient("Darkhan", api_id, api_hash)
		self.client.start()
		self.need_groups = {}

	def invite_task_manager(self):
		users = self.client.get_participants(self.need_groups.get('invite_from_group'))
		for user in users:
			print(user.username)
			try:
				user_to_add = InputPeerUser(user.id, user.access_hash)
				self.invite_user_task(user_to_add)
				time.sleep(random.randrange(10, 30))
			except Exception as e:
				print(e)
				print(user.username)
			except PeerFloodError:
				print("[!] Получаю ошибку Flood от telegram. \n[!] Сценарий сейчас останавливается. \n[!] Пожалуйста, повторите попытку через некоторое время.")
			except UserPrivacyRestrictedError:
				print("[!] Настройки конфиденциальности пользователя не позволяют вам этого делать. Пропускаем.")

	def invite_user_task(self, user):
		self.client(InviteToChannelRequest(channel=self.need_groups.get('invite_to_group'), users=[user]))

	def get_group_users(self, group_name_to_invite, group_name_from_invite):
		all_dialogs = self.client(GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=InputPeerEmpty(), limit=200, hash=0))

		for chat in all_dialogs.chats:
			try:
				if not chat.megagroup:
					continue
				if chat.title == group_name_to_invite:
					self.need_groups['invite_to_group'] = chat
				elif chat.title == group_name_from_invite:
					self.need_groups['invite_from_group'] = chat
			except AttributeError:
				continue

		print(self.need_groups["invite_to_group"].__dict__)
		print()
		print()
		print(self.need_groups["invite_from_group"].__dict__)


inviter = UserInviter(API_ID, API_HASH)
group_to_invite = "test_to_add2"
group_from_invite = "KAKA"
# group_to_invite = input("Напиши название группы в которую хочешь инвайтить:\n")
# group_from_invite = input("Напиши название группы с которой будешь инвайтить:\n")
inviter.get_group_users(group_to_invite, group_from_invite)
inviter.invite_task_manager()
