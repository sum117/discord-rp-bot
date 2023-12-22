import os, discord
from dotenv import load_dotenv
from feedback import Feedback
from player import Player
from utilities import try_give_feedback
from commands import handle_add_emoji_command, handle_change_avatar_command
load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

PREFIX = '$'


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user or not message.content.startswith(PREFIX):
        return
    
    command = message.content[len(PREFIX):].split(' ')
    try:
        match command: 
            case ['change_avatar', *_]:
                await handle_change_avatar_command(message, client)
            case ["add_emoji", emoji_name]:
                await handle_add_emoji_command(message, emoji_name)
            case ["profile"]:
                player = Player(message.author.id)
                await message.reply(embed=await player.get_profile(client))
            case _:
                await message.reply(Feedback.INVALID_COMMAND)
    except discord.HTTPException as exception:
        print(f"[ERROR] {exception}")
        await try_give_feedback(message, Feedback.GENERIC_FEEDBACK)
    


# ---- run the bot ---- #
client.run(os.getenv('BOT_TOKEN')) 