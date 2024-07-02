import discord
import os
from discord.ext import commands
from discord import app_commands
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

WHITELIST_MANAGER_ROLE_NAME = "jtoh-bot whitelist manager"

# Set to store whitelisted user IDs
whitelist = set()

# Track channel to send in
target_channel_id = None

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
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Command: Add Completion
@bot.tree.command(name='addcompletion')
@app_commands.describe(username="Roblox username", tower_name="Name of the tower", difficulty="Tower difficulty", time="Completion time")
async def add_completion(interaction: discord.Interaction, username: str, tower_name: str, difficulty: str, time: str):
    # Check if user is in whitelist
    if interaction.user.id not in whitelist:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    
    # Check if target channel is defined
    if target_channel_id is None:
        await interaction.response.send_message("Before recording completions, set the target tracking channel with `!setchannel`", ephemeral=True)
        return

    if difficulty.lower() in known_difficulties:
        message = f"{username} has beaten {tower_name} [<:{difficulty.lower()}:{known_difficulties.get(difficulty.lower())}>] in {time}"
    else:
        message = f"{username} has beaten {tower_name} [:unknown:] in {time}"
        
    await interaction.response.send_message("Completion successfully recorded in tracking channel.", ephemeral=True)
    
    await bot.get_channel(target_channel_id).send(message)
    
# Command: Channel Management
@bot.tree.command(name='setchannel')
@app_commands.describe(channel="Target channel to track completions in")
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global target_channel_id
    target_channel_id = channel.id
    await interaction.response.send_message(f"Target channel has been set to: {channel.name} ({channel.id})", ephemeral=True)
    

# Command: Whitelist Management
@bot.tree.command(name='whitelist')
@app_commands.describe(user="User to manage whitelist permissions for")
async def whitelist_management(interaction: discord.Interaction, action: str, user: discord.Member = None):
    whitelist_management_role = discord.utils.get(interaction.user.roles, name=WHITELIST_MANAGER_ROLE_NAME)
    user_is_admin = any(role.permissions.administrator for role in interaction.user.roles)
    if action == 'add':
        if whitelist_management_role not in interaction.user.roles and not user_is_admin:
            await interaction.response.send_message("You do not have the required role to manage the jtoh-bot witelist.")
            return
        if user:
            whitelist.add(user.id)
            await interaction.response.send_message(f"{user.display_name} has been added to the whitelist.", ephemeral=True)
        else:
            await interaction.response.send_message("Please mention a user to add to the whitelist.", ephemeral=True)
    elif action == 'remove':
        if whitelist_management_role not in interaction.user.roles and not user_is_admin:
            await interaction.response.send_message("You do not have the required role to manage the jtoh-bot witelist.")
            return
        if user:
            if user.id in whitelist:
                whitelist.remove(user.id)
                await interaction.response.send_message(f"{user.display_name} has been removed from the whitelist.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{user.display_name} is not in the whitelist.", ephemeral=True)
        else:
            await interaction.response.send_message("Please mention a user to remove from the whitelist.", ephemeral=True)
    elif action == 'list':
        if whitelist:
            await interaction.response.send_message("Whitelisted users:", ephemeral=True)
            for user_id in whitelist:
                user = bot.get_user(user_id)
                if user:
                    await interaction.response.send_message(f"- {user.name}#{user.discriminator}", ephemeral=True)
        else:
            await interaction.response.send_message("No users are currently whitelisted.", ephemeral=True)
    else:
        await interaction.response.send_message("Invalid action. Use `add`, `remove`, or `list`.", ephemeral=True)

bot.run(TOKEN)