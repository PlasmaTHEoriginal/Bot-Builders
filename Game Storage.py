#  Games Bot

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

# Game 1 - Roll a die
@bot.command("Roll")
async def roll(ctx):
    number = random.randint(1, 6)
    await ctx.send(f"You rolled a {number}!")


# Game 2 - Flip a coin
@bot.command("Flip")
async def flip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(result)


# Game 3 - Rock, paper, scissors
@bot.command("Rock Paper Scissors")
async def rps(ctx, player):
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


# Start the bot (reads TOKEN from your .env file)
bot.run(str(os.getenv("TOKEN")))
