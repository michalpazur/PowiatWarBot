from pprint import pprint
from typing import IO

from discord import Client, TextChannel, Forbidden, File
from log import log_error, log_info

client = Client()


async def SendMessageToAll():
    try:
        with open('discord-api-key.txt', 'r') as f:
            TOKEN = f.readline()
            client.run(TOKEN)
    except Exception as ex:
        log_error(ex)


@client.event
async def on_ready(message: str, image: IO = None):
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        pprint([x for x in guild.channels if isinstance(x, TextChannel)])
        for channel in [x for x in guild.channels if isinstance(x, TextChannel)]:
            try:
                await channel.trigger_typing()
                await channel.send(message, file=File(image, 'bot.png'))
                break
            except Forbidden:
                pass

    log_info("Send to all discord channels")
    await client.close()
