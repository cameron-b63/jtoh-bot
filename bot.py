import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot prefix (commands start with this prefix)
BOT_PREFIX = "!"

# Define intents with necessary permissions
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Initialize bot with intents and command prefix
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Set to store whitelisted user IDs
whitelist = set()

known_difficulties = {
    'easy': 1256313207925243924,
    'medium': 1256313233279553656, 
    'hard': 1256313250988036217,
    'difficult': 1256313271951032441,
    'challenging': 1256313289739206716,
    'intense': 1256313304809476137,
    'remorseless': 1256313320575860826,
    'insane': 1256313336790913034,
    'extreme': 1256313352985247861,
    'terrifying': 1256313374787244055,
    'catastrophic': 1256313392705044550, 
    'horrific': 1256313451568042004, 
    'unreal': 1256313466944356402, 
    'nil': 1256313482576396399,
    'unknown' :1256349546515140778,
    }

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Command: Add Completion
@bot.command(name='addcompletion')
async def add_completion(ctx, username, tower_name, difficulty, time):
    # Check if user is in whitelist
    if ctx.author.id not in whitelist:
        await ctx.send("You are not authorized to use this command.")
        return

    if difficulty.lower() in known_difficulties:
        message = f"{username} has beaten {tower_name} [<:{difficulty}:{known_difficulties.get(difficulty)}>] in {time}"
    else:
        message = f"{username} has beaten {tower_name} [:unknown:] in {time}"
    await ctx.send(message)

# Command: Whitelist Management
@bot.command(name='whitelist')
async def whitelist_management(ctx, action, user: discord.Member = None):
    if action == 'add':
        if user:
            whitelist.add(user.id)
            await ctx.send(f"{user.display_name} has been added to the whitelist.")
        else:
            await ctx.send("Please mention a user to add to the whitelist.")
    elif action == 'remove':
        if user:
            if user.id in whitelist:
                whitelist.remove(user.id)
                await ctx.send(f"{user.display_name} has been removed from the whitelist.")
            else:
                await ctx.send(f"{user.display_name} is not in the whitelist.")
        else:
            await ctx.send("Please mention a user to remove from the whitelist.")
    elif action == 'list':
        if whitelist:
            await ctx.send("Whitelisted users:")
            for user_id in whitelist:
                user = bot.get_user(user_id)
                if user:
                    await ctx.send(f"- {user.name}#{user.discriminator}")
        else:
            await ctx.send("No users are currently whitelisted.")
    else:
        await ctx.send("Invalid action. Use `add`, `remove`, or `list`.")

bot.run(TOKEN)