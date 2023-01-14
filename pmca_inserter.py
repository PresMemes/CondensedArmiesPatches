import re


class pmca_insertOp:

    # Constructor Args
    input_file_name = "input.txt"
    output_file_name = "output.txt"
    modPrefix = "acot_"
    isHundred = False

    # Non-Constructor Args
    lineCount = 0
    inPrereq = False
    braceCountUpdated = False
    numIsolatedBraces = 0
    armyDefName = "some_name"
    seenUsesArmyNames = False


    # Constructor
    def __init__(self, input_file_name, output_file_name, isHundred, modPrefix):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.isHundred = isHundred
        self.modPrefix = modPrefix

    # Count the number of braces. If numIsolatedBraces == 0, we must be outside an army definition (i.e whitespace between armies)
    def updateNumBraces(self, line, insertBool):
        if (not insertBool):
            if ("{" in line):
                self.numIsolatedBraces += 1
            if ("}" in line):
                self.numIsolatedBraces -= 1
        if (insertBool and self.numIsolatedBraces == 0):
            self.seenUsesArmyNames = False

    # Checks for use_armynames_from and/or potential_country = { }
    def updateArmyDefChecks(self, line):
        if ("use_armynames_from" in line and not "#" in line):
            self.seenUsesArmyNames = True

    def insertArmyNameCheck(self, line):
        return bool(not self.seenUsesArmyNames and bool(re.search(r"[}]", line)) and not "#" in line and self.numIsolatedBraces == 0)

    # Check if inputString is inside the prerequisites table
    def updatePrereq(self, armyDefPrereqLine, prereqMultiLineBool):
        if ("prerequisites" in armyDefPrereqLine):
            self.inPrereq = True
        if (self.inPrereq and "}" in armyDefPrereqLine and prereqMultiLineBool):
            self.inPrereq = False

    # If modPrefix is in inputString, add pmca_ten_ to the front of the line (or replace it if x10 -> x100) also fetches the army name for later
    def updatePrefix(self, armyDefLine):
        outputString = armyDefLine
        if (not self.inPrereq and self.modPrefix in armyDefLine and self.numIsolatedBraces == 1 and not "pmca_ten_" in armyDefLine and not "icon" in armyDefLine):
            self.armyDefName = re.match(r"\w+", outputString).group(0)
            outputString = "pmca_ten_" + outputString
        if (self.isHundred):
            outputString = re.sub("pmca_ten_", "pmca_hundred_", outputString)
        return outputString

    # Main function
    def readAndWrite(self):
        with open(self.input_file_name, "r") as file_input, open(self.output_file_name, "w") as file_output:
            for line in file_input:
                outputLine = line
                self.updateNumBraces(outputLine, False)
                self.updateArmyDefChecks(outputLine)
                self.updatePrereq(outputLine, False)
                outputLine = self.updatePrefix(outputLine)
                self.updatePrereq(outputLine, True)
                if ("potential_country" in outputLine and not self.isHundred):
                    file_output.write(outputLine)
                    file_output.write("        pmca_materiel_policy_check = {\n")
                    file_output.write("            PMCA_MULT = ten\n")
                    file_output.write("            PMCA_RESOURCE = minerals\n")
                    file_output.write("            PMCA_VALUE = 100\n")
                    file_output.write("        }\n\n")
                    outputLine = ""
                if (self.insertArmyNameCheck(outputLine)):
                    concatArmyName = "    uses_armynames_from = " + self.armyDefName + "\n"
                    file_output.write(concatArmyName)
                    file_output.write(outputLine)
                    outputLine = ""
                self.updateNumBraces(outputLine, True)
                file_output.write(outputLine)
