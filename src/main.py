import re
import time
import random

from credentials import API_ID, API_HASH
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError

from src.base import Base
from src.client import Client


class UserInviter(Base):
	def __init__(self, tg_client):
		super().__init__(tg_client)
		self.need_groups = {}

	def invite_task_manager(self):
		users = self.get_group_users(self.need_groups.get('invite_from_group'))
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

	def search_chats_to_invite(self, group_name_to_invite, group_name_from_invite):
		dialogs = self.get_gialogs()

		for chat in dialogs.chats:
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


class Parser(Base):
	def __init__(self, tg_client):
		super().__init__(tg_client)
		self.group_to_pars = None

	def set_chat_to_collect(self, chat_to_collect_from):
		dialogs = self.get_gialogs()

		for chat in dialogs.chats:
			try:
				if not chat.megagroup:
					continue
				if chat.title == chat_to_collect_from:
					self.group_to_pars = chat
			except AttributeError:
				continue

	def collect_and_save_users(self):
		users = self.get_group_users(self.group_to_pars)

		emoji_pattern = re.compile("["
								   u"\U0001F600-\U0001F64F"  # emoticons
								   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
								   u"\U0001F680-\U0001F6FF"  # transport & map symbols
								   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
								   "]+", flags=re.UNICODE)
		group_name_deleted_emoji = emoji_pattern.sub('', self.group_to_pars.title)
		with open(f'{group_name_deleted_emoji}_users.txt', 'w', encoding='UTF-8') as txtfile:
			for user in users:
				if not user.is_self and not user.bot:
					txtfile.write(f"{user.id} {user.username} {user.access_hash}\n")


class MessageSender(Base):
	def __init__(self, tg_client):
		super().__init__(tg_client)
		self.file_name = ""

	def set_file_name(self, file_name):
		self.file_name = file_name + '.txt'

	def send_message_task_manager(self):
		users = self.read_users()

		for user in users:
			user_id = user.get('id')
			user_username = user.get("username")

			try:
				if user_username == "None":
					user_entity = self.client.get_entity(int(user_id))
				else:
					user_entity = self.client.get_entity(user_username)

				self.send_message_task(user_entity)

				time.sleep(random.randrange(10, 30))

			except Exception as e:
				print(e)
				print(user.get("username"))

			except PeerFloodError:
				print("[!] Получаю ошибку Flood от telegram. \n[!] Сценарий сейчас останавливается. \n[!] Пожалуйста, повторите попытку через некоторое время.")

			except UserPrivacyRestrictedError:
				print("[!] Настройки конфиденциальности пользователя не позволяют вам этого делать. Пропускаем.")

	def send_message_task(self, to_user):
		default_message = f"Привет {to_user.username}! Я тестирую эту хуйню"

		self.client.send_message(to_user, default_message)

	def read_users(self):
		FIELDS = ('id', 'username', 'access_hash')
		users = []
		with open(self.file_name, "r", encoding='UTF-8') as file:
			lines = file.readlines()
			for i in lines:
				users.append(dict(zip(FIELDS, i.split())))

		return users


if __name__ == "__main__":
	client = Client(API_ID, API_HASH)


	# inviter = UserInviter(client.get_client())
	# group_to_invite = "test_to_add2"
	# group_from_invite = "KAKA"
	# inviter.search_chats_to_invite(group_to_invite, group_from_invite)
	# inviter.invite_task_manager()


	# parser = Parser(client.get_client())
	# parser.set_chat_to_collect("KAKA")
	# parser.collect_and_save_users()

	sms_sender = MessageSender(client.get_client())
	sms_sender.set_file_name("KAKA_users")
	sms_sender.read_users()
	sms_sender.send_message_task_manager()
