from character import Character
from dungeon_master import DungeonMaster, Input

def main():
	num_chars = int(input('Enter the number of characters: '))
	characters = []
	for i in range(num_chars):
		name = input(f'Enter the name of character {i + 1}: ')
		characters.append(Character(name))
	
	dungeon_master = DungeonMaster(characters)

	while True:
		inputs = []
		for character in characters:
			prompt = input(f'[{character.name}]: ')
			inputs.append(Input(character, prompt))

		output = dungeon_master.get_output(inputs)
		print("========================================")
		print(output)
		print("========================================")



if __name__ == '__main__':
	main()