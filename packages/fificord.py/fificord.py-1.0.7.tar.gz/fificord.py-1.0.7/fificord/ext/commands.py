# ext/commands.py
import asyncio
from ...fificord import session
from maxdev import Fore
import random

class BotUser():
    name = None
    display_name = None
    discriminator = None
    avatar_url = None
    default_avatar_url = None
    id = None
    
class Activity:
    def __init__(self, client):
        self.client = client

    def set(self, data):
        token = self.client.token
        authorization = self.client.authorization
        headers = {
            'Authorization': f'{authorization} {token}',
            'Content-Type': 'application/json',
        }
        response = session.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(Fore.YELLOW + 'fificord.py ' + Fore.RED + '[ERROR] ' + Fore.GRAY + "Could not set status." + Fore.RESET)

    def set_activity(self, type, name, status, url=None):
        data = {
            'status': status,
            'custom_status': {
                'text': name,
                'emoji_name': None,
                'emoji_id': None,
                'expires_at': None,
                'activities': [
                    {
                        'type': type,
                        'name': name,
                        "url": url
                    }
                ]
            }
        }
        self.set(data)

    async def Playing(self, content, status):
        self.set_activity(0, content, status)

    async def Streaming(self, content, status, url):
        self.set_activity(1, content, status, url)

    async def Listening(self, content, status):
        self.set_activity(2, content, status)

    async def Watching(self, content, status):
        self.set_activity(3, content, status)

class Bot:
    def __init__(self, command_prefix='!'):
        self.command_prefix = command_prefix
        self._is_running = False
        self.event_listeners = {}
        self.token = None
        self.user = BotUser()
        self.authorization = None
        self.Activity = Activity(self)

    async def login(self, token, bot=False):
        self.token = token
        if bot == False:
            self.authorization = ""
        elif bot == True:
            self.authorization = "Bot"
        headers = {
            'Authorization': f'{self.authorization} {token}'
        }
        response = session.get('https://discord.com/api/v9/users/@me', headers=headers)

        if response.status_code == 200:
            self.user.name = response.json()["username"]
            self.user.display_name = response.json()["username"]
            if response.json()["global_name"] != None:
                self.user.display_name = response.json()["global_name"]
            self.user.discriminator = response.json()["discriminator"]
            self.user.id = response.json()["id"]
            self.user.avatar_url = f"https://cdn.discordapp.com/avatars/{self.user.id}/avatar.png"
            self.user.default_avatar_url = f"https://cdn.discordapp.com/embed/avatars/{str(random.randint(1, 5))}.png"
            await self.dispatch_event('on_ready')
        else:
            self._is_running = False
            raise Exception(Fore.YELLOW + 'fificord.py ' + Fore.RED + '[ERROR] ' + Fore.GRAY + "Improper token has been passed." + Fore.RESET)

    def event(self, func):
        event_type = func.__name__
        async def wrapper(*args, **kwargs):
            await func(*args, **kwargs)
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(wrapper)
        return wrapper

    async def dispatch_event(self, event_type, *args, **kwargs):
        if event_type in self.event_listeners:
            for func in self.event_listeners[event_type]:
                await func(*args, **kwargs)

    async def start(self, token, bot):
        if not self._is_running:
            self._is_running = True
            await self.login(token, bot)

            while self._is_running:
                await asyncio.sleep(1)

    def run(self, token, bot):
        asyncio.run(self.start(token, bot))