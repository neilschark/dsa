#!/usr/bin/env python3
#####################################################################
# Authors: Neil Schark, Michael Book                                #
# Version: 1.0                                                      #
# Read the README for further instructions, like how to use this    #
# program.                                                          #
#####################################################################
from random import randint
import json
import os
import csv

version_of_program = 1.0

debug_mode = False

class dice_roll_result:
    def __init__(self):
        self.name = ""
        self.talent = ""
        self.type = ""
        self.quality_level = ""
        self.talent_value = ""
        self.remaining_points = ""
        self.dice_values = ""
        self.modification = ""
        self.attribute_names = ""
        self.attribute_values = ""
        self.compensation_points = ""


class Hero:
    def __init__(self):
        self.name = ""
        self.optolith_version = 0
        self.attributes = {}
        self.talents = {}
        self.modification_temp = 0
        self.modification_perm = 0
        self.enabled = True
        self.number_of_successes = 0
        self.number_of_failures = 0
        self.number_of_critical_successes = 0
        self.number_of_critical_failures = 0
        self.number_of_really_critical_failures = 0
        self.number_of_really_critical_successes = 0
        self.number_of_games = 0

    def roll_dices(self, talent_input, modification):
        talent = german_talents[talent_input]
        relevant_attributes = talents[talent]
        # print(modification)
        compensation_points_max = self.talents[talent]
        compensation_points = compensation_points_max
        modification = int(modification) + int(self.modification_perm) + int(self.modification_temp)
        self.modification_temp = 0  # reset temporary modification
        # compensation_points = 0  # just for testing
        # print(compensation_points)
        value_attributes = []
        value_attributes.append(self.attributes[relevant_attributes[0]] + int(modification))
        value_attributes.append(self.attributes[relevant_attributes[1]] + int(modification))
        value_attributes.append(self.attributes[relevant_attributes[2]] + int(modification))
        return_dic = {"modification": modification, "attribute_names": relevant_attributes,
                      "attribute_values": value_attributes,
                      "compensation_points": compensation_points}

        return_element = dice_roll_result()
        return_element.modification = modification
        return_element.attribute_names = relevant_attributes
        return_element.attribute_values = value_attributes
        return_element.compensation_points = compensation_points

        rolls = []

        for counter_dice in range(0, 3):
            roll = randint(1, 20)  # Dice with 20 sites
            rolls.append(roll)

        if rolls.count(1) == 3:
            self.number_of_really_critical_successes += 1
            return_element.name = self.name
            return_element.talent = talent_input
            return_element.type = "really_critical_success"
            return_element.quality_level = str(self.calc_quality(compensation_points_max * 2))
            return_element.talent_value = str(compensation_points_max)
            return_element.remaining_points = str(compensation_points)
            return_element.dice_values = rolls
            return return_element

        if rolls.count(1) == 2:
            self.number_of_critical_successes += 1
            return_element.name = self.name
            return_element.talent = talent_input
            return_element.type = "critical_success"
            return_element.quality_level = str(self.calc_quality(compensation_points_max * 2))
            return_element.talent_value = str(compensation_points_max)
            return_element.remaining_points = str(compensation_points)
            return_element.dice_values = rolls
            return return_element

        if rolls.count(20) == 3:
            self.number_of_really_critical_failures += 1
            return_element.name = self.name
            return_element.talent = talent_input
            return_element.type = "really_critical_failure"
            return_element.quality_level = 0
            return_element.talent_value = str(compensation_points_max)
            return_element.remaining_points = str(compensation_points)
            return_element.dice_values = rolls
            return return_element

        if rolls.count(20) == 2:
            self.number_of_critical_failures += 1
            return_element.name = self.name
            return_element.talent = talent_input
            return_element.type = "critical_failure"
            return_element.quality_level = 0
            return_element.talent_value = str(compensation_points_max)
            return_element.remaining_points = str(compensation_points)
            return_element.dice_values = rolls
            return return_element

        for x, roll in enumerate(rolls):
            if roll > value_attributes[x]:
                if roll - value_attributes[x] <= compensation_points:
                    compensation_points = compensation_points - (roll - value_attributes[x])
                else:
                    number_of_failures += 1
                    self.number_of_failures += 1
                    return_element.name = self.name
                    return_element.talent = talent_input
                    return_element.type = "failure"
                    return_element.quality_level = 0
                    return_element.talent_value = str(compensation_points_max)
                    return_element.remaining_points = 0
                    return_element.dice_values = rolls
                    return return_element
            #x += 1

        self.number_of_successes += 1
        return_dic["name"] = self.name
        return_dic["talent"] = talent_input
        return_dic["type"] = "success"
        return_dic["quality_level"] = str(self.calc_quality(compensation_points))
        return_dic["talent_value"] = str(compensation_points_max)
        return_dic["remaining_points"] = str(compensation_points)
        return_dic["dice_values"] = rolls
        return return_dic

    def calc_quality(self, compensation_points_input):

        if 0 <= compensation_points_input <= 3:
            return 1

        if 4 <= compensation_points_input <= 6:
            return 2

        if 7 <= compensation_points_input <= 9:
            return 3

        if 10 <= compensation_points_input <= 12:
            return 4

        if 13 <= compensation_points_input <= 15:
            return 5

        else:
            return 6


