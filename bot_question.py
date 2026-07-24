import os
import pandas as pd
from dotenv import load_dotenv
import discord
from discord.ext import commands
from openai import OpenAI, api_key
from openpyxl.comments import author
from surprise import Dataset, Reader, SVD


load_dotenv()

# HINT (Blank 1): read the secret Discord token out of the environment (Day 6/8).
# Which os function reads an environment variable, given its name as a string?
# Your .env file's variable is named TOKEN.
DISCORD_TOKEN = "TOKEN"
# HINT (Blank 2): same idea, but for the OpenAI key (Day 8).
# Your .env file's variable is named OPENAI_API_KEY.
OPENAI_API_KEY = api_key

client = OpenAI(api_key=OPENAI_API_KEY)
OPENAI_MODEL = "gpt-4.1"

SYSTEM_PROMPT = (
    "You are a helper for a Discord movie recommendation bot. Given a user's "
    "question, reply with ONLY the movie title they are asking about, and "
    "nothing else. If their message isn't about a movie, reply with exactly: "
    "I can only help with movie recommendations."
)

MOVIES_FILE = "ml-100k/u.item"
ORIGINAL_RATINGS_FILE = "ml-100k/u.data"
WORKING_RATINGS_FILE = "working_ratings.data"
USERS_FILE = "registered_users.csv"


def load_movie_titles():
    movies = pd.read_csv(MOVIES_FILE, sep="|", encoding="latin-1",usecols=[0, 1], names=["movie_id", "title"],)
    return dict(zip(movies["title"], movies["movie_id"]))


def load_registered_users():
    if not os.path.exists(USERS_FILE):
        return {}
    users = pd.read_csv(USERS_FILE)
    return dict(zip(users["discord_username"], users["user_id"]))


def save_registered_user(discord_username, user_id):
    new_row = pd.DataFrame([{"discord_username": discord_username, "user_id": user_id}])
    write_header = not os.path.exists(USERS_FILE)
    new_row.to_csv(USERS_FILE, mode="a", header=write_header, index=False)


def ensure_working_ratings_file_exists():
    if not os.path.exists(WORKING_RATINGS_FILE):
        original = pd.read_csv(ORIGINAL_RATINGS_FILE, sep="\t", header=None)
        original.to_csv(WORKING_RATINGS_FILE, sep="\t", header=False, index=False)


def add_rating_to_working_file(user_id, movie_id, rating):
    new_row = pd.DataFrame([[user_id, movie_id, rating, 0]])
    new_row.to_csv(WORKING_RATINGS_FILE, sep="\t", mode="a", header=False, index=False)


def train_model():
    reader = Reader(line_format="user item rating timestamp", sep="\t", rating_scale=(1, 5))
    data = Dataset.load_from_file(WORKING_RATINGS_FILE, reader=reader)
    trainset = data.build_full_trainset()
    # HINT (Blank 3): create the recommendation algorithm (Day 5).
    model = SVD() # >>> BLANK 3 <<<
    # HINT (Blank 4): train it on the trainset (Day 5).
    # Which method do you call on a model to actually teach it?
    model.fit(trainset)  # >>> BLANK 4 <<<
    return model


def find_movie(search_text):
    search_text = search_text.lower()
    for title, movie_id in movie_titles.items():
        if search_text in title.lower():
            return title, movie_id
    return None


ensure_working_ratings_file_exists()
movie_titles = load_movie_titles()
registered_users = load_registered_users()
model = train_model()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Loaded {len(movie_titles)} movies and {len(registered_users)} registered users.")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send("Something went wrong — check the spelling of your command and try again!")
    print(error)


# ==============================================================================
#  WORKED EXAMPLE: add_user is written for you, fully. Read through it
#  carefully — the other two commands below follow the same overall shape:
#  check something, handle the problem case, then do the real work.
# ==============================================================================

@bot.command("add_user")
async def add_user(ctx):
    discord_username = ctx.author.name

    if discord_username in registered_users:
        await ctx.send(f"You're already registered, {discord_username}!")
        return

    new_user_id = 9999 + len(registered_users)
    registered_users[discord_username] = new_user_id
    save_registered_user(discord_username, new_user_id)

    await ctx.send(f"Welcome, {discord_username}! You're registered as user {new_user_id}.")


# ==============================================================================
#  YOUR TURN: write add_rating and recommend below, from scratch.
#
#  You have these tools available to call:
#    registered_users             a dict: {discord_username: user_id}
#    find_movie(search_text)       returns (title, movie_id) or None
#    add_rating_to_working_file(user_id, movie_id, rating)
#    train_model()                  returns a freshly trained model
#    model                           the current trained model
#    client, OPENAI_MODEL, SYSTEM_PROMPT   for talking to OpenAI
# ==============================================================================

"""
    Let a registered user rate a movie, e.g.  !!add_rating Titanic 5

    Example:
      !!add_rating Titanic 5
      -> Got it — you rated Titanic (1997) a 5.0!

    Requirements:
      - Make sure the user is registered first; if not, tell them to
        register with !!add_user, and stop 
      - Make sure the rating is between 1 and 5; if not, tell them so, and stop
      - Use find_movie() to look up the title they typed; if nothing
        matches, tell them, and stop
      - Save the new rating with add_rating_to_working_file()
      - Retrain the model immediately, so this new rating counts right away
      - Send a confirmation message showing the movie title and rating
    """
#or

@bot.command("add_rating")
async def add_rating(ctx, movie_title: str, rating: float):
    discord_username = ctx.author.name

    if discord_username not in registered_users:
        await ctx.send(f"Before rating, please register yourself with !!add_user, {discord_username}!")
        return
    if float(rating) < 1 or float(rating) > 5:
        await ctx.send(f"Rating must be between 1 and 5!")
        return
    if find_movie(movie_title) is None:
        await ctx.send(f"Please put a valid movie name in, {discord_username}!")
        return
    if find_movie(movie_title) is not None:
        add_rating_to_working_file(discord_username, movie_title, rating)
        await  ctx.send(f"It has been logged: {movie_title} {rating}.")
        return
    trained_model = train_model()






@bot.command("recommend")
async def recommend(ctx, *, question: str):
    response = client.responses.create(model="gpt-4.1", input=[ {"role": "system", "content": SYSTEM_PROMPT }, {"role": "user", "content": question}])
    discord_username = ctx.author.name
    ctx.send(response.output_text)
    if discord_username not in registered_users:
        await ctx.send(f"Before rating, please register yourself with !!add_user, {discord_username}!")
        return

    user_id = registered_users[discord_username]

    movie_title_guess = response.output_text

    match = find_movie(movie_title_guess)
    if not match:
        await ctx.send(f"Sorry, I couldn't find a movie matching '{movie_title_guess}'.")
        return

    title, movie_id = match
    prediction = model.predict(str(user_id), str(movie_id))

    await ctx.send(f"{title} — Predicted rating: {prediction.est}")
    pass


bot.run(DISCORD_TOKEN)