import discord
import os
import requests

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == client.user:
        return

    # Only respond to "give me a joke" in server text channels
    if message.content.lower() == "give me a joke":
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = response.json()
        await message.channel.send(f"{joke['setup']} - {joke['punchline']}")
        
client.run(TOKEN)
