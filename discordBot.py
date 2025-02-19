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

@bot.command(name="trivia")
async def trivia(ctx):
    """Start a trivia game or join the existing one."""
    channel_id = ctx.channel.id
    
    if channel_id in trivia_sessions:
        # Game is already running, add the player to the game
        game = trivia_sessions[channel_id]
        game.add_player(ctx.author.name)
        await ctx.send(f"{ctx.author.name} joined the trivia game! Type `~trivia-start` to begin.")
    else:
        # Start a new trivia game
        trivia_sessions[channel_id] = TriviaGame(channel_id)
        game = trivia_sessions[channel_id]
        game.add_player(ctx.author.name)
        await ctx.send(f"{ctx.author.name}, you've started a new trivia game! Type `~trivia-start` to begin.")
    
    # Send a reminder every minute
    send_reminder.start(ctx)

@bot.command(name="trivia-start")
async def trivia_start(ctx):
    """Start the trivia game once the player is ready."""
    channel_id = ctx.channel.id
    
    if channel_id not in trivia_sessions:
        await ctx.send("No trivia game is running in this channel. Use `~trivia` to start a new game.")
        return
    
    game = trivia_sessions[channel_id]
    if len(game.players) < 1:
        await ctx.send("You need at least 1 player to start the game. Have more players join with `~trivia`.")
        return

    # Start the trivia game
    question, options = game.start_game()

    if question:
        await ctx.send(f"Question: {question}\nOptions: {', '.join(options)}")
    else:
        await ctx.send("There was an error starting the game.")

@tasks.loop(minutes=1)
async def send_reminder(ctx):
    """Send a reminder every minute that the game can start with `~trivia-start`."""
    channel_id = ctx.channel.id
    
    if channel_id in trivia_sessions:
        await ctx.send("Reminder: Type `~trivia-start` to begin the game.")

@bot.command(name="answer")
async def trivia_answer(ctx, answer):
    """Check the player's answer."""
    channel_id = ctx.channel.id
    
    if channel_id not in trivia_sessions:
        await ctx.send("No game is currently running.")
        return

    game = trivia_sessions[channel_id]
    if game.game_started:
        correct = game.correct_answer.lower() == answer.lower()
        if correct:
            game.score[ctx.author.name] += 1
            await ctx.send(f"Correct, {ctx.author.name}! You have {game.score[ctx.author.name]} points.")
        else:
            await ctx.send(f"Sorry, {ctx.author.name}. The correct answer was: {game.correct_answer}")
    else:
        await ctx.send("The game hasn't started yet. Use `~trivia-start` to begin.")

bot.run(TOKEN)
