import json

def main():
    animalInput1 = input("Pick the name of the first animal you want:")
    animalInput2 = input("Pick the name of the second animal you want:")

    creature = animalInput1[:len(animalInput1) // 2] + animalInput2[len(animalInput2) // 2:]
    print(f"The name of the creature you created is:  {creature}")
    print("Here are some facts about your creature: ")
main()

