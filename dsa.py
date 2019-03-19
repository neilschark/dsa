from random import randint
import json
import os

all_files = os.listdir("./")

json_files = []
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
    # print(modifikator)
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

    critical_failure = False
    critical_success = False
    failure = False
    rolls = []

    global number_of_20
    bereits_20 = False

    for x in range(0, 3):
        wurf = randint(1, 20)  # Würfel mit 20 Seiten
        rolls.append(wurf)
        if wurf == 20:
            # if bereits_20 == False:
                # number_of_20 += 1
            # bereits_20 = True
            if randint(1, 20) > value_attributes[x]:
                critical_failure = True
            else:
                failure = True
        elif wurf == 1:
            if randint(1, 20) <= value_attributes[x]:
                critical_success = True
        elif wurf <= value_attributes[x]:
            pass
        elif wurf > value_attributes[x]:
            if wurf - value_attributes[x] <= compensation_points:
                compensation_points = compensation_points - (wurf - value_attributes[x])
                print(compensation_points)
            else:
                failure = True

    global number_of_successes
    global number_of_failures
    global number_of_critical_successes
    global number_of_critical_failures

    print("Es wurden folgende Werte geworfen:")
    for wurf_wert in rolls:
        print(wurf_wert)

    if critical_failure:
        print("KRITISCHER MISSERFOLG")
        # number_of_critical_failures += 1
    elif failure:
        print("MISSERFOLG")
        # number_of_failures += 1
    elif critical_success:
        print("KRITISCHER ERFOLG")
        # number_of_critical_successes += 1
    else:
        print("ERFOLG")
        # number_of_successes += 1

    print("*************************************")

# number_of_20 = 0

# number_of_successes = 0
# number_of_failures = 0
# number_of_critical_successes = 0
# number_of_critical_failures = 0


# held1 = {"name": "Jürgen", "mut": 10, "klugheit": 10, "intuition": 10, "charisma": 10, "fingerfertigkeit": 10, "gewandheit": 10, "konstitution": 10, "koerperkraft": 10, "klettern": 0, "koerperbeherrschung": 10}

talents = {"klettern": ["mut", "gewandheit", "koerperkraft"], "koerperbeherrschung": ["gewandheit", "gewandheit", "konstitution"]}

input_attribut = input("Welche Fähigkeit? (z.B. klettern)")
input_modificator = input("Welcher Bonus/Malus (z.B. -2 oder +1) ")

for hero in heroes:
    roll_dices(input_attribut, input_modificator, hero)

# for i in range(0, 100):
    # roll_dices(input_attribut, int(input_modificator), held1)

# print("Anzahl erfolge: " + str(number_of_successes))
# print("Anzahl misserfolge: " + str(number_of_failures))
# print("Anzahl kritischer erfolge: " + str(number_of_critical_successes))
# print("Anzahl kritischer misserfolge: " + str(number_of_critical_failures))

# print("Anzahl 20er: " + str(number_of_20))
# print("Kritischer Misserfolg + Misserfolg: " + str(number_of_critical_failures + number_of_failures))

print("+++++++++++++++++++++++++")
