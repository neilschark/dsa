from random import randint
import json
import os

from test import visualize

all_files = os.listdir("./")

heroes = []

for file in all_files:
    if file.endswith(".json"):
        input_file = open(file, "r")
        heroes.append(json.loads(input_file.read()))  # read line, convert it to dictionary and append it to list
        input_file.close()


def roll_dices(talent, modificator, current_hero):
    print("*************************************")
    print("Es würfelt: " + str(current_hero["name"]))
    relevant_attributes = talents[talent]
    # print(modificator)
    compensation_points = current_hero[talent]
    # print(compensation_points)
    value_attributes = []
    value_attributes.append(current_hero[relevant_attributes[0]] + modificator)
    value_attributes.append(current_hero[relevant_attributes[1]] + modificator)
    value_attributes.append(current_hero[relevant_attributes[2]] + modificator)
    print("Wert inkl. Multiplikator für " + str(relevant_attributes[0]) + ": " + str(value_attributes[0]))
    print("Wert inkl. Multiplikator für " + str(relevant_attributes[1]) + ": " + str(value_attributes[1]))
    print("Wert inkl. Multiplikator für " + str(relevant_attributes[2]) + ": " + str(value_attributes[2]))
    print("Anzahl verfügbarer Talentpunkte: " + str(compensation_points))

    global number_of_successes
    global number_of_failures
    global number_of_critical_successes
    global number_of_critical_failures
    global number_of_really_critical_failures
    global number_of_really_critical_successes

    rolls = []

    # global number_of_20
    # bereits_20 = False

    for roll in range(0, 3):
        roll = randint(1, 20)  # Würfel mit 20 Seiten
        rolls.append(roll)

    print("Es wurden folgende Werte geworfen:")
    print(rolls)

    if rolls.count(1) == 3:
        print("BESONDERER KRITISCHER ERFOLG")
        print("*************************************")
        number_of_really_critical_successes += 1
        return

    if rolls.count(1) == 2:
        print("KRITISCHER ERFOLG")
        print("*************************************")
        number_of_critical_successes += 1
        return

    if rolls.count(20) == 3:
        print("BESONDERER KRITISCHER MISSERFOLG")
        print("*************************************")
        number_of_really_critical_failures += 1
        return

    if rolls.count(20) == 2:
        print("KRITISCHER MISSERFOLG")
        print("*************************************")
        number_of_critical_failures += 1
        return

    x = 0  # TODO: ZIP-FUNCTION
    for roll in rolls:
        if roll > value_attributes[x]:
            if roll - value_attributes[x] <= compensation_points:
                compensation_points = compensation_points - (roll - value_attributes[x])
            else:
                print("MISSERFOLG")
                print("*************************************")
                number_of_failures += 1
                return
        x += 1

    print("ERFOLG")
    number_of_successes += 1
    print("*************************************")

# number_of_20 = 0

number_of_successes = 0
number_of_failures = 0
number_of_critical_successes = 0
number_of_critical_failures = 0
number_of_really_critical_failures = 0
number_of_really_critical_successes = 0

held1 = {"name": "Jürgen", "mut": 10, "klugheit": 10, "intuition": 10, "charisma": 10, "fingerfertigkeit": 10, "gewandheit": 10, "konstitution": 10, "koerperkraft": 10, "klettern": 0, "koerperbeherrschung": 10}

talents = {"klettern": ["mut", "gewandheit", "koerperkraft"], "koerperbeherrschung": ["gewandheit", "gewandheit", "konstitution"]}

# input_attribut = input("Welche Fähigkeit? (z.B. klettern)")
# input_modificator = input("Welcher Bonus/Malus (z.B. -2 oder +1) ")

# for hero in heroes:
    # roll_dices(input_attribut, input_modificator, hero)
number_of_tests = 100000
for i in range(0, number_of_tests):
    roll_dices("klettern", 0, held1)

print("Anzahl erfolge: " + str(number_of_successes))
print("Anzahl misserfolge: " + str(number_of_failures))
print("Anzahl kritischer erfolge: " + str(number_of_critical_successes))
print("Anzahl kritischer misserfolge: " + str(number_of_critical_failures))
print("Anzahl besonders kritischer misserfolge: " + str(number_of_really_critical_failures))
print("Anzahl besonders kritischer erfolge: " + str(number_of_really_critical_successes))
# print("Anzahl 20er: " + str(number_of_20))
# print("Kritischer Misserfolg + Misserfolg: " + str(number_of_critical_failures + number_of_failures))

print("+++++++++++++++++++++++++")
results = [number_of_really_critical_successes, number_of_critical_successes,
           number_of_successes, number_of_failures,
           number_of_critical_failures, number_of_really_critical_failures]
visualize(number_of_tests, results)
