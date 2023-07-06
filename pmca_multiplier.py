import re


class pmca_multiplyOp:

    # Constructor Args
    input_file_name = "input.txt"
    output_file_name = "output.txt"
    isHundred = False

    # Non-Constructor Args
    factor = 10
    reductionFraction = 2/3
    inPrereq = False
    inResourceTable = False
    resourceIsolatedBraces = 0

    # Constructor
    def __init__(self, input_file_name, output_file_name, isHundred):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.isHundred = isHundred

    # Check if inputString is inside the prerequisites table
    def updatePrereq(self, armyDefPrereqLine, prereqMultiLineBool):
        if ("prerequisites" in armyDefPrereqLine):
            self.inPrereq = True
        if (self.inPrereq and "}" in armyDefPrereqLine and prereqMultiLineBool):
            self.inPrereq = False

    # Check if inputString is in the resources table. If resourceIsolatedBraces == 0, we must be outside the resource table
    def updateResourceTable(self, armyDefResourceLine):
        if ("resources" in armyDefResourceLine and not self.inPrereq):
            self.inResourceTable = True
        if (self.inResourceTable and "{" in armyDefResourceLine):
            self.resourceIsolatedBraces += 1
        if (self.inResourceTable and "}" in armyDefResourceLine):
            self.resourceIsolatedBraces -= 1
        if (self.resourceIsolatedBraces == 0):
            self.inResourceTable = False

    # Does inputString have a int/float?
    def has_number(self, line):
        return bool(re.search(r'\d', line))

    # Does inputString contain any of the following?
    def containsValid(self, line):
        return bool(self.inResourceTable or "damage" in line or "health" in line or "morale" in line or "war_exhaustion" in line or "PMCA_VALUE" in line or "base" in line)

    # Convert inputList into a float, multiply it, then return it as a string
    def convertList(self, findallList):
        output = float(findallList[0]) * self.factor
        return str(output)

    # Handle AI weight stuff
    def handleBase(self, findallList):
        output = float(findallList[0])
        if (self.isHundred):
            return str((output*self.reductionFraction)*2)
        else:
            return str(output*1.5)

    # Replace the number in inputString
    def replaceNumber(self, line):
        outputString = line
        if (self.containsValid(outputString) and self.has_number(outputString)):
            replacementList = re.findall(r'\d+(?:\.\d+)?', outputString)
            if (not "base" in outputString):
                outputString = re.sub( r'\d+(?:\.\d+)?', self.convertList(replacementList), outputString)
            else:
                outputString = re.sub(r'\d+(?:\.\d+)?', self.handleBase(replacementList), outputString)
        if (self.isHundred):
            outputString = re.sub("PMCA_MULT = ten", "PMCA_MULT = hundred", outputString)
        return outputString

    # Main function, calls everything else
    def readAndWrite(self):
        with open(self.input_file_name, "r") as file_input, open(self.output_file_name, "w") as file_output:
            for line in file_input:
                outputLine = line
                self.updatePrereq(outputLine, False)
                self.updateResourceTable(outputLine)
                if (not self.inPrereq and not "morale_damage" in outputLine):
                    outputLine = self.replaceNumber(outputLine)
                self.updatePrereq(outputLine, True)
                if (self.isHundred and "pmca_ten_" in outputLine and "= {" in outputLine):
                    outputLine = re.sub("pmca_ten_", "pmca_hundred_", outputLine)
                file_output.write(outputLine)