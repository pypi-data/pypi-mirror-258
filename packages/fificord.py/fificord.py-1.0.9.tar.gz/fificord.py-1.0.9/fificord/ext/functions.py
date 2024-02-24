import tls_client
from maxdev import Fore
session = tls_client.Session()

class Functions():
    def __init__(self, client):
        self.client = client
    def send_message(self, channel_id, message):
        data = {
            "content": message
        }

        headers = {
            'Authorization': f'{self.client.authorization} {self.client.token}'
        }
        response = session.post(f"https://discord.com/api/v9/{channel_id}/messages", headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(Fore.YELLOW + 'fificord.py ' + Fore.RED + '[ERROR] ' + Fore.GRAY + "Could not send message." + Fore.RESET)
    def open_dm(self, user_id):
        data = {"recipient_id": user_id}
        headers = {
            'Authorization': f'{self.client.authorization} {self.client.token}'
        }
        response = session.post("https://discord.com/api/v9/users/@me/channels", headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(Fore.YELLOW + 'fificord.py ' + Fore.RED + '[ERROR] ' + Fore.GRAY + "Could not open dm." + Fore.RESET)
    
        channel_id = response.json()['id']
    
        return channel_id
    def send_dm_message(self, user_id, message):
        channel_id = self.open_dm(user_id)
        self.send_message(channel_id, message)