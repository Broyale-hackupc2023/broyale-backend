import openai
import os
from dotenv import load_dotenv
# load_dotenv()
import random

class DungeonMaster:

	def __init__(self, characters):
		self.characters = characters
		api_key = os.getenv('OPENAI_API_KEY')
		openai.api_key = api_key

		self.messages = [
			{
				"role": "system",
				"content": "You are a dungeon master. The players are in a setting of your initial choosing. You must be actively trying to kill them. You must take into account the responses from each player and briefly (one paragraph) narrate the outcome of said actions, based on the surroundings and the characters' abilities. You must respond to the answers of every character within the same explanation. You must take the actions chosen by every player into account when narrating your response, but ignore everything that blatantly does not make sense within the story. Each interaction of each user is assigned a number from 1 to 20 between parenthesis: the lower the number the more unlikely the action will be to succeed. If a player gets a ridiculously low roll make it funny. When you describe the result to each of the character's actions include the rolled number, as a way to justify their success/failure to the player ['player_name':'roll']. Make sure to do this for all characters which's interaction with the world you describe. If the player requests to do aything beyond superhuman capacity through their character's actions, you musn't let them, and instead make them look silly. All about the response must be coherent with the previous context and help create a story."
			},
			{
				"role": "assistant",
				"content": "I am your dungeon master. I will be narrating the story and controlling the NPCs. You can ask me anything about the world and I will answer you. You can also ask me to do things and I will try to do them. You may call me Great Peter The III (GPT-3)."
			}
		]

	def get_output(self, inputs):
		if len(inputs) != len(self.characters):
			raise GenerationError("Every character must have an input")

		self.actions = ""

		for input in inputs:
			if input.user.name not in self.characters:
				raise GenerationError(f"Input character '{input.user.name}' not found")
			self.actions += input.user.name + " responds " + input.prompt + "(" + str(input.roll) + "); "

		self.messages.append({
			"role": "user",
			"content": self.actions
		})

		# Generate openai output
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=self.messages
			)

		output = response.choices[0].message.content
		finish_reason = response.choices[0].finish_reason

		self.messages.append({
			"role": "assistant",
			"content": output
		})

		if finish_reason != 'stop':
			raise GenerationError(f'La generación del output ha terminado por el siguiente motivo: "{finish_reason}"')

		return output


class Input:

	def __init__(self, user, prompt, roll):
		self.user = user
		self.prompt = prompt
		self.roll = roll


	def __str__(self):
		return f"[{self.user.name}]: {self.prompt} ({self.roll})"

# Define a GenerationError
class GenerationError(Exception):
	pass