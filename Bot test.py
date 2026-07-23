import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

# Load the secret bot token from the .env file
load_dotenv()

# Turn on the one permission we need: reading message text
intents = discord.Intents.default()
intents.message_content = True

# Every command starts with "!!"
bot = commands.Bot(command_prefix="!!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command("Start")
async def start(ctx):
    print("Hello, I am a game bot!")
game_choice = input("Please select a game! Coin Flip[1] or Rock Paper Scissors![2] ").lower()


async def on_message(self, message):
    # don't respond to ourselves
    if message.author == self.user:
        return
    if message.content == 'ping':
        await message.channel.send('pong')
if game_choice == "1":
    user_input1 = input("Enter in flip for a coin flip: ").lower()
    coin_flip = random.choice([True, False])
    if coin_flip:
        print("Heads")
        if user_input1 in ("heads", "head"):
            print("You won!")
        else:
            print("You lost!")
    else:
        print("Tails")
        if user_input1 in ("tails", "tail"):
            print("You won!")
        else:
            print("You lost!")
elif game_choice == "2":
    print("Rules:"
          "1.Rock beats scissors, "
          "2.Paper beats rock, "
          "3.Scissors beats paper, and so on. "
          "4.If you have the same it is a draw!")
    user_input2 = input("Enter in Rock Paper Scissors: ").lower()
    rock_paper_scissors = random.choice([1, 2, 3])

    if rock_paper_scissors == 3:
        print("Computer chose: Scissors")
        if user_input2 == "rock":
            print("You won!")
        elif user_input2 == "paper":
            print("You lost!")
        elif user_input2 == "scissors":
            print("You draw!")
        else:
            print("Invalid input for Rock Paper Scissors.")
    elif rock_paper_scissors == 2:
        print("Computer chose: Paper")
        if user_input2 == "rock":
            print("You lost!")
        elif user_input2 == "scissors":
            print("You won!")
        elif user_input2 == "paper":
            print("You draw!")
        else:
            print("Invalid input for Rock Paper Scissors.")
    elif rock_paper_scissors == 1:
        print("Computer chose: Rock")
        if user_input2 == "rock":
            print("You draw!")
        elif user_input2 == "scissors":
            print("You lost!")
        elif user_input2 == "paper":
            print("You won!")
        else:
            print("Invalid input for Rock Paper Scissors.")

else:
    print("That's not a valid game!")
bot.run(str(os.getenv("TOKEN")))
