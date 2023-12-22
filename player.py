
import discord
from pydash import start_case
from database import database, Database

PLAYER_ATTRIBUTES = {
	"level": 0,
	"xp": 0,
	"unassigned_points": 0,
	"current_health": 0,
	"max_health": 0,
	"current_mana": 0,
	"max_mana": 0,
	"strength": 0,
	"dexterity": 0,
	"intelligence": 0,
	"luck": 0,
	"charisma": 0,
	"wisdom": 0,
	"constitution": 0,
	"mining": 0,
	"fishing": 0,
	"cooking": 0,
}

class Player:
	
	def __init__(self, player_id):
		print(player_id)
		self.player_id = str(player_id)
		if not self.player_id in database:
			print("[WARNING] Player not found in database, creating new entry...")
			database[self.player_id] = self.__dict__ | PLAYER_ATTRIBUTES
			Database.save()
		else:
			print("Loading Player")
			for key, value in self._get_attributes(): setattr(self, key, value)

	def _get_attributes(self):
		return database[self.player_id].items()
		
	async def get_profile(self, client: discord.Client):
		member = await client.fetch_user(self.player_id)
		embed = discord.Embed(title=f'{member.name.title()}]\'s Profile', color=discord.Color.random())
		embed.set_author(name=member.name, icon_url=client.guilds[0].icon.url)
		embed.set_thumbnail(url=member.avatar.url)
		for key, value in self._get_attributes(): embed.add_field(name=start_case(key), value=value, inline=True)
		
		return embed

