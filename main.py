import os, discord
from dotenv import load_dotenv
from feedback import Feedback
from player import Player
from utilities import try_give_feedback
from commands import handle_add_emoji_command, handle_change_avatar_command
from items import ITEM_DATABASE
from database import Database
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
	if message.author == client.user or not message.content.startswith(PREFIX): return

	command = message.content.strip()[len(PREFIX):].split(' ')
	try:
		match command: 
			case ['change_avatar', *_]:
				await handle_change_avatar_command(message, client)
			case ['add_emoji', emoji_name]:
				await handle_add_emoji_command(message, emoji_name)
			case ['profile']:
				player = Player(message.author.id)
				await message.reply(embed=await player.get_profile(client))
			case ['inventory']:
				player = Player(message.author.id)
				await message.reply(await player.get_inventory(client))
			case ['award']: 
				player = Player(message.author.id)
				outp = ""
				for item in ITEM_DATABASE.values(): 
					outp += f'Awarding {message.author} with {item.name} x{item.stack_size}\n'
					await player.award_item(item, message)
				Database.save()
				await message.reply(outp)
			case _:
				await message.reply(Feedback.INVALID_COMMAND)
	except discord.HTTPException as exception:
		print(f"[ERROR] {exception}")
		await try_give_feedback(message, Feedback.GENERIC_FEEDBACK)
    

client.run(os.getenv('BOT_TOKEN')) 