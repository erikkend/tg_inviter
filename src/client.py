from telethon.sync import TelegramClient


class Client:
    def __init__(self, api_id, api_hash):
        self.client: TelegramClient = TelegramClient("Darkhan", api_id, api_hash)
        self.client.connect()
        self.check_is_client_connected()

    def check_is_client_connected(self):
        if not self.client.is_user_authorized():
            phone = input('Вы не авторизованы. Для авторизации введите номер телеграм: ')
            self.client.send_code_request(phone)
            self.client.sign_in(phone, input('Введите код: '))

    def get_client(self):
        return self.client
