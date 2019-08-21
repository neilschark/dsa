#!/usr/bin/env python3
#####################################################################
# Authors: Neil Schark, Michael Book                                #
# Version: 1.0                                                      #
# Read the README for further instructions, like how to use this    #
# program.                                                          #
#####################################################################
from tkinter import *
import dsa


def update_statistics():
    """Updated hero statistics in gui"""
    successLabel.config(text="Anzahl Erfolge: {}".format(dsa.number_of_successes))
    criticalSuccessLabel.config(text="Anzahl kritischer Erfolge: {}".format(dsa.number_of_critical_successes))
    reallyCriticalSuccessLabel.config(text="Anzahl besonders kritischer Erfolge: {}".format(
        dsa.number_of_really_critical_successes))
    failureLabel.config(text="Anzahl Misserfolge: {}".format(dsa.number_of_failures))
    criticalFailureLabel.config(text="Anzahl kritischer Misserfolge: {}".format(dsa.number_of_critical_failures))
    reallyCriticalFailureLabel.config(text="Anzahl besonders kritischer Misserfolge: {}".format(
        dsa.number_of_really_critical_failures))


def check_heroes_enabled(event):
    """checks if heroes are checked to take part in the next roll and update the status in Hero instance"""
    for hero_in_func in dsa.heroes:
        if hero_in_func.name == event.widget.cget("text"):
            if hero_in_func.enabled is True:
                hero_in_func.enabled = False
                break
            elif hero_in_func.enabled is False:
                hero_in_func.enabled = True
                break


def print_result(position, outcome_dic):
    """prints the last roll results to the gui"""
    new_text = ""
    if outcome_dic["type"] == "success":
        new_text += "Erfolg"
    elif outcome_dic["type"] == "failure":
        new_text += "Misserfolg"
        outcome_dic["quality_level"] = "0"
    elif outcome_dic["type"] == "really_critical_success":
        new_text += "Besonders kritischer Erfolg"
    elif outcome_dic["type"] == "critical_success":
        new_text += "Kritischer Erfolg"
    elif outcome_dic["type"] == "really_critical_failure":
        new_text += "Besonders kritischer Misserfolg"
        outcome_dic["quality_level"] = "0"
    elif outcome_dic["type"] == "critical_failure":
        new_text += "Kritischer Misserfolg"
        outcome_dic["quality_level"] = "0"
    new_text += " | QS {} | FP {} | {} | FW {}".format(outcome_dic["quality_level"], outcome_dic["remaining_points"],
                                                       outcome_dic["dice_values"], outcome_dic["talent_value"])
    results[position].config(text=new_text)


def talent_press(event):
    """calls function roll_dice for the talent that was pressed"""
    hero_mod_error = get_hero_mods()
    global_mod = get_global_mod()
    if hero_mod_error is False or global_mod is False:
        # Checks if there was an input error
        return
    btn = event.widget
    talent_name = btn.cget("text")
    # Updates last roll
    lastRoll.config(text="Letzte Probe: {}".format(talent_name))
    for u, hero_in_func in enumerate(dsa.heroes):
        # Calls dice_roll for all heroes that are enabled
        if hero_in_func.enabled is False:
            results[u].config(text="Nicht teilgenommen")
            continue
        outcome_dic = hero_in_func.roll_dices(talent_name, global_mod)
        print_result(u, outcome_dic)
    update_statistics()


def get_global_mod():
    """reads in the global mod the gui entry"""
    try:
        global_mod = int(globalModEntry.get())
    except ValueError:
        if globalModEntry.get() == "":
            global_mod = 0
        else:
            globalModErrorLabel.config(text="Falsche eingabe in Globaler Modifikator")
            return False
    globalModErrorLabel.config(text="")
    return global_mod


def get_hero_mods():
    """reads in the perm and temp mod form gui entry and updates the values inside the Hero instance"""
    one_error = False
    for u, hero_in_func in enumerate(dsa.heroes):
        error_text = "Falsche eingabe in "
        error_counter = 0
        try:
            hero_in_func.modification_perm = int(mods1[u].get())
        except ValueError:
            if mods1[u].get() == "":
                hero_in_func.modification_perm = 0
            else:
                error_text += "Permanenter"  # Nr. {}".format(u + 1)
                error_counter += 1
                one_error = True
        try:
            hero_in_func.modification_temp = int(mods2[u].get())
        except ValueError:
            if mods2[u].get() == "":
                hero_in_func.modification_temp = 0
            else:
                if error_counter > 0:
                    error_text += " und "
                error_text += "Temporärer Modifikator [{}]".format(hero_in_func.name)
                error_counter += 1
                one_error = True
        if error_text == "Falsche eingabe in Permanenter":
            error_text += " Modifikator [{}]".format(hero_in_func.name)
        if error_counter > 0:
            results[u].config(text=error_text)
        else:
            results[u].config(text="")
    if one_error:
        return False
    return True


