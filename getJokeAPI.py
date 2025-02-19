import discord
import os

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    
    # Send a test response to every message (this will show if the bot can post to channels)
    await message.channel.send("Bot is working!")

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
