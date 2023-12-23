
import discord
from pydash import start_case
from database import database, Database
from items import Item
from utilities import create_embed
from items import ITEM_DATABASE, MAX_STACK_SIZE

PROFILE_ATTRIBUTES = ["level","exp","unassigned_points","current_health","max_health",
					  "current_mana","max_mana","strength","dexterity","intelligence",
					  "luck","charisma","wisdom","constitution","mining","fishing","cooking"]

INVENTORY_ATTRIBUTES = ["weapon_r","weapon_l","helm","chest","arms","legs","ring_r","ring_l","amulet"]

PLAYER_ATTRIBUTES = {
	**dict.fromkeys(PROFILE_ATTRIBUTES, 0),
	**dict.fromkeys(INVENTORY_ATTRIBUTES, -1),
	"inventory": {}
}

EXP_CONSTANT = 20
EXP_DAMPENING_CONSTANT = 1/3
MAX_LEVEL = 100
MAX_INVENTORY_SLOTS = 10

class Player:
	
	def __init__(self, player_id):
		self.player_id = str(player_id)
		if not self.player_id in database:
			print("[WARNING] Player not found in database, creating new entry...")
			database[self.player_id] = self.__dict__ | PLAYER_ATTRIBUTES
			Database.save()
		else:
			for key, value in self._get_attributes(): setattr(self, key, value)

	def _get_attributes(self):
		return database[self.player_id].items()
		
	async def get_profile(self, client: discord.Client):
		member = await client.fetch_user(self.player_id)
		embed = create_embed(title=f'Profile', color=discord.Color.random())
		embed.set_author(name=member.name, icon_url=client.guilds[0].icon.url)
		embed.set_thumbnail(url=member.avatar.url)
		for key, value in self._get_attributes(): embed.add_field(name=start_case(key), value=value, inline=True)
		
		return embed
	
	async def get_inventory(self, client: discord.Client):
		member = await client.fetch_user(self.player_id)
		outp = f'**{member.name.capitalize()}\'s Inventory**\n```ansi\n{self.generate_inventory_string()}```'

		return outp
	
	def generate_inventory_string(self):
		outp = ""
		for item_id in self.inventory: 
			item = ITEM_DATABASE[int(item_id)] #item_id's must be stored as strings in the json so they need to be converted to int when using them
			outp += f'{item.stack_size}x {item}\n'
		outp += f'{len(self.inventory)}/{MAX_INVENTORY_SLOTS}'
		return outp

	def get_required_exp(self): return EXP_CONSTANT**(self.level**EXP_DAMPENING_CONSTANT)

	def can_level(self): return int(self.exp > self.get_required_exp())

	def take_damage(self, amount: int):
		self.current_health = min(self.current_health - amount, 0)
		if self.current_health == 0:
			... #do something when a player dies, maybe save a timestamp and use that for a death cooldown?
	
	def level_up(self):
		self.level = max(self.level+1, MAX_LEVEL)
		self.exp = 0

	def award_exp(self, amount: int):
		self.exp += amount
		if self.can_level(): self.level_up()

	async def award_item(self, item: Item, msg: discord.Message):
		if len(self.inventory) == MAX_INVENTORY_SLOTS:
			await msg.reply(f"Sorry, your inventory is full so you couldn't be awarded with {item.stack_size} {item.name}")
			#maybe give the player an option to trade items out with an ephemeral message? idk
			return
		if item.item_id in self.inventory and item.is_stackable(): 
			self.inventory[item.item_id] = max(self.inventory[item.item_id]+item.stack_size, MAX_STACK_SIZE)
		else: self.inventory[item.item_id] = 1


	
