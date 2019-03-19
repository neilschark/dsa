import pygal

def visualize(number_of_tests, results):
    # Visualize the results.
    hist = pygal.Bar()

    hist.title = "Results of {} tests".format(number_of_tests)
    hist.x_labels = ["BESONDERS KRITISCHER ERFOLG", "KRITISCHER ERFOLG",
                     "ERFOLG", "MISSERFOLG",
                     "KRITISCHER MISSERFOLG", "BESONDERS KRITISCHER MISSERFOLG"]
    hist.x_title = "Result"
    hist.y_labels = "Frequency of Result"

    hist.add("results", results)
    hist.render_to_file("test_visual.svg")

