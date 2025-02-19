import discord
import os
import requests

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

    # Check if the message is coming from a server channel (not DM)
    if message.guild:
        # Respond only if the message starts with "~tell me a joke"
        if message.content.lower().startswith("~tell me a joke"):
            # Call the joke API
            joke = get_joke()
            await message.channel.send(joke)
        
        # Respond only if the message starts with "~tell me a fact"
        elif message.content.lower().startswith("~tell me a fact"):
            # Call the fact API
            fact = get_fact()
            await message.channel.send(fact)

# Function to get a joke from the JokeAPI
def get_joke():
    url = "https://v2.jokeapi.dev/joke/Programming?type=single"  # Example API endpoint for programming jokes
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        joke_data = response.json()

        if joke_data["error"]:
            return "Sorry, I couldn't fetch a joke at the moment."

        return joke_data["joke"]

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Function to get a fact from the new Fact API
def get_fact():
    url = "https://api.api-ninjas.com/v1/facts"
    headers = {
        "X-Api-Key": os.getenv("FACT_API_KEY"),  # Load the API key from the environment variable
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        fact_data = response.json()

        return fact_data[0]["fact"]

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