def read_json_files():

    all_files = os.listdir("./helden/")

    heroes_json = []

    for file in all_files:
        if file.endswith(".json"):
            input_file = open("./helden/" + file, "r", encoding="utf-8")
            heroes_json.append(json.loads(input_file.read()))  # read line, convert it to dictionary and append it to list
            input_file.close()

    heroes_temp_attributes = []

    for hero in heroes_json:
        heroes_temp_attributes.append(hero["attr"]["values"])

    heroes = []

    for hero in heroes_temp_attributes:  # read Attributes from json file
        h = Hero()
        for stats in hero:
            h.attributes[str(stats[0])] = stats[1]
        heroes.append(h)

    for i, hero in enumerate(heroes_json):  # read talents
        for tal_count in range(1, 60):  # 59 talents
            key_for_dic = "TAL_" + str(tal_count)
            heroes[i].talents[key_for_dic] = hero["talents"].get(key_for_dic, 0)
        heroes[i].name = hero['name']
        heroes[i].optolith_version = hero["clientVersion"]
        heroes[i].modification_perm = 0
        heroes[i].modification_temp = 0
        heroes[i].enabled = True
    return heroes


def read_talents():
    with open("csv/talents.csv", "r", encoding="utf-8") as input_csv:
        german_talents = {}
        talents_german = {}
        talents = {}
        input_csv.readline()  # skip first line
        csv_reader = csv.reader(input_csv)
        for row in csv_reader:
            row_list = str(row[0]).split(';')
            #print(row_list)
            german_talents[str(row_list[1])] = "TAL_" + str(row_list[0])
            attr_list = row_list[2].split('&')
            talents["TAL_" + str(row_list[0])] = ['ATTR_' + str(attr_list[0]), 'ATTR_' + str(attr_list[1]), 'ATTR_' + str(attr_list[2])]

        talents_german = {value: key for (key, value) in german_talents.items()}
        return talents, german_talents, talents_german


def read_attributes():
    with open("csv/attributes.csv", "r", encoding="utf-8") as input_csv:
        german_attributes = {}
        input_csv.readline()  # skip first line
        csv_reader = csv.reader(input_csv)
        for row in csv_reader:
            row_list = str(row[0]).split(';')
            #print(row_list)
            german_attributes[str(row_list[1])] = "ATTR_" + str(row_list[0])

    attributes_german = {value: key for (key, value) in german_attributes.items()}
    return german_attributes, attributes_german


def console_output_result(input_dictionary, flag):
    if flag:
        print("*************************************")
        print("Name: " + str(input_dictionary["name"]))
        print("Aktueller Modifikator auf diese Probe: " + str(input_dictionary["modification"]))
        for m, attribute in enumerate(input_dictionary["attribute_names"]):
            print("Wert inkl. Modifikatoren für " + str(attributes_german[attribute]) + ": " + str(input_dictionary["attribute_values"][m]))

        print("Anzahl verfügbarer Talentpunkte: " + str(input_dictionary["compensation_points"]))
        print("Talent: " + str(input_dictionary["talent"]))
        print(str(input_dictionary["type"]))
        print("Talentpunkte: " + str(input_dictionary["talent_value"]))
        print("Verbleibende Talentpunkte: " + str(input_dictionary["remaining_points"]))
        print("Qualitätsstufe: " + str(input_dictionary["quality_level"]))
        print("Würfelergebnis: " + str(input_dictionary["dice_values"]))
        print("*************************************")


number_of_successes = 0
number_of_failures = 0
number_of_critical_successes = 0
number_of_critical_failures = 0
number_of_really_critical_failures = 0
number_of_really_critical_successes = 0
number_of_games = 0

heroes = read_json_files()
talents, german_talents, talents_german = read_talents()
german_attributes, attributes_german = read_attributes()


def main():
    global heroes

    print("Programmversion: " + str(version_of_program))
    for hero in heroes:
        print("Der Held " + str(hero.name) + " wurde erstellt mit Optolith Version " + str(hero.optolith_version))

    while True:
        debug_mode = True
        input_talent = input(
            "Welche Fähigkeit? (z.B. Klettern) oder 'M' um heldenspezifischen Modifikator zu ändern, oder 'S' für die Statistiken")

        if input_talent == "m" or input_talent == "M":
            print("Eingelesene Helden: ")
            for i, hero in enumerate(heroes):
                print("[" + str(i) + "]" + hero["name"])
            input_hero_choice = input("Welcher Held soll geändert werden? (z.B. 1) ")
            input_hero_specific_mod = input("Auf welchen gesamten Modifikator? (z.B. 1 oder -2)")
            heroes[int(input_hero_choice)].modification_perm = input_hero_specific_mod
        elif input_talent not in german_talents:
            print("Ungültige Eingabe erkannt.")
        elif input_talent == "s" or input_talent == "S":
            number_of_games = (number_of_successes + number_of_failures + number_of_really_critical_failures + number_of_really_critical_successes + number_of_critical_failures + number_of_critical_successes) / len(heroes)
            print("Anzahl Erfolge: " + str(number_of_successes))
            print("Anzahl Misserfolge: " + str(number_of_failures))
            print("Anzahl kritischer Erfolge: " + str(number_of_critical_successes))
            print("Anzahl kritischer Misserfolge: " + str(number_of_critical_failures))
            print("Anzahl besonders kritischer Misserfolge: " + str(number_of_really_critical_failures))
            print("Anzahl besonders kritischer Erfolge: " + str(number_of_really_critical_successes))
            print("Anzahl gesamter Spiele: " + str(number_of_games))
            print("+++++++++++++++++++++++++")
        else:
            input_modification = input("Welcher Bonus/Malus (z.B. -2 oder +1) ")
            for hero in heroes:
                output = hero.roll_dices(input_talent, input_modification)
                console_output_result(output, debug_mode)  # print results


if __name__ == '__main__':
    main()



