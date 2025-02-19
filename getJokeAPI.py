import discord
import os

intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Respond only if the message starts with "~tell me a joke"
    if message.guild:  # Check if it's a server message (not DM)
        if message.content.lower().startswith("~tell me a joke"):
            await message.channel.send("Here's a joke for you! 😂")

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
