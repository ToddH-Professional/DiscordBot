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
    if message.author == client.user:
        return
    
    if message.content.lower() == "give me a joke":
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        joke = response.json()
        await message.channel.send(f"{joke['setup']} - {joke['punchline']}")

client.run(TOKEN)
