import re

pmcaTen = "$pmca_ten$ "
pmcaHundred = "$pmca_hundred$ "


def combineStrings(prefix, input_list):
    return str('"' + prefix + "$" + input_list[0] + "$"+ '"')


with open("input.txt", "r") as file_input, open("output.txt", "w") as file_output:
    count = 0
    for line in file_input:
        output_line = line
        count += 1
        if (count % 3 == 1): # Army Name Singular
            if ("pmca_ten_" in output_line):
                file_output.write(re.sub('"REPLACE_ME"', combineStrings(pmcaTen, re.findall(r'(?:pmca_ten_)([^:]*)', output_line)), output_line))
            else:
                file_output.write(re.sub('"REPLACE_ME"', combineStrings(pmcaHundred, re.findall(r'(?:pmca_hundred_)([^:]*)', output_line)), output_line))
        
        elif (count % 3 == 2): # Army Name Plural
            file_output.write(re.sub('"REPLACE_ME"', combineStrings("", re.findall(r'(?:pmca_ten_|pmca_hundred_)([^:]*)', output_line)), output_line))
        
        else: # Army Description
            file_output.write(re.sub('"REPLACE_ME"', combineStrings("", re.findall(r'(?:pmca_ten_|pmca_hundred_)([^:]*)', output_line)), output_line))