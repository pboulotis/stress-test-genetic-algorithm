import sys
import random
import matplotlib.pyplot as plt

element_list = []
signal_list = []
input_list = []
output_list = []
acceptable_gates = ["NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR"]
file_data = []
gaps_flag = False


class Element:
    def __init__(self):
        self.gate = ""
        self.inputs = []
        self.output = None


def print_element(element):
    if len(element.inputs) > 1:
        inp_list = []
        for i in range(len(element.inputs)):
            inp_list.append(element.inputs[i].name)

        print(element.gate + " gate, inputs: " + str(inp_list) + " output: " + str(element.output.name))
    else:
        print("NOT gate, input: " + str(element.inputs[0].name) + " output: " + str(element.output.name))


class Signal:
    def __init__(self, name):
        self.name = name
        self.value = 2
        signal_list.append(self)


def print_signal(signal):
    print("Signal: " + str(signal.name) + ", value: " + str(signal.value))


def search_signal(name):
    for i in range(len(signal_list)):
        if name == signal_list[i].name:
            return signal_list[i]


def print_all():
    for i in range(len(element_list)):
        print("Element " + str(i+1) + ":")
        print_element(element_list[i])
        print("Input(s): ")
        for j in range(len(element_list[i].inputs)):
            print_signal(element_list[i].inputs[j])
        print("Output:")
        print_signal(element_list[i].output)
        print("--------------------------------------------")


def and_gate(inp):
    for i in range(len(inp)):
        if inp[i].value == 0:
            return 0
        elif (inp[i].value != 0) and (inp[i].value != 1):
            print("Non bit value given to " + inp[i].name + " (" + str(inp[i].value) + ")")
            sys.exit()
    return 1


def nand_gate(inp):
    temp = and_gate(inp)
    if temp == 0:
        return 1
    else:
        return 0


def not_gate(inp):
    if inp[0].value == 0:
        return 1
    elif (inp[0].value != 0) and (inp[0].value != 1):
        print("Non bit value given to " + inp[0].name + " (" + str(inp[0].value) + ")")
        sys.exit()
    else:
        return 0


def or_gate(inp):
    for i in range(len(inp)):
        if inp[i].value == 0:
            return 1
        elif (inp[i].value != 0) and (inp[i].value != 1):
            print("Non bit value given to " + inp[i].name + " (" + str(inp[i].value) + ")")
            sys.exit()
    return 0


def nor_gate(inp):
    temp = or_gate(inp)
    if temp == 0:
        return 1
    else:
        return 0


def xor_gate(inp):
    temp = 0
    for i in range(len(inp)):
        if inp[i].value == 1:
            if temp == 0:
                temp = 1
            elif temp == 1:
                temp = 0
            else:
                print("How did this happen? " + str(temp))
        elif (inp[i].value != 0) and (inp[i].value != 1):
            print("Non bit value given to " + inp[i].name + " (" + str(inp[i].value) + ")")
            sys.exit()

    return temp


def xnor_gate(inp):
    temp = xor_gate(inp)
    if temp == 0:
        return 1
    else:
        return 0


def process_element_values(element):
    global gaps_flag
    # We need to check if any of the inputs have not been set
    for i in range(len(element.inputs)):
        if element.inputs[i].value == 2:
            gaps_flag = True
            return

    if element.gate == "AND":
        element.output.value = and_gate(element.inputs)
    elif element.gate == "NAND":
        element.output.value = nand_gate(element.inputs)
    elif element.gate == "OR":
        element.output.value = or_gate(element.inputs)
    elif element.gate == "NOR":
        element.output.value = nor_gate(element.inputs)
    elif element.gate == "NOT":
        element.output.value = not_gate(element.inputs)
    elif element.gate == "XOR":
        element.output.value = xor_gate(element.inputs)
    elif element.gate == "XNOR":
        element.output.value = xnor_gate(element.inputs)
    else:
        print("Invalid type of logic gate:" + str(element.gate))
        sys.exit()


def file_handling(file_input):
    tlp_enabled = False
    temp_file_data = file_input.readlines()
    for i in range(len(temp_file_data)):
        temp_file_data[i] = temp_file_data[i].strip('\n')
        file_data.append((temp_file_data[i].split()))

    if file_data[0][0] == "Top_inputs":
        tlp_enabled = True
        for i in range(1, len(file_data[0])):
            input_list.append(file_data[0][i])
            Signal(file_data[0][i])
        del file_data[0]

    for i in range(len(file_data)):
        if file_data[i][1] not in output_list:
            output_list.append(file_data[i][1])
            Signal(file_data[i][1])

    if not tlp_enabled:
        for i in range(len(file_data)):
            for j in range(2, len(file_data[i])):
                if file_data[i][j] not in output_list and file_data[i][j] not in input_list:
                    input_list.append(file_data[i][j])
                    Signal(file_data[i][j])


def set_values():
    for i in range(len(input_list)):
        signal = search_signal(input_list[i])
        signal.value = random.randint(0, 1)


def create_elements():
    for i in range(len(file_data)):
        element = Element()
        element.gate = file_data[i][0]
        for j in range(2, len(file_data[i])):
            element.inputs.append(search_signal(file_data[i][j]))
        element.output = search_signal(file_data[i][1])
        element_list.append(element)


def compute_output():
    global gaps_flag
    for i in range(len(element_list)):
        element = element_list[i]
        process_element_values(element)

    # fill in the outputs that don't have a value
    while gaps_flag:
        fill_gaps()


def fill_gaps():
    global gaps_flag
    gaps_flag = False
    for i in range(len(element_list)):
        temp_element = element_list[i]
        process_element_values(temp_element)


# Computes the new output values if the input values are changed
def stress_test():
    input_values = []
    output_values = []

    # Set values to inputs
    set_values()
    compute_output()
    for k in range(len(signal_list)):
        if signal_list[k].name in input_list:
            input_values.append(signal_list[k].value)
        else:
            output_values.append(signal_list[k].value)

    return output_values


if __name__ == '__main__':
    file = open(sys.argv[1], 'r')
    file_handling(file)
    create_elements()
    score = []
    max_iterations = int(input("How many iterations? "))

    for n in range(max_iterations):
        switches_number = 0
        signals_before = stress_test()
        signals = stress_test()
        for c in range(len(signals)):
            if signals[c] != signals_before[c]:
                switches_number += 1

        score.append(switches_number)
        print("Iteration " + str(n+1) + " Score: " + str(score[n]))

    plt.plot(score)
    plt.title("Score")
    plt.xlabel("Individual")
    plt.ylabel("Number of switches")
    plt.show()
