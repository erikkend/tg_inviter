from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty


class Base:
    def __init__(self, tg_client):
        self.client = tg_client

    def get_group_users(self, group_entity):
        users = self.client.get_participants(group_entity)

        return users

    def get_gialogs(self):
        dialogs = self.client(GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=InputPeerEmpty(), limit=200, hash=0))

        return dialogs
