# trivia_game.py

class TriviaGame:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.game_started = False

    async def fetch_categories(self):
        # Static categories for simplicity
        categories = ['Science', 'History', 'Music', 'Movies', 'Sports', 'General Knowledge']
        return categories

    async def start_game(self, ctx):
        """Starts the trivia game and prompts the player to choose a category."""
        if self.game_started:
            await ctx.send("The game has already started!")
            return
        
        self.game_started = True
        categories = await self.fetch_categories()
        await ctx.send(f"Game started! Choose a category to begin: {', '.join(categories)}")
