

class Message:
	
	def __init__(self, text):
		self.text = text
		self.type = 'unknown'

	def to_dict(self):
		return {
			'type': self.type,
			'text': self.text,
		}



class UserMessage:

	def __init__(self, user, text, roll):
		self.user = user
		self.text = text
		self.roll = roll
		self.type = 'user'

	def to_dict(self):
		return {
			'type': self.type,
			'user': self.user.to_dict(),
			'text': self.text,
			'roll': self.roll
		}




class AssistantMessage:

	def __init__(self, text):
		self.text = text
		self.type = 'assistant'

	def to_dict(self):
		return {
			'type': self.type,
			'text': self.text,
		}