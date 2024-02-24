import fificord
from fificord.ext import commands

client = commands.Bot(command_prefix="l!")

@client.event
async def on_ready():
    print(f"Loggined in as: " + client.user.name)

client.run(token="MTEyMjU2NTgwMDExNzY3NDEwNA.G6qPhp.x-C11vnE13qLYnH27l2tBFrf-wQAf3_3ARRi44", bot=False)