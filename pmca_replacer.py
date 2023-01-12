import re


class pmca_multiplier:

    input_file_name = "input.txt"
    output_file_name = "output.txt"
    modPrefix = "acot_"
    isHundred = False

    factor = 10
    reductionFraction = 2/3
    braceCountUpdated = False
    numOpenBracesInArmyDef = 0
    numClosedBracesInArmyDef = 0

    inPrereq = False
    inResourceTable = False
    resourceOpenBrace = 0
    resourceCloseBrace = 0

    def __init__(self, isHundred, input_file_name, output_file_name, modPrefix):
        self.isHundred = isHundred
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.modPrefix = modPrefix

    def has_number(self, inputString):
        return bool(re.search(r'\d', inputString))

    def containsValid(self, inputString):
        return bool(self.inResourceTable or "damage" in inputString or "health" in inputString or "morale" in inputString or "war_exhaustion" in inputString or "PMCA_VALUE" in inputString)

    def updateNumBraces(self, inputString):
        if ("{" in inputString):
            self.numOpenBracesInArmyDef += 1
            self.braceCountUpdated = True
        if ("}" in inputString):
            self.numClosedBracesInArmyDef += 1
        if (self.numOpenBracesInArmyDef == self.numClosedBracesInArmyDef):
            self.numOpenBracesInArmyDef = 0
            self.numClosedBracesInArmyDef = 0
            self.braceCountUpdated = False

    def updatePrefix(self, inputString):
        outputString = inputString
        if (not self.inPrereq and self.modPrefix in inputString and self.numOpenBracesInArmyDef == 1 and not "pmca_ten_" in inputString and not "icon" in inputString):
            outputString = "pmca_ten_" + outputString
        if (self.isHundred):
            outputString = re.sub("pmca_ten_", "pmca_hundred_", outputString)
        return outputString

    def updatePrereq(self, inputString):
        if ("prerequisites" in inputString):
            self.inPrereq = True
    
    def updatePrereqOneLine(self, inputString):
        if (self.inPrereq and "}" in inputString):
            self.inPrereq = False

    def updateResourceTable(self, inputString):
        if ("resources" in inputString and not self.inPrereq):
            self.inResourceTable = True
        if (self.inResourceTable and "{" in inputString):
            self.resourceOpenBrace += 1
        if (self.inResourceTable and "}" in inputString):
            self.resourceCloseBrace += 1
        if (self.resourceOpenBrace == self.resourceCloseBrace):
            self.inResourceTable = False
            self.resourceOpenBrace = 0
            self.resourceCloseBrace = 0

    def convertList(self, inputList):
        output = float(inputList[0]) * self.factor
        return str(output)

    def handleBase(self, inputList):
        output = float(inputList[0])
        if (self.isHundred):
            return str((output*self.reductionFraction)*2)
        else:
            return str(output*1.5)

    def replaceNumber(self, inputString):
        outputString = inputString
        if (self.containsValid(outputString) and self.has_number(outputString)):
            replacementList = re.findall(r'\d+(?:\.\d+)?', outputString)
            if ("base" in outputString):
                outputString = re.sub(r'\d+(?:\.\d+)?', self.handleBase(replacementList), outputString)
            else:
                outputString = re.sub( r'\d+(?:\.\d+)?', self.convertList(replacementList), outputString)
        if (self.isHundred):
            outputString = re.sub("PMCA_MULT = ten", "PMCA_MULT = hundred", outputString)
        return outputString

    def readAndWrite(self):
        with open(self.input_file_name, "r") as file_input, open(self.output_file_name, "w") as file_output:
            for line in file_input:
                dummyString = line
                self.updateNumBraces(dummyString)
                self.updatePrereq(dummyString)
                self.updateResourceTable(dummyString)
                if (not self.inPrereq and not "morale_damage" in dummyString):
                    dummyString = self.replaceNumber(dummyString)
                dummyString = self.updatePrefix(dummyString)
                self.updatePrereqOneLine(dummyString)
                file_output.write(dummyString)

Tester = pmca_multiplier(True, "input.txt", "output.txt", "acot_")
Tester.readAndWrite()