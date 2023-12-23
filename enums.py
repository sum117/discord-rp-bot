from enum import Enum

class ItemType(Enum):
	WEAPON = 0
	HELMET = 1
	CHEST = 2
	ARMS = 3
	LEGS = 4
	RING = 5
	AMULET = 6
	CONSUMABLE = 7
	MATERIAL = 8

class ItemRarity(Enum):
	COMMON = 0
	UNCOMMON = 1
	RARE = 2
	EPIC = 3
	LEGENDARY = 4
	MYTHIC = 5