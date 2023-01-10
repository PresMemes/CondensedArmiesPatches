import re

factor = 10  # Don't change (trust me)
reductionFraction = 2/3  # Also don't change

# if you're converting from vanilla/mod to x10, set to False.
# if you're converting from x10 to x100, set to True
isHundred = False


# Checks if a given string has any numbers in it
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


# Checks if a given string has any of the following substrings
def containsInvalid(inputString):
    return ("morale_damage" in inputString or "time" in inputString or "factor" in inputString or "prerequisites" in inputString or "armynames_from" in inputString or (not bool(inputString)) or " = {" in inputString)


# Converts a list of strings into a float
# Not sure if it can handle multiple numbers on one line
def convert(inputList):
    output = float(inputList[0]) * factor
    return str(output)


# Handle AI weight and/or other stuff that uses base
def handleBase(inputList):
    output = float(inputList[0])
    if (isHundred):
        return str((output*reductionFraction)*2)
    else:
        return str(output*1.5)


# Copy contents of one file, then puts them into a new file while modifiying them
with open("input.txt", "r") as file_input, open("output.txt", "w") as file_output:
    for line in file_input:
        dummyString = line
        if ((not containsInvalid(line)) and has_numbers(line)):
            # Converts every number in a line into a list of strings
            replacementList = re.findall(r'\d+(?:\.\d+)?', line)
            if ("base" in line):
                # Replace number in string with another string
                dummyString = re.sub(
                    r'\d+(?:\.\d+)?', handleBase(replacementList), line)
            else:
                dummyString = re.sub(
                    r'\d+(?:\.\d+)?', convert(replacementList), line)

        if (isHundred):
            # dummyString = re.sub(r"pmca_ten_\S* = {", "pmca_hundred_", line) # TODO: fix? not like it's hard to ctrl + h
            dummyString = re.sub(r"PMCA_MULT = ten",
                                 "PMCA_MULT = hundred", line)
        file_output.write(dummyString)
