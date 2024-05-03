import json

def retreive_facts(firstAnimal, secondAnimal):
    with open('animal_facts.json', 'r') as f: #accesses json file scraped from factanimal.com
        data = json.load(f)

    #store dictionaries for each animal in these two variables
    firstAnimal = parse_json(firstAnimal, data)
    secondAnimal = parse_json(secondAnimal, data)

    if not firstAnimal or not secondAnimal:
        print("One animal was not found.")
        return

    keys = list(firstAnimal.keys()) #attribute keys
    #"randomly" selects facts by alternating which animal the facts come from every other loop
    for i in range(min(len(keys), 9)):
        if i % 2 == 0:
            print(f"{keys[i].capitalize()}: {firstAnimal[keys[i]]}")
        else:
            print(f"{keys[i].capitalize()}: {secondAnimal[keys[i]]}")

# this function searches for the animal names in the json file and returns the dictionaries for each
def parse_json(animal_name, data):
    for animal in data:
        #finds the first entry that includes the provided string
        if animal_name.lower() in animal['title'].lower():
            return animal['attributes']
    return None
def main():
    #input
    animalInput1 = input("Pick the name of the first animal you want:")
    animalInput2 = input("Pick the name of the second animal you want:")

    #mash front of animal one and back of animal two names together
    creature = animalInput1[:len(animalInput1) // 2] + animalInput2[len(animalInput2) // 2:]
    print(f"The name of the creature you created is:  {creature}")
    print("Here are some facts about your creature: ")

    retreive_facts(animalInput1, animalInput2)


main()

