#  Games Bot

import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from openai import OpenAI

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
@bot.command("d6")
async def d6(ctx):
    number = random.randint(1, 6)
    await ctx.send(f"You rolled a {number}!")


# Game 2 - Flip a coin                                                   #Adjust outputs then step 2 done
@bot.command("flip")
async def flip(ctx,user_input1):
    coin_flip = random.choice([True, False])
    if coin_flip:
        s = "Heads"
        if user_input1 in ("heads", "head"):
            r = " and You won!"
        else:
            r = " and You lost!"
    else:
        s = "Tails"
        if user_input1 in ("tails", "tail"):
            r = " and You won!"
        else:
            r = " and You lost!"
    await ctx.send(s + r)
# Game 3 - Rock, paper, scissors
@bot.command("rps")
async def rock_paper_scissors(ctx,user_input2):
    result = random.randint( 1, 3)

    if result == 3:
        s = "Computer chose: Scissors"
        if user_input2 == ("rock", "Rock"):
            r = " and You won!"
        elif user_input2 == "paper":
            r = " and You lost!"
        elif user_input2 == "scissors":
            r = " and You draw!"
        else:
            r = " Invalid input for Rock Paper Scissors."
    elif result == 2:
        s = "Computer chose: Paper"
        if user_input2 == ("rock", "Rock"):
            r = " and You lost!"
        elif user_input2 == "scissors":
            r = " and You won!"
        elif user_input2 == "paper":
            r = " and You draw!"
        else:
            r= "Invalid input for Rock Paper Scissors."
    elif result == 1:
        s = "Computer chose: Rock"
        if user_input2 == ("rock", "Rock"):
            r = " and You draw!"
        elif user_input2 == "scissors":
            r = " and You lost!"
        elif user_input2 == "paper":
            r = " and You won!"
        else:
            r = "Invalid input for Rock Paper Scissors."
    await ctx.send(s + r)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@bot.command("chat")
async def chat(ctx, *, message):
    response = client.responses.create(model="gpt-4.1",input="Answer in under 100 words: "+ message,)
    await ctx.send(response.output_text)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@bot.command("")
async def chat(ctx, *, message):
    response = client.responses.create(model="gpt-4.1",input="Use the movies that are provided to you and their story to make a quick synopsis of a new movie combining both of the mention movies. Make sure it is under 200 words: "+ message,)
    await ctx.send(response.output_text)


# Start the bot (reads TOKEN from your .env file)
bot.run(str(os.getenv("TOKEN")))
=======
#  Games Bot

import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from openai import OpenAI

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
@bot.command("d6")
async def d6(ctx):
    number = random.randint(1, 6)
    await ctx.send(f"You rolled a {number}!")


# Game 2 - Flip a coin                                                   #Adjust outputs then step 2 done
@bot.command("flip")
async def flip(ctx,user_input1):
    coin_flip = random.choice([True, False])
    if coin_flip:
        s = "Heads"
        if user_input1 in ("heads", "head"):
            r = " and You won!"
        else:
            r = " and You lost!"
    else:
        s = "Tails"
        if user_input1 in ("tails", "tail"):
            r = " and You won!"
        else:
            r = " and You lost!"
    await ctx.send(s + r)
# Game 3 - Rock, paper, scissors
@bot.command("rps")
async def rock_paper_scissors(ctx,user_input2):
    result = random.randint( 1, 3)

    if result == 3:
        s = "Computer chose: Scissors"
        if user_input2 == ("rock", "Rock"):
            r = " and You won!"
        elif user_input2 == "paper":
            r = " and You lost!"
        elif user_input2 == "scissors":
            r = " and You draw!"
        else:
            r = " Invalid input for Rock Paper Scissors."
    elif result == 2:
        s = "Computer chose: Paper"
        if user_input2 == ("rock", "Rock"):
            r = " and You lost!"
        elif user_input2 == "scissors":
            r = " and You won!"
        elif user_input2 == "paper":
            r = " and You draw!"
        else:
            r= "Invalid input for Rock Paper Scissors."
    elif result == 1:
        s = "Computer chose: Rock"
        if user_input2 == ("rock", "Rock"):
            r = " and You draw!"
        elif user_input2 == "scissors":
            r = " and You lost!"
        elif user_input2 == "paper":
            r = " and You won!"
        else:
            r = "Invalid input for Rock Paper Scissors."
    await ctx.send(s + r)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@bot.command("chat")
async def chat(ctx, *, message):
    response = client.responses.create(model="gpt-4.1",input="Answer in under 100 words: "+ message,)
    await ctx.send(response.output_text)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@bot.command("")
async def chat(ctx, *, message):
    response = client.responses.create(model="gpt-4.1",input="Use the movies that are provided to you and their story to make a quick synopsis of a new movie combining both of the mention movies. Make sure it is under 200 words: "+ message,)
    await ctx.send(response.output_text)


# Start the bot (reads TOKEN from your .env file)
bot.run(str(os.getenv("TOKEN")))
