import json

class Database:
	@staticmethod
	def save():
		with open("database.json", "w") as file:
			json.dump(database, file)

	@staticmethod
	def load():
		with open("database.json", "r") as file:
			database = json.load(file)
		return database
	

database = Database.load()