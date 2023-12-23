import discord
from utilities import admin_only, get_image_url_from_message, download_image

class ChangeAvatarState:
    working = False

@admin_only
async def handle_change_avatar_command(message: discord.Message, client: discord.Client):
    if ChangeAvatarState.working:
        await message.reply('Bot is already changing avatar. Please wait until it is done.')
        return

    ChangeAvatarState.working = True
    await message.reply('Changing bot avatar...')
    avatar = await download_image(get_image_url_from_message(message))
    await client.user.edit(avatar=avatar)
    await message.reply('Bot avatar changed.')
    ChangeAvatarState.working = False


@admin_only
async def handle_add_emoji_command(message: discord.Message, emoji_name: str):
    if not message.attachments:
        await message.reply('Please attach an image to your message.')
        return

    image = await download_image(message.attachments[0].url)
    if not image:
        await message.reply('Could not download image.')
        return
    
    await message.guild.create_custom_emoji(name=emoji_name, image=image)
    await message.reply(f'Emoji {emoji_name} added.')