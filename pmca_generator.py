import re
import os


class pmca_generate_defs:
    input_file_name = "input.txt"
    output_file_post_insert_name = "PMCA_GEN_OUTPUT/00_pmca_post_insert_defs.txt"
    output_file_x10_name = "PMCA_GEN_OUTPUT/01_pmca_ten_defs.txt"
    output_file_x100_name = "PMCA_GEN_OUTPUT/02_pmca_hundred_defs.txt"
    output_file_placeholder_loc_keys_name = (
        "PMCA_GEN_OUTPUT/03_pmca_loc_keys_placeholders.txt"
    )
    output_file_loc_keys_name = "PMCA_GEN_OUTPUT/04_pmca_loc_keys_complete.txt"

    in_resource_table = False
    in_cost_table = False
    current_resource_name = "food"
    current_resource_value = 0
    resource_priority_dict = {
        "food": 0,  # No use outside of colony ships
        "energy": 1,  # Usually used for upkeep, not cost
        "unity": 2,  # Again, not seen much but decently useful
        "minerals": 3,  # Default resource for most armies
        "consumer_goods": 4,  # Same as food, but also for upkeep
        "alloys": 6,  # Used for a lot, so hard to keep a massive stockpile
        "exotic_gases": 7,  # Not much income of these, so pretty good for clutter reducing
        "rare_crystals": 7,
        "volatile_motes": 7,
        "sr_zro": 8,
        "sr_living_metal": 8,
        "sr_nanites": 8,
        "sr_dark_matter": 8,  # Mainly for ACOT and similar
        "acot_sr_dark_energy": 8,  # ACOT specific
        "minor_artifacts": 10,  # Pretty rare
        "influence": 10,  # Capped at 1k for the most part, so pretty rare
        "acot_sr_stellarite": 11,  # Rare ACOT specific
    }

    pmca_scripted_trigger_block = ""
    seen_potential_country_block = False

    brace_count_updated = False
    num_isolated_braces = 0

    army_def_name = "PLACEHOLDER_ARMY_PLEASE_REPLACE_ME"
    seen_use_armynames_from = False

    army_def_list = []

    # Change a variable whenever we see a brace
    def update_brace_count(self, input_line, reset_seen_blocks):
        if reset_seen_blocks == False and "{" in input_line:
            self.num_isolated_braces += 1
        if reset_seen_blocks == False and "}" in input_line:
            self.num_isolated_braces -= 1
            self.in_cost_table = False
        if self.num_isolated_braces == 1:
            self.in_resource_table = False
        if reset_seen_blocks == True and self.num_isolated_braces == 0:
            self.seen_use_armynames_from = False
            self.seen_potential_country_block = False
            self.current_resource_name = "food"
            self.current_resource_value = 0

    # Save the army def for later if needed, and prepend pmca_ten_ to the line
    def fetch_army_def_and_prepend(self, input_line):
        appended_string = input_line
        if (
            self.num_isolated_braces == 1
            and "= {" in input_line
            and not "}" in input_line
        ):
            self.army_def_name = re.match(r"\w+", input_line).group(0)
            self.army_def_list.append(self.army_def_name)
            appended_string = "pmca_ten_" + input_line

        return appended_string

    # Return a string for output when given a line, meant for inserting the pmca_materiel_policy_check scripted_trigger
    def insert_materiel_policy_check(self, input_line):
        if "potential_country = {" in input_line:
            self.seen_potential_country_block = True
            if "}" in input_line:
                return -1
            else:
                return 1

        return 0

    # Try to update the cost of an army for later
    def update_army_costs(self, input_line):
        clean_string = re.sub("\t", "", input_line)
        if (
            self.resource_priority_dict[re.match(r"[^ ]*", clean_string).group(0)]
            > self.resource_priority_dict[self.current_resource_name]
        ):
            self.current_resource_name = re.match(r"[^ ]*", clean_string).group(0)
            self.current_resource_value = self.convert_list(
                re.findall(r"\d+(?:\.\d+)?", input_line), False
            )

    # Convert input_list into a float then return it as a string
    def convert_list(self, input_list, multiply):
        output = float(input_list[0])
        if multiply:
            output *= 10
        return str(output)

    # Should the script read this line?
    def should_read_line(self, input_line):
        if input_line.strip() and input_line.strip()[0] == "#":
            return False
        if "PMCA_GEN: IGNORE" in input_line:
            return False
        return True

    def insert_pmca_army_defs(self):
        with open(self.input_file_name, "r") as file_input, open(
            self.output_file_post_insert_name, "w"
        ) as file_output:
            for line in file_input:
                string_to_output = line
                self.update_brace_count(line, False)
                if self.should_read_line(string_to_output):
                    string_to_output = self.fetch_army_def_and_prepend(line)

                    if "resources = {" in line:
                        self.in_resource_table = True
                    if (
                        "cost = {" in line
                        and "}" not in line
                        and self.in_resource_table
                    ):
                        self.in_cost_table = True

                    if self.in_cost_table and bool(re.search(r"\d", line)):
                        self.update_army_costs(line)
                        self.pmca_scripted_trigger_block = (
                            "        pmca_materiel_policy_check = {\n            PMCA_MULT = ten\n            PMCA_RESOURCE = "
                            + self.current_resource_name
                            + "\n            PMCA_VALUE = "
                            + str(self.current_resource_value)
                            + "\n        }\n"
                        )

                    # Insert scripted trigger if potential_country exists, create if it doesn't
                    match (self.insert_materiel_policy_check(string_to_output)):
                        case 1:
                            file_output.write(string_to_output)
                            string_to_output = ""
                            file_output.write(self.pmca_scripted_trigger_block + "\n")
                        case -1:
                            string_to_output = ""
                            nested_string = re.search(r"\{ (.*?) \}\n", line).group(0)
                            nested_string = nested_string[2:-2]
                            file_output.write(
                                "    potential_country = { # PMCA_GEN: Modified trigger, probably was a nested 1-line statement\n"
                            )
                            file_output.write(self.pmca_scripted_trigger_block + "\n")
                            file_output.write("        " + nested_string + "\n")
                            file_output.write("    }\n")
                        case 0:
                            pass
                    if (
                        self.num_isolated_braces == 0
                        and self.seen_potential_country_block == False
                        and "}" in string_to_output
                    ):
                        file_output.write(
                            "    potential_country = { # PMCA_GEN: No potential_country detected, inserted template\n"
                        )
                        file_output.write(self.pmca_scripted_trigger_block)
                        file_output.write("    }\n")

                    # Create use_armynames_from if it doesn't exist
                    if "use_armynames_from" in line:
                        self.seen_use_armynames_from = True
                    if (
                        self.num_isolated_braces == 0
                        and self.seen_use_armynames_from == False
                        and "}" in line
                    ):
                        file_output.write(
                            "    use_armynames_from = "
                            + self.army_def_name
                            + " # PMCA_GEN: No use_armynames_from detected, inserted best guess\n"
                        )

                self.update_brace_count(string_to_output, True)
                file_output.write(string_to_output)

    # Does input_line have a int/float?
    def has_number(self, input_line):
        return bool(re.search(r"\d", input_line))

    # What lines should the script multiply numbers in?
    def valid_lines_to_multiply(self, input_line):
        return bool(
            not "morale_damage" in input_line
            and (
                self.in_resource_table
                or "damage" in input_line
                or "health" in input_line
                or "morale" in input_line
                or "war_exhaustion" in input_line
                or "PMCA_VALUE" in input_line
                or "base" in input_line
            )
        )

    # Handle AI weight stuff
    def handle_ai_base(self, input_list, is_hundred):
        output = float(input_list[0])
        if is_hundred:
            return str(output * (2 / 3) * 2)
        else:
            return str(output * 1.5)

    # Get the number in a string and send it to another function for multiplying
    def factor_number_in_string(self, input_line, is_hundred):
        output_string = input_line
        temp_list = re.findall(r"\d+(?:\.\d+)?", input_line)
        if "base" in input_line:
            output_string = re.sub(
                r"\d+(?:\.\d+)?",
                self.handle_ai_base(temp_list, is_hundred),
                output_string,
            )
        else:
            output_string = re.sub(
                r"\d+(?:\.\d+)?", self.convert_list(temp_list, True), output_string
            )

        return output_string

    def multiply_values_by_ten(self):
        with open(self.output_file_post_insert_name, "r") as file_input, open(
            self.output_file_x10_name, "w"
        ) as file_output:
            for line in file_input:
                string_to_output = line
                self.update_brace_count(line, False)
                if self.should_read_line(string_to_output):
                    if "resources = {" in line:
                        self.in_resource_table = True
                    if self.valid_lines_to_multiply(string_to_output) and self.has_number(
                        string_to_output
                    ):
                        string_to_output = self.factor_number_in_string(
                            string_to_output, False
                        )
                self.update_brace_count(string_to_output, True)
                file_output.write(string_to_output)

    def multiply_values_by_hundred(self):
        with open(self.output_file_x10_name, "r") as file_input, open(
            self.output_file_x100_name, "w"
        ) as file_output:
            for line in file_input:
                string_to_output = line
                self.update_brace_count(line, False)
                if self.should_read_line(string_to_output):
                    if "resources = {" in line:
                        self.in_resource_table = True
                    if self.valid_lines_to_multiply(string_to_output) and self.has_number(
                        string_to_output
                    ):
                        string_to_output = self.factor_number_in_string(
                            string_to_output, True
                        )
                    if "PMCA_MULT = ten" in string_to_output:
                        string_to_output = re.sub(
                            "PMCA_MULT = ten", "PMCA_MULT = hundred", string_to_output
                        )
                    if "pmca_ten_" in string_to_output:
                        string_to_output = re.sub(
                            "pmca_ten_", "pmca_hundred_", string_to_output
                        )
                self.update_brace_count(string_to_output, True)
                file_output.write(string_to_output)

    def generate_placeholder_loc_keys(self):
        with open(self.output_file_placeholder_loc_keys_name, "w") as file_output:
            if len(self.army_def_list) > 0:
                for key in self.army_def_list:
                    file_output.write("pmca_ten_" + key + ': "REPLACE_ME"\n')
                    file_output.write("pmca_ten_" + key + '_plural: "REPLACE_ME"\n')
                    file_output.write("pmca_ten_" + key + '_desc: "REPLACE_ME"\n')
                for key in self.army_def_list:
                    file_output.write("pmca_hundred_" + key + ': "REPLACE_ME"\n')
                    file_output.write("pmca_hundred_" + key + '_plural: "REPLACE_ME"\n')
                    file_output.write("pmca_hundred_" + key + '_desc: "REPLACE_ME"\n')

    pmcaTen = "$pmca_ten$ "
    pmcaHundred = "$pmca_hundred$ "

    def combineStrings(self, prefix, input_list):
        return str('"' + prefix + "$" + input_list[0] + "$" + '"')

    def complete_loc_keys(self):
        with open(self.output_file_placeholder_loc_keys_name, "r") as file_input, open(
            self.output_file_loc_keys_name, "w"
        ) as file_output:
            count = 0
            for line in file_input:
                output_line = line
                count += 1
                if count % 3 == 1:  # Army Name Singular
                    if "pmca_ten_" in output_line:
                        file_output.write(
                            re.sub(
                                '"REPLACE_ME"',
                                self.combineStrings(
                                    self.pmcaTen,
                                    re.findall(r"(?:pmca_ten_)([^:]*)", output_line),
                                ),
                                output_line,
                            )
                        )
                    else:
                        file_output.write(
                            re.sub(
                                '"REPLACE_ME"',
                                self.combineStrings(
                                    self.pmcaHundred,
                                    re.findall(
                                        r"(?:pmca_hundred_)([^:]*)", output_line
                                    ),
                                ),
                                output_line,
                            )
                        )

                elif count % 3 == 2:  # Army Name Plural
                    file_output.write(
                        re.sub(
                            '"REPLACE_ME"',
                            self.combineStrings(
                                "",
                                re.findall(
                                    r"(?:pmca_ten_|pmca_hundred_)([^:]*)", output_line
                                ),
                            ),
                            output_line,
                        )
                    )

                else:  # Army Description
                    file_output.write(
                        re.sub(
                            '"REPLACE_ME"',
                            self.combineStrings(
                                "",
                                re.findall(
                                    r"(?:pmca_ten_|pmca_hundred_)([^:]*)", output_line
                                ),
                            ),
                            output_line,
                        )
                    )


if os.path.isfile("./input.txt"):
    directory = "PMCA_GEN_OUTPUT"
    path = os.path.join(os.getcwd(), directory)
    print("Trying to create Directory '%s'..." % directory)
    try:
        os.mkdir(path)
        print("Directory '%s' does NOT exist, creating..." % directory)
    except OSError as error:
        print("Directory '%s' exists, continuing..." % directory)

    pmca_automater = pmca_generate_defs()

    print("Inserting required army properties...")
    pmca_automater.insert_pmca_army_defs()

    print("Multiplying values to x10...")
    pmca_automater.multiply_values_by_ten()

    print("Multiplying values to x100...")
    pmca_automater.multiply_values_by_hundred()

    print("Generating placeholder localisation keys...")
    pmca_automater.generate_placeholder_loc_keys()

    print("Replacing placeholder lines with preferred text and format...")
    pmca_automater.complete_loc_keys()

    print(
        "Done! Check the Directory '%s' for your freshly Condensed Armies!" % directory
    )
else:
    print(
        "ERROR: input.txt does NOT exist! Please create it and put your army definitions inside it."
    )
