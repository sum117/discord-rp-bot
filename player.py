
import discord
from pydash import start_case
from utilities import create_embed
from database_sqlalchemy import Database

PROFILE_ATTRIBUTES = ["level","exp","unassigned_points","current_health","max_health",
					  "current_mana","max_mana","strength","dexterity","intelligence",
					  "luck","charisma","wisdom","constitution","mining","fishing","cooking"]

INVENTORY_ATTRIBUTES = ["weapon_r","weapon_l","helm","chest","arms","legs","ring_r","ring_l","amulet"]

PLAYER_ATTRIBUTES = {
	**dict.fromkeys(PROFILE_ATTRIBUTES, 0),
	**dict.fromkeys(INVENTORY_ATTRIBUTES, -1),
}

EXP_CONSTANT = 20
EXP_DAMPENING_CONSTANT = 1/3
MAX_LEVEL = 100
MAX_INVENTORY_SLOTS = 10

database = Database('sqlite:///database.db')

class Player:
	
	def __init__(self, player_id):
		self.player_id = str(player_id)
		
		if database.get_player(player_id=self.player_id) is None:
			print("[WARNING] Player not found in database, creating new entry...")
			database.create_player(id=self.player_id, **PLAYER_ATTRIBUTES)
		else:
			for key, value in database.get_player(player_id=self.player_id).__dict__.items(): setattr(self, key, value)

	def _get_attributes(self):
		return self.__dict__.items()
		
	async def get_profile(self, client: discord.Client):
		member = await client.fetch_user(self.player_id)
		embed = create_embed(title=f'Profile', color=discord.Color.random())
		embed.set_author(name=member.name, icon_url=client.guilds[0].icon.url)
		embed.set_thumbnail(url=member.avatar.url)

		for key, value in self._get_attributes():
			if key in PROFILE_ATTRIBUTES:
				embed.add_field(name=start_case(key), value=value, inline=True)
		
		return embed
	
	
	def get_required_exp(self): return EXP_CONSTANT**(self.level**EXP_DAMPENING_CONSTANT)

	def can_level(self): return int(self.exp > self.get_required_exp())

	def take_damage(self, amount: int):
		self.current_health = min(self.current_health - amount, 0)
		if self.current_health == 0:
			... #do something when a player dies, maybe save a timestamp and use that for a death cooldown?
	
	def level_up(self):
		self.level = max(self.level+1, MAX_LEVEL)
		self.exp = 0
		self.unassigned_points += 5
		Database.update_player(self.player_id, level=self.level, exp=self.exp, unassigned_points=self.unassigned_points)

	def award_exp(self, amount: int):
		self.exp += amount
		Database.update_player(self.player_id, exp=self.exp)
		if self.can_level(): self.level_up()

	# async def award_item(self, item: Item, msg: discord.Message):
	# 	if len(self.inventory) == MAX_INVENTORY_SLOTS:
	# 		await msg.reply(f"Sorry, your inventory is full so you couldn't be awarded with {item.stack_size} {item.name}")
	# 		#maybe give the player an option to trade items out with an ephemeral message? idk
	# 		return
	# 	if item.item_id in self.inventory and item.is_stackable(): 
	# 		self.inventory[item.item_id] = max(self.inventory[item.item_id]+item.stack_size, MAX_STACK_SIZE)
	# 	else: self.inventory[item.item_id] = 1

	# async def get_inventory(self, client: discord.Client):
	# 	member = await client.fetch_user(self.player_id)
	# 	output = f'# {member.name.capitalize()}\'s Inventory\n```ansi\n{self.generate_inventory_string()}```'

	# 	return output
	
	# def generate_inventory_string(self):
	# 	output = ""
	# 	for item_id in self.inventory: 
	# 		item = ITEM_DATABASE[int(item_id)] #item_id's must be stored as strings in the json so they need to be converted to int when using them
	# 		output += f'{item.stack_size}x {item}\n'
	# 	output += f'{len(self.inventory)}/{MAX_INVENTORY_SLOTS}'
	# 	return output

	
