import re

pmcaTen = "$pmca_ten$"
pmcaHundred = "$pmca_hundred$"


def combineStrings(input1, inputList):
    return str(input1 + " $" + inputList[0] + "$")


with open("input.txt", "r") as file_input, open("output.txt", "w") as file_output:
    count = 0
    for line in file_input:
        placeholderString = line
        if (bool(line)):
            count += 1
            if (count % 2 == 1):  # Odds, army names
                if ("pmca_hundred" in line):
                    armyNameOrDesc = re.findall(r'(?:pmca_hundred_)([^;]*):', line)
                    placeholderString = re.sub(r'("")', combineStrings(pmcaHundred, armyNameOrDesc), line)
                else:
                    armyNameOrDesc = re.findall(r'(?:pmca_ten_)([^;]*):', line)
                    placeholderString = re.sub(r'("")', combineStrings(pmcaTen, armyNameOrDesc), line)
            else:  # Evens, army descriptions
                if ("pmca_hundred" in line):
                    armyNameOrDesc = re.findall(r'(?:pmca_hundred_)([^;]*):', line)
                    placeholderString = re.sub(r'("")', combineStrings("", armyNameOrDesc), line)
                else:
                    #print(re.findall(r'(?:pmca_ten_)([^;]*):', line))
                    armyNameOrDesc = re.findall(r'(?:pmca_ten_)([^;]*):', line)
                    placeholderString = re.sub(r'("")', combineStrings("", armyNameOrDesc), line)
        file_output.write(placeholderString)
