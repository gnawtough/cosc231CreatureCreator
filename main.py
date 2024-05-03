import json


def retreive_facts(firstAnimal, secondAnimal):
    with open('animal_facts.json', 'r') as f:
        data = json.load(f)

    firstAnimal = parse_json(firstAnimal, data)
    secondAnimal = parse_json(secondAnimal, data)
    print(firstAnimal, secondAnimal)

def parse_json(animal_name, data):
    for animal in data:
        if animal_name.lower() in animal['title'].lower():
            print(animal['title'])
            return animal['attributes']

    return None
def main():
    animalInput1 = input("Pick the name of the first animal you want:")
    animalInput2 = input("Pick the name of the second animal you want:")

    creature = animalInput1[:len(animalInput1) // 2] + animalInput2[len(animalInput2) // 2:]
    print(f"The name of the creature you created is:  {creature}")
    print("Here are some facts about your creature: ")

    retreive_facts(animalInput1, animalInput2)


main()

