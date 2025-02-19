import discord
import os
import requests
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

#Trivia!
@bot.command(name='trivia')
async def trivia(ctx):
    trivia_data = get_trivia()
    
    if trivia_data:
        question = trivia_data['question']
        options = trivia_data['incorrect_answers'] + [trivia_data['correct_answer']]
        random.shuffle(options)
        
        # Send the question and options to the channel
        options_text = '\n'.join([f"{i + 1}. {opt}" for i, opt in enumerate(options)])
        await ctx.send(f"**Question:** {question}\n{options_text}")
    else:
        await ctx.send("Sorry, I couldn't fetch a trivia question right now.")

# Command to check the answer
@bot.command(name='answer')
async def answer(ctx, number: int):
    trivia_data = get_trivia()  # Make sure to fetch a new trivia question
    correct_answer = trivia_data['correct_answer']
    
    # Check if the user's answer matches the correct one
    if trivia_data['incorrect_answers'][number - 1] == correct_answer:
        await ctx.send("Correct! Well done.")
    else:
        await ctx.send(f"Sorry, that's incorrect. The correct answer was: {correct_answer}")


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
    
# Function to fetch trivia questions
def get_trivia():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"  # Get one question
    response = requests.get(url)
    question_data = response.json()
    
    if question_data['response_code'] == 0:
        question = question_data['results'][0]
        return {
            'question': question['question'],
            'correct_answer': question['correct_answer'],
            'incorrect_answers': question['incorrect_answers']
        }
    return None
    
bot.run(TOKEN)