root = Tk()

# Titles
root.title("DSA Würfel Helfer")
nameTitle = Label(root, text="Name")
mod1Title = Label(root, text="Permanenter Modifikator")
mod2Title = Label(root, text="Temporärer Modifikator")
nameTitle.grid(row=0, column=0)
mod1Title.grid(row=0, column=1)
mod2Title.grid(row=0, column=2)

# Create Hero site of the gui
names = []  # List of all name labels
mods1 = []  # List of all perm mod entries
mods2 = []  # List of all temp mod entries
results = []  # List of all result labels
i = 1  # Row number the next widget is placed
j = 0  # Position the current widgets have inside the list
for hero in dsa.heroes:
    # Create as many hero widgets as there are heroes
    hero.enabled = False  # Changes the "enabled" value form the default to False
    names.append(Checkbutton(root, text=hero.name))
    mods1.append(Entry(root))
    mods2.append(Entry(root))
    results.append(Label(root, text=""))
    names[j].bind("<Button-1>", check_heroes_enabled)
    names[j].grid(row=i, column=0, sticky=W)
    mods1[j].grid(row=i, column=1)
    mods2[j].grid(row=i, column=2)
    i += 1
    results[j].grid(row=i, columnspan=3, sticky=W)
    i += 1
    j += 1

lastRoll = Label(root, text="Letzte Probe: ")  # Label to display the name of the talent the last roll was for
lastRoll.grid(row=i, columnspan=3, sticky=W)
i += 1
globalModLabel = Label(root, text="Globaler Modifikator:")  # Global mod entry
globalModLabel.grid(row=i, column=0, sticky=W)
globalModEntry = Entry(root)
globalModEntry.grid(row=i, column=1)
i += 1
globalModErrorLabel = Label(root, text="")
globalModErrorLabel.grid(row=i, column=0, columnspan=3, sticky=W)
i += 1

# Shows stats below the hero section
successLabel = Label(root, text="Anzahl Erfolge: 0")
successLabel.grid(row=i, column=0, columnspan=3, sticky=W)
i += 1
criticalSuccessLabel = Label(root, text="Anzahl kritischer Erfolge: 0")
criticalSuccessLabel.grid(row=i, column=0, columnspan=3, sticky=W)
i += 1
reallyCriticalSuccessLabel = Label(root, text="Anzahl besonders kritischer Erfolge: 0")
reallyCriticalSuccessLabel.grid(row=i, column=0, columnspan=3, sticky=W)
i += 1
failureLabel = Label(root, text="Anzahl Misserfolge: 0")
failureLabel.grid(row=i, column=0, columnspan=3, sticky=W)
i += 1
criticalFailureLabel = Label(root, text="Anzahl kritischer Misserfolge: 0")
criticalFailureLabel.grid(row=i, column=0, columnspan=3, sticky=W)
i += 1
reallyCriticalFailureLabel = Label(root, text="Anzahl besonders kritischer Misserfolge: 0")
reallyCriticalFailureLabel.grid(row=i, column=0, columnspan=3, sticky=W)

# Create talent side of gui
talentButtons = []  # List of all talent buttons
groupLabels = []  # List of all talent group labels
i = 0  # Position in talentButton list
j = 0  # Position in groupLabels list
x = 3  # column number
y = 0  # row number

groupLabels.append(Label(root, text="Körpertalente:"))
groupLabels[i].grid(row=y, column=x, sticky=W)
y += 1
i += 1
for talent in dsa.german_talents.keys():
    if j == 15:
        groupLabels.append(Label(root, text="Gesellschaftstalente:"))
        groupLabels[i].grid(row=y, column=x, sticky=W)
        y += 1
        i += 1
    elif j == 24:
        x += 1
        y = 0
        groupLabels.append(Label(root, text="Naturtalente:"))
        groupLabels[i].grid(row=y, column=x, sticky=W)
        y += 1
        i += 1
    elif j == 31:
        groupLabels.append(Label(root, text="Wissenstalente:"))
        groupLabels[i].grid(row=y, column=x, sticky=W)
        y += 1
        i += 1
    elif j == 43:
        x += 1
        y = 0
        groupLabels.append(Label(root, text="Handwerkstalente:"))
        groupLabels[i].grid(row=y, column=x, sticky=W)
        y += 1
        i += 1

    talentButtons.append(Button(root, text=talent))
    talentButtons[j].bind("<Button-1>", talent_press)
    talentButtons[j].grid(row=y, column=x, sticky=W)
    y += 1
    j += 1

root.mainloop()
