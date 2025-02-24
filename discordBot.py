import discord
import os
import requests
import random
import html
import asyncio
from discord.ext import commands, tasks

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

# Function to handle the `~trivia` command
@bot.command()
async def trivia(ctx):
    """Fetch a random trivia and give answer in 15 seconds."""
    trivia_text = fetch_trivia()
    await ctx.send(trivia_text)

     # Wait for 10 seconds before starting the countdown
    await asyncio.sleep(10)

    # Countdown from 5 to 1
    for i in range(5, 0, -1):
        await ctx.send(f"{i}...")
        await asyncio.sleep(1)  # Wait for 1 second

    # Send the correct answer after countdown
    await ctx.send(f"The answer is: {current_answer}")

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

# Function to get random trivia question
# Variable to store the question and correct answer globally
current_question = None
current_answer = None
def fetch_trivia():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        trivia_data = response.json()

        if trivia_data["response_code"] == 0:
            question_data = trivia_data["results"][0]
            question = html.unescape(question_data["question"])  # Unescape HTML entities in the question
            correct_answer = html.unescape(question_data["correct_answer"])  # Unescape HTML entities in the correct answer
            all_answers = [html.unescape(answer) for answer in question_data["incorrect_answers"]] + [correct_answer]
            random.shuffle(all_answers)

            choices = "\n".join([f"{i+1}. {answer}" for i, answer in enumerate(all_answers)])

            # Store the question and correct answer
            global current_question, current_answer
            current_question = question + "\n\n" + choices
            current_answer = correct_answer

            return f"**Trivia Time!**\n{current_question}"

        else:
            return "Couldn't fetch a trivia question. Try again!"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    
bot.run(TOKEN)
