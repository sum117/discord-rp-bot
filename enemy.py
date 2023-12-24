
from player import Player
from random import randint
from discord import Message
from items import ITEM_DATABASE, Item
from utilities import create_embed

"""
Some notes on drop tables here:

Drop tables are represented as a dictionary of {item_id: drop_chance}, drop chances can range from 0.01 to 100, 
these numbers representing the percent chance of an event occuring.

Drop chances are accumulative, for example:

full_table = {-1: .05, 0: .05, 1: 10, 2: 89.9}

In this drop table:
	rolls from 1 to 5 will reward nothing / .05% chance
	rolls from 6 to 10 will reward item_id 0 / .05% chance
	rolls from 11 to 1010 will reward item_id 1 / 10% chance
	rolls from 1011 to 10000 will reward item_id 2 / 89.95% chance

The drop chances in this table represent the real chance of items dropping because they sum to 100;
however, in the next example this will not be the case:

partial_table = {0: 5, 1: 5}

In this drop table:
	rolls from 1 to 500 will reward item_id 0
	rolls from 501 to 1000 will reward item_id 1

Although these items have a drop chance of 5, they actuall both have a 50% chance of being dropped 
"""

class Enemy:
	def __init__(self, name: str, description: str, level: int, max_health: int, attack: int, defense: int, exp: int, drop_table: dict[int, int], icon_url: str, channel):
		self.adversaries = {} #dict that stores player id keys and the amount of damage they did as the value for awarding exp
		self.name, self.description, self.level, self.max_health, self.attack, self.defense, self.drop_table, self.icon_url, self.exp, self.channel = name, description, level, max_health, attack, defense, drop_table, icon_url, exp, channel
		self.current_health = self.max_health


	def attack_player(self, player: Player, msg: Message):
		damage = int(self.attack * (self.attack / player.defense))
		player.take_damage(damage)


	def take_damage(self, amount: int, player: Player):
		self.adversaries[player.player_id] = self.adversaries.get(player.player_id, 0) + amount

		self.current_health = min(self.current_health - amount, 0)
		if self.current_health == 0: self.die()
		else: self.display(self.channel)
		
		
	def die(self):
		total_damage = sum(self.adversaries.values())
		for pid in self.adversaries:
			contribution = self.adversaries[pid] / total_damage
			player = Player(pid)
			if (reward:=self.roll_loot()): 
				if (reward.is_stackable()): reward.stack_size = self.roll_stack()
				player.award_item(reward)
				player.award_exp(int(self.calculate_exp() * contribution))

	def calculate_exp(self):
		# TODO: write a formula for calculating exp instead of passing a flat value
		return self.exp

	def roll_loot(self) -> Item | None:
		"""
		rolls an item from a drop table
		"""
		possible_drops = sorted(self.drop_table.items(), key=lambda x: x[1], reverse=True) #sort items by drop rates in ascending order
		drop_sum = sum(map(lambda x: x*100, self.drop_table.values()))
		rolling_sum = 0
		roll = randint(1, drop_sum)
		for item_id, drop_rate in possible_drops:
			if roll <= drop_rate * 100 + rolling_sum: return ITEM_DATABASE[item_id]
			rolling_sum += drop_rate * 100
		return None
	
	def roll_stack(self, item: Item):
		if item.is_stackable(): return 1
		return randint(1, 5)
	
	async def display(self):
		embed1 = create_embed()
		embed2 = create_embed(self.name, self.description)
		embed1.set_image(url=self.icon_url)
		await self.channel.send(embed=embed1)
		await self.channel.send(embed=embed2)

class Goblin(Enemy):
	def __init__(self, channel):
		level, max_health, attack, defense = randint(1, 5), randint(1, 5), randint(1, 5), randint(1, 5)
		super().__init__(
			name='Goblin', 
			description='No, you can\'t fuck her...', 
			level=level, 
			max_health=max_health, 
			attack=attack, 
			defense=defense, 
			exp=30,
			drop_table={0: 50, 1:50}, 
			icon_url='https://cdn.discordapp.com/attachments/1188112675620786246/1188112726367682601/iu.png',
			channel=channel
		)
