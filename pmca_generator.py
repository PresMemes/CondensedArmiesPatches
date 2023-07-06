import re


class pmca_generate_defs:
    # Constructor Args
    input_file_name = "input.txt"

    # Non-Constructor Args
    output_file_post_insert_name = "pmca_post_insert_defs.txt"
    output_file_x10_name = "pmca_ten_defs.txt"
    output_file_x100_name = "pmca_hundred_defs.txt"

    in_resource_table = False
    in_cost_table = False
    current_resource_name = "food"
    current_resource_value = 0
    resource_priority_dict = {
        "food": 0,  # No use outside of colony ships
        "energy": 1,  # Usually used for upkeep, not cost
        "minerals": 2,  # Default resource for most armies
        "consumer_goods": 3,  # Same as food, but also for upkeep
        "unity": 4,  # Again, not seen much but decently useful
        "exotic_gases": 5,  # The next 6 aren't used much outside of weaponry or upkeep
        "rare_crystals": 5,
        "volatile_motes": 5,
        "sr_zro": 7,
        "sr_living_metal": 7,
        "sr_nanites": 7,
        "alloys": 10,  # Used for a lot, so hard to keep a massive stockpile
        "sr_dark_matter": 12,  # Mainly for ACOT and similar
        "sr_acot_dark_energy": 12,  # ACOT specific
        "influence": 13,  # Capped at 1k for the most part, so pretty rare
    }

    pmca_scripted_trigger_block = ""
    seen_potential_country_block = False

    brace_count_updated = False
    num_isolated_braces = 0

    army_def_name = "PLACEHOLDER_ARMY_PLEASE_REPLACE_ME"
    seen_use_armynames_from = False

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

    def insert_pmca_army_defs(self):
        with open(self.input_file_name, "r") as file_input, open(
            self.output_file_post_insert_name, "w"
        ) as file_output:
            for line in file_input:
                string_to_output = line
                self.update_brace_count(line, False)
                string_to_output = self.fetch_army_def_and_prepend(line)

                if "resources = {" in line:
                    self.in_resource_table = True
                if "cost = {" in line and "}" not in line and self.in_resource_table:
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
                if "use_army_names_from" in line:
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

    def factor_number_in_string(self, input_line, is_hundred):
        output_string = input_line
        temp_list = re.findall(r"\d+(?:\.\d+)?", input_line)
        if "base" in input_line:
            output_string = re.sub(
                r"\d+(?:\.\d+)?", self.handle_ai_base(temp_list, is_hundred), output_string
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
                if "resources = {" in line:
                    self.in_resource_table = True
                if self.valid_lines_to_multiply(string_to_output) and self.has_number(string_to_output):
                    string_to_output = self.factor_number_in_string(string_to_output, False)
                self.update_brace_count(string_to_output, True)
                file_output.write(string_to_output)
                
    def multiply_values_by_hundred(self):
        with open(self.output_file_x10_name, "r") as file_input, open(
            self.output_file_x100_name, "w"
        ) as file_output:
            for line in file_input:
                string_to_output = line
                self.update_brace_count(line, False)
                if "resources = {" in line:
                    self.in_resource_table = True
                if self.valid_lines_to_multiply(string_to_output) and self.has_number(string_to_output):
                    string_to_output = self.factor_number_in_string(string_to_output, True)
                if ("PMCA_MULT = ten" in string_to_output):
                    string_to_output = re.sub("PMCA_MULT = ten", "PMCA_MULT = hundred", string_to_output)
                if ("pmca_ten_" in string_to_output):
                    string_to_output = re.sub("pmca_ten_", "pmca_hundred_", string_to_output)
                self.update_brace_count(string_to_output, True)
                file_output.write(string_to_output)


pmca_automater = pmca_generate_defs()
pmca_automater.insert_pmca_army_defs()
pmca_automater.multiply_values_by_ten()
pmca_automater.multiply_values_by_hundred()
