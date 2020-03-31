# Work with Python 3.6
import discord
import yaml
import asyncio

from mysql_library import *

TOKEN = ""
ONLINE_STATUS_MESSAGE = "ONLINE"
OFFLINE_STATUS_MESSAGE = "OFFLINE"

with open(r'config.yaml') as file:
    document = yaml.full_load(file)
    TOKEN = document.get('discord-token')
    ONLINE_STATUS_MESSAGE = document.get('online-status-message')
    OFFLINE_STATUS_MESSAGE = document.get('offline-status-message')
    
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

async def set_game_status(game):
    await client.change_presence(activity=discord.Game(game), status=discord.Status.online, afk=False)
        
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    client.loop.create_task(poll_server_status())

async def get_server_last_active():
    server_data = await execute_read_query(connection, "SELECT LAST_ACTIVE FROM SUM_TABLE WHERE EVENT_NAME='SERVER_ONLINE' AND UUID='SERVER'")
    return server_data[0][0]
    
async def poll_server_status():
    last_value = -1
    last_online = True
    online = False
    while True:
        server_last_seen = await get_server_last_active()

        if server_last_seen == last_value or last_value == -1:
            online = False
        else:
            online = True

        if last_online != online:
            if online:
                print("Setting Status to ONLINE")
                await set_game_status(ONLINE_STATUS_MESSAGE)               
            else:
                print("Setting Status to OFFLINE")
                await set_game_status(OFFLINE_STATUS_MESSAGE)

        last_online = online
        last_value = server_last_seen
        await asyncio.sleep(5)
        
        
client.run(TOKEN)
