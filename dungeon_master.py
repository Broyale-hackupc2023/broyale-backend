


class DungeonMaster:

	def __init__(self, characters):
		self.characters = characters

	
	def get_output(self, inputs):
		if len(inputs) != len(self.characters):
			raise GenerationError("Every character must have an input")

		for input in inputs:
			if input.character not in self.characters:
				raise GenerationError(f"Input character '{input.character.name}' not found")

		# Generar output...
		# ...

		return "You are in a dungeon. There are dragons. You are likely to be eaten by a grue."


class Input:
	
	def __init__(self, character, prompt):
		self.character = character
		self.prompt = prompt


	def __str__(self):
		return f"[{self.character.name}] {self.prompt}"

# Define a GenerationError
class GenerationError(Exception):
	pass