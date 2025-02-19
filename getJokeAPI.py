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

    # Respond only if the message starts with "~tell me a joke"
    if message.content.lower().startswith("~tell me a joke"):
        # Send a response (this is where you can add a joke from an API)
        await message.channel.send("Here's a joke for you! 😂")

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
