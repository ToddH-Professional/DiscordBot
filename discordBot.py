import discord
import os
import requests
import asyncio
import random
from trivia_game import TriviaGame
from discord.ext import commands

# Load your bot token and API keys
TOKEN = os.getenv("DISCORD_TOKEN")
FACT_API_KEY = os.getenv("FACT_API_KEY")

# Set the command prefix to "~"
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

bot = commands.Bot(command_prefix="~", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

#---------COMMANDS-------------#

#Jokes!
@bot.command(name="joke")
async def get_joke(ctx):
    """Fetch a random programming joke and send it."""
    joke = fetch_joke()
    await ctx.send(joke)

#Facts!
@bot.command(name="fact")
async def get_fact(ctx):
    """Fetch a random fact and send it."""
    fact = fetch_fact()
    await ctx.send(fact)

#Quotes!
@bot.command(name="quote")
async def get_quote(ctx):
    """Fetch a random quote and send it with the author."""
    quote, author = fetch_quote()
    await ctx.send(f'"{quote}" - {author}')

#--------FUNCTIONS------------#

# Function to get a joke from the JokeAPI
def fetch_joke():
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

# Function to get a fact from the Fact API
def fetch_fact():
    url = "https://api.api-ninjas.com/v1/facts"
    headers = {
        "X-Api-Key": FACT_API_KEY,  # Load the API key from the environment variable
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        fact_data = response.json()

        return fact_data[0]["fact"]

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Function to get a random quote from the Ninja API
def fetch_quote():
    url = "https://api.api-ninjas.com/v1/quotes"
    headers = {
        "X-Api-Key": FACT_API_KEY,  # Load the API key from the environment variable
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        quote_data = response.json()

        # Return the quote and author
        return quote_data[0]["quote"], quote_data[0]["author"]

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", ""

#------------------The trivia game  #------------------

# # A dictionary to hold trivia sessions
trivia_sessions = {}

# Start the trivia game with the `~trivia` command
@bot.command()
async def trivia(ctx):
    """Starts a solo trivia session."""
    if ctx.guild.id in trivia_sessions:
        await ctx.send("A trivia session is already in progress. Use ~trivia-start to begin the game.")
    else:
        trivia_sessions[ctx.guild.id] = TriviaGame(ctx.guild.id)
        await ctx.send("Trivia game has started! Type ~trivia-start to begin playing.")

# Command to start the solo trivia game
@bot.command()
async def trivia_start(ctx):
    """Starts the trivia game and prompts the player to choose a category."""
    if ctx.guild.id not in trivia_sessions:
        await ctx.send("No trivia game is active. Type ~trivia to start a new game.")
        return

    session = trivia_sessions[ctx.guild.id]
    
    if not session.game_started:
        await session.start_game(ctx)
    else:
        await ctx.send("The game has already started!")

bot.run(TOKEN)
