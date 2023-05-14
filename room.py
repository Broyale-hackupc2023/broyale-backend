import random

class Room:

	def __init__(self, id, name, description, owner):
		self.id = id
		self.name = name
		self.description = description
		self.owner = owner
		self.users = []
		self.max_users = 5
		self.active = False

	
	def __str__(self):
		return f"<Room {self.id}: {self.name}>"

	
	def add_user(self, user):
		if user not in self.users:
			self.users.append(user)
			user.room = self


	def remove_user(self, user):
		if user in self.users:
			self.users.remove(user)
			user.room = None

	
	def start_game(self):
		self.active = True


	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'owner': self.owner.to_dict(),
			'players': [user.to_dict() for user in self.users],
			'max_players': self.max_users,
			'active': self.active,
		}