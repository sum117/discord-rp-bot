import discord, random, httpx
from feedback import Feedback


async def try_give_feedback(message: discord.Message, feedback = Feedback.GENERIC_FEEDBACK):
    try:
        await message.channel.send(feedback)
    except discord.HTTPException:
        print('Error sending feedback message.')


def get_image_url_from_message(message: discord.Message):
    """
    Returns the first image attachment in the message, or the first link to an image.
    """
    if message.attachments: return message.attachments[0].url
    
    url = message.content.split(' ')[1]
    allowed_extensions = ('jpg', 'png', 'jpeg')
    
    if url.startswith('https://') and url.endswith(allowed_extensions): return url



def admin_only(func):
	"""
	Decorator for checking authorization to use certain commands, can only be used on async functions
	"""
	async def wrapper(*args, **kwargs):
		if not isinstance(args[0], discord.Message):
			print('[WARNING] admin_only decorator used on a function that doesn\'t take a message as its first argument.')
			return         
		if args[0].author.guild_permissions.administrator: await func(*args, **kwargs)
	return wrapper


def create_embed(msg: discord.Message):
    return discord.Embed(description=msg.content)


async def react(msg: discord.Message):
    possible_emotes = [*msg.guild.emojis, '😄']
    await msg.add_reaction(random.choice(possible_emotes))

async def download_image(url: str) -> bytes | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200: 
        return response.content