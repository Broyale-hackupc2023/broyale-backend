

class User:

	def __init__(self, sid, name):
		self.sid = sid
		self.name = name
		self.room = None


	def __str__(self):
		return self.name


	def join(self, room):
		if self.room is not None:
			self.room.remove_user(self)
		room.add_user(self)
		self.room = room


	def leave_room(self):
		if self.room is not None:
			self.room.remove_user(self)
			self.room = None


	def to_dict(self):
		return {
			'id': self.sid,
			'name': self.name,
		}