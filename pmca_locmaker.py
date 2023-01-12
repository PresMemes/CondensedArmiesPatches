import re

pmcaTen = "$pmca_ten$"
pmcaHundred = "$pmca_hundred$"


def combineStrings(input1, inputList):
    return str('"' + input1 + " $" + inputList[0] + "$"+ '"')


with open("input.txt", "r") as file_input, open("output.txt", "w") as file_output:
    count = 0
    for line in file_input:
        placeholderString = line
        if (bool(placeholderString)):
            count += 1
            if (count % 2 == 1):  # Odds, army names
                if ("pmca_hundred" in line):
                    armyNameOrDesc = re.findall(r'(?:pmca_hundred_)([^;]*):', placeholderString)
                    placeholderString = re.sub('("REPLACE_ME")', combineStrings(pmcaHundred, armyNameOrDesc), placeholderString)
                else:
                    armyNameOrDesc = re.findall(r'(?:pmca_ten_)([^;]*):', placeholderString)
                    placeholderString = re.sub('("REPLACE_ME")', combineStrings(pmcaTen, armyNameOrDesc), placeholderString)
            else:  # Evens, army descriptions
                if ("pmca_hundred" in line):
                    armyNameOrDesc = re.findall(r'(?:pmca_hundred_)([^;]*):', placeholderString)
                    placeholderString = re.sub('("REPLACE_ME")', combineStrings("", armyNameOrDesc), placeholderString)
                else:
                    armyNameOrDesc = re.findall(r'(?:pmca_ten_)([^;]*):', placeholderString)
                    placeholderString = re.sub('("REPLACE_ME")', combineStrings("", armyNameOrDesc), placeholderString)
        file_output.write(" " + placeholderString)
