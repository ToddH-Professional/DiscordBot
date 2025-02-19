import random
import requests
import asyncio

class TriviaGame:
    def __init__(self, guild_id):
        self.guild_id = guild_id  # Unique ID for the server
        self.game_started = False  # Track if the game has started
        self.players = []  # List of players who joined
        self.score = {}  # Dictionary to keep track of player scores
        self.current_question = None  # Store the current question
        self.correct_answer = None  # Store the correct answer for the current question

    def add_player(self, player):
        """Add a player to the trivia game."""
        try:
            self.players.append(player)
            self.score[player] = 0  # Initialize the player's score
        except Exception as e:
            print(f"Error adding player {player}: {e}")
            
    async def start_reminder(self, ctx):
        """Send a reminder message 5 minutes after first player joined, if game hasn't started."""
        while not self.game_started:  # Only remind if the game hasn't started yet
            if self.start_time is not None:
                elapsed_time = asyncio.get_event_loop().time() - self.start_time
                if elapsed_time >= 300:  # 300 seconds = 5 minutes
                    await ctx.send(f"Reminder: The game has started! Type `~trivia-start` to begin the trivia!")
                    self.start_time = None  # Stop sending reminders after the first one
            await asyncio.sleep(60)  # Check every minute

    def start_game(self):
        """Start the trivia game."""
        try:
            self.game_started = True
            question, options = self.ask_question()
            return question, options
        except Exception as e:
            print(f"Error starting game: {e}")
            return None, None

    def ask_question(self):
        """Fetch a trivia question and prepare the options."""
        try:
            question_data = self.fetch_question()
            self.current_question = question_data["question"]
            self.correct_answer = question_data["correct_answer"]
            options = question_data["incorrect_answers"] + [self.correct_answer]
            random.shuffle(options)  # Shuffle options so the answer is not always last

            return self.current_question, options
        except Exception as e:
            print(f"Error asking question: {e}")
            return None, []

    def fetch_question(self):
        """Fetch a random trivia question from the API."""
        try:
            url = "https://opentdb.com/api.php?amount=1&type=multiple"
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            return data["results"][0]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trivia question: {e}")
            return {"question": "Sorry, there was an error fetching a question.", 
                    "correct_answer": "N/A", 
                    "incorrect_answers": []}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"question": "Sorry, there was an unexpected error.", 
                    "correct_answer": "N/A", 
                    "incorrect_answers": []}
