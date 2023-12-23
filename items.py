from enums import ItemType, ItemRarity


MAX_STACK_SIZE = 99

class Item:
	_colors = {
		ItemRarity.COMMON: '{}',
		ItemRarity.UNCOMMON: '[2;33m{}[0m',
		ItemRarity.RARE: '[0m[2;34m{}[0m',
		ItemRarity.EPIC: '[0m[2;36m{}[0m',
		ItemRarity.LEGENDARY: '[2;35m{}[0m',
		ItemRarity.MYTHIC: '[2;35m[0m[2;41m[2;30m[0m[2;41m[0m[2;41m[2;36m[2;31m[2;34m[0m[2;31m[2;41m[0m[2;36m[2;41m[0m[2;41m[0m[2;45m[2;31m[2;35m[2;31m[2;47m{}[0m[2;31m[2;45m[0m[2;35m[2;45m[0m[2;31m[2;45m[0m[2;45m[0m'
	}

	def __init__(self, **kwargs):
		self.__dict__ |= kwargs
		#removes the need to pass a stack size for items that don't stack
		if not self.is_stackable(): self.stack_size = 1

	#must be printed to discord inside of a string with ansi formatting f'```ansi\n{text}\n``` 
	def __str__(self):
		color_template = self._colors[self.rarity]
		return color_template.format(self.name)
	
	def is_stackable(self):
		#types 7 and 8 are MATERIAL and CONSUMABLE which are stackable
		return self.type.value >= 7
	

	
ITEM_DATABASE = {
	0: Item(item_id=0, type=ItemType.WEAPON, name='Longsword', attack=10, defense=0, rarity=ItemRarity.COMMON),
	1: Item(item_id=1, type=ItemType.MATERIAL, name='Iron Ore', rarity=ItemRarity.UNCOMMON, stack_size=10),
	2: Item(item_id=2, type=ItemType.CONSUMABLE, name='Health Potion', rarity=ItemRarity.RARE, stack_size=3),
	3: Item(item_id=3, type=ItemType.CHEST, name='Cloak of the Veil', defense=45, rarity=ItemRarity.EPIC),
	4: Item(item_id=4, type=ItemType.HELMET, name='Helm of the Boar God', defense=500, rarity=ItemRarity.LEGENDARY),
	5: Item(item_id=5, type=ItemType.MATERIAL, name='Eye of Ragathar', attack=10, defense=0, rarity=ItemRarity.MYTHIC, stack_size=1),
}
