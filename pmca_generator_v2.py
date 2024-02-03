import re, time, os, shutil

stellaris_languages = [
    "braz_por",
    "english",
    "french",
    "german",
    "japanese",
    "korean",
    "polish",
    "russian",
    "simp_chinese",
    "spanish",
]

vanilla_army_keys = set(
    [
        "assault_army",
        "slave_army",
        "clone_army",
        "robotic_army",
        "psionic_army",
        "xenomorph_army",
        "gene_warrior_army",
        "machine_assault_1",
        "machine_assault_2",
        "machine_assault_3",
        "undead_army",
        "warpling_army",
        "flamestorm_troopers_army",
        "cybrex_warform",
    ]
)

# If a resource is not here, it's assumed to have a value of 7
resource_priority_dict = {
    "food": 0,
    "energy": 1,
    "unity": 2,
    "minerals": 3,
    "consumer_goods": 4,
    "alloys": 6,
    "minor_artifacts": 10,
    "influence": 10,
    "astral_threads": 9,
    "sr_iodizium": 8,
    "ehof_sr_negative_mass": 9,
    "ehof_sr_sentient_metal": 9,
    "giga_sr_amb_megaconstruction": 12,
    "acot_sr_stellarite": 10,
    "acot_sr_light_matter": 11,
}

list_of_armies = []
armies_with_issues = {
    "Unbuildable": [],
    "Variable Manipulation": [],
    "Odd Property": [],
}
scripted_variables = ()
scripted_variable_assignment_regex = re.compile(r"(@\S*)\s*=\s*(\S*)")
block_regex = re.compile(r"(\w+)\s*=\s*{")
complex_block_regex = re.compile(
    r"(prerequisites|resources|show_tech_unlock_if|potential|potential_country|allow|on_queued|on_unqueued|ai_weight|spawn_chance|army_modifier)\s*=\s*{"
)
field_value_pair_regex = re.compile(r"(\w+)\s*=\s*([-+]?\d+\.?\d*)")
field_bool_pair_regex = re.compile(r"(\w+)\s*=\s*(yes|no)")
icon_regex = re.compile(r"icon\s*=\s*(\w+)")
prerequisites_regex = re.compile(r"prerequisites\s*=\s*{(.*)}")
category_regex = re.compile(r"category\s*=\s*(\w+)")
subsection_type_regex = re.compile(r"(cost|upkeep|produces)\s*=\s*{")
mult_field_regex = re.compile(r"(?:multiplier|mult)\s*=\s*(\S+)")
ai_weight_base_regex = re.compile(r"base\s*=\s*([-+]?\d+\.?\d*)")


class pdscript_resource_table_subsection:
    def __init__(
        self,
        sub_type: str,
        trigger_block: str,
        resource_value_pairs: dict,
        multiplier: str,
    ):
        self.sub_type = sub_type
        self.trigger_block = trigger_block
        self.resource_value_pairs = resource_value_pairs
        self.multiplier = multiplier

    def multiply_economy(self, factor: float | int) -> None:
        """Multplies all valid resources = value pairs by a factor

        Args:
            factor (float | int): Number to multiply by
        """
        self.resource_value_pairs = {
            key: value * factor for key, value in self.resource_value_pairs.items()
        }

    def construct_subsection(self) -> str:
        """Constructs a valid resource subsection

        Returns:
            str: The resource subsection
        """
        if self.trigger_block.strip().startswith("always = no"):
            return ""

        subsection_output = f"\t\t{self.sub_type} = {{\n"

        if self.trigger_block.strip() != "always = yes":
            subsection_output += "\t\t\t\ttrigger = {\n"
            subsection_output += f"\t\t\t\t\t{self.trigger_block}\n"
            subsection_output += "\t\t\t\t}\n"

        for key, value in self.resource_value_pairs.items():
            subsection_output += f"\t\t\t\t{key} = {value}\n"

        if self.multiplier != 1.0:
            subsection_output += f"\t\t\t\tmultiplier = {self.multiplier}\n"

        subsection_output += "\t\t\t}"
        return subsection_output


class PDSArmy:
    def __init__(
        self,
        army_name: str,
        defensive: bool,
        occupation: bool,
        is_pop_spawned: bool,
        rebel: bool,
        damage: float,
        health: float,
        has_morale: bool,
        morale: float,
        morale_damage: float,
        collateral_damage: float,
        war_exhaustion: float,
        time: float,
        has_species: bool,
        disband_if_species_lacks_right: bool,
        icon: str,
        prerequisites: str,
        resource_table_category: str,
        resource_table: list[pdscript_resource_table_subsection],
        show_tech_unlock_if: str,
        potential: str,
        potential_country: str,
        allow: str,
        on_queued: str,
        on_unqueued: str,
        ai_weight_base: float,
        ai_weight_extra: str,
        spawn_chance: str,
        army_modifier: str,
    ):
        self.army_name = army_name
        self.use_army_names_from = self.army_name
        self.defensive = defensive
        self.occupation = occupation
        self.is_pop_spawned = is_pop_spawned
        self.rebel = rebel
        self.damage = damage
        self.health = health
        self.has_morale = has_morale
        self.morale = morale
        self.morale_damage = morale_damage
        self.collateral_damage = collateral_damage
        self.war_exhaustion = war_exhaustion
        self.time = time
        self.has_species = has_species
        self.disband_if_species_lacks_right = disband_if_species_lacks_right
        self.icon = icon
        self.prerequisites = prerequisites
        self.resource_table_category = resource_table_category
        self.resource_table = resource_table
        self.show_tech_unlock_if = show_tech_unlock_if
        self.potential = potential
        self.potential_country = potential_country.strip()
        self.allow = allow
        self.on_queued = on_queued
        self.on_unqueued = on_unqueued
        self.ai_weight_base = ai_weight_base
        self.ai_weight_extra = ai_weight_extra
        self.spawn_chance = spawn_chance
        self.army_modifier = army_modifier

        self.pmca_mult = "ten"
        self.pmca_resource = "food"
        self.pmca_resource_value = "0"

        if (
            self.potential.strip().startswith("always = no")
            or self.potential_country.strip().startswith("always = no")
            or self.allow.strip().startswith("always = no")
        ):
            self.unbuildable = True
        else:
            self.unbuildable = False

        blocks_to_indent = [
            "show_tech_unlock_if",
            "potential",
            "potential_country",
            "allow",
            "on_queued",
            "on_unqueued",
            "ai_weight_extra",
            "spawn_chance",
            "army_modifier",
        ]

        for block in blocks_to_indent:
            lines = self.__getattribute__(block).splitlines()
            tabbed_lines = ["\t" + line for line in lines]
            tabbed_string = "\n".join(tabbed_lines)
            self.__setattr__(block, tabbed_string)

    def convert_to_pdscript(self) -> str:
        """Turns all of the class variables into a string

        Returns:
            str: A string that should make a functioning army in PDScript
        """
        pdscript_output = ""

        pdscript_output += f"\tpmca_{self.pmca_mult}_{self.army_name} = {{\n"
        pdscript_output += f"\t\tuse_armynames_from = {self.use_army_names_from}\n"

        if self.defensive:
            pdscript_output += f"\t\tdefensive = yes\n"
        if self.occupation:
            pdscript_output += f"\t\toccupation = yes\n"
        if self.is_pop_spawned:
            pdscript_output += f"\t\tis_pop_spawned = yes\n"
        if self.rebel:
            pdscript_output += f"\t\trebel = yes\n"

        pdscript_output += f"\t\tdamage = {self.damage}\n"
        pdscript_output += f"\t\thealth = {self.health}\n"

        if not self.has_morale:
            pdscript_output += f"\t\thas_morale = no\n"
        else:
            pdscript_output += f"\t\tmorale = {self.morale}\n"

        pdscript_output += f"\t\tmorale_damage = {self.morale_damage}\n"
        pdscript_output += f"\t\tcollateral_damage = {self.collateral_damage}\n"
        pdscript_output += f"\t\twar_exhaustion = {self.war_exhaustion}\n"
        pdscript_output += f"\t\ttime = {self.time}\n"

        if not self.has_species:
            pdscript_output += f"\t\thas_species = no\n"
        if not self.disband_if_species_lacks_right:
            pdscript_output += f"\t\tdisband_if_species_lacks_right = no\n"

        pdscript_output += f"\t\ticon = {self.icon}\n"

        if len(self.prerequisites) > 0:
            list_of_techs = re.findall(r"\w+", str(self.prerequisites))
            pdscript_output += f"\t\tprerequisites = {{"
            if len(list_of_techs) == 1:
                pdscript_output += f" {list_of_techs[0]} }}\n"
            else:
                pdscript_output += "\n" + "\n".join(
                    f"\t\t\t{item}" for item in list_of_techs
                )
                pdscript_output += f"\n\t\t}}\n"

        if len(self.resource_table) > 0:
            pdscript_output += f"\t\tresources = {{\n"
            pdscript_output += f"\t\t\tcategory = {self.resource_table_category}\n"
            pdscript_output += "\n".join(
                f"\t{subsection.construct_subsection()}"
                for subsection in self.resource_table
            )
            pdscript_output += f"\n\t\t}}\n"

        if self.show_tech_unlock_if.strip():
            pdscript_output += f"\t\tshow_tech_unlock_if = {{\n"
            pdscript_output += f"\t\t\t{self.show_tech_unlock_if.strip()}\n"
            pdscript_output += f"\t\t}}\n"

        if self.unbuildable:
            pdscript_output += "\t\tpotential = { always = no }\n"
        else:
            if self.potential.strip():
                pdscript_output += f"\t\tpotential = {{\n"
                pdscript_output += f"\t\t\t{self.potential.strip()}\n"
                pdscript_output += f"\t\t}}\n"

            pdscript_output += f"\t\tpotential_country = {{\n"
            pdscript_output += (
                f"\t\t\t{self.potential_country.strip()}\n"
                if self.potential_country.strip()
                else ""
            )
            pdscript_output += f"\t\t\tpmca_materiel_policy_check = {{\n\t\t\t\tPMCA_MULT = {self.pmca_mult}\n\t\t\t\tPMCA_RESOURCE = {self.pmca_resource}\n\t\t\t\tPMCA_VALUE = {self.pmca_resource_value}\n\t\t\t}}\n"
            pdscript_output += f"\t\t}}\n"

            if self.allow.strip():
                pdscript_output += f"\t\tallow = {{\n"
                pdscript_output += f"\t\t\t{self.allow.strip()}\n"
                pdscript_output += f"\t\t}}\n"

            if self.on_queued.strip():
                pdscript_output += f"\t\ton_queued = {{\n"
                pdscript_output += f"\t\t\t{self.on_queued.strip()}\n"
                pdscript_output += f"\t\t}}\n"

            if self.on_unqueued.strip():
                pdscript_output += f"\t\ton_unqueued = {{\n"
                pdscript_output += f"\t\t\t{self.on_unqueued.strip()}\n"
                pdscript_output += f"\t\t}}\n"

            pdscript_output += f"\t\tai_weight = {{\n"
            pdscript_output += f"\t\t\tbase = {self.ai_weight_base}\n"
            pdscript_output += (
                f"\t\t\t{self.ai_weight_extra.strip()}\n"
                if self.ai_weight_extra.strip()
                else ""
            )
            pdscript_output += f"\t\t}}\n"

        if self.spawn_chance.strip():
            pdscript_output += f"\t\tspawn_chance = {{\n"
            pdscript_output += f"\t\t\t{self.spawn_chance.strip()}\n"
            pdscript_output += f"\t\t}}\n"

        if self.army_modifier.strip():
            pdscript_output += f"\t\tarmy_modifier = {{\n"
            pdscript_output += f"\t\t\t{self.army_modifier.strip()}\n"
            pdscript_output += f"\t\t}}\n"

        pdscript_output += f"\t}}\n"
        return pdscript_output


###########################
### NON-CLASS FUNCTIONS ###
###########################


def scan_input_file() -> None:
    """
    Scans 'input.txt' for army definitions.
    """

    # Read content from the file
    with open("input.txt", "r") as file_input:
        file_content = file_input.read()

    # Find scripted variable declarations
    scripted_variables = dict(
        re.findall(scripted_variable_assignment_regex, file_content)
    )

    # Delete scripted variable declarations so they don't screw up the parsing
    file_content = re.sub(scripted_variable_assignment_regex, "", file_content)

    # Replaces any used of scripted variables if possible
    for key, value in scripted_variables.items():
        file_content = file_content.replace(key, value)

    # Remove quotes and split content into lines
    file_content = file_content.replace('"', "")
    file_lines = file_content.splitlines(True)

    brace_level = 0
    army_definition = ""

    for line in file_lines:
        # Ignore empty lines or comments
        if line.strip() and not (
            line.strip().startswith("#") or line.strip().startswith("@")
        ):
            # Count brace levels
            brace_level += line.count("{")
            brace_level -= line.count("}")

            army_definition += line

            # If the brace level is balanced, parse the army
            if brace_level == 0:
                list_of_armies.append(parse_army(army_definition))
                army_definition = ""


def parse_army(input_string: str) -> PDSArmy:
    """Parses a given string into the various parts needed to make a valid PDScript army

    Args:
        input_string (str): A string containing an army definition

    Returns:
        pdscript_army: A pdscript_army object
    """

    brace_level = 0
    block_data = {
        "prerequisites": [-1, ""],
        "resources": [-1, ""],
        "show_tech_unlock_if": [-1, ""],
        "potential": [-1, ""],
        "potential_country": [-1, ""],
        "allow": [-1, ""],
        "on_queued": [-1, ""],
        "on_unqueued": [-1, ""],
        "ai_weight": [-1, ""],
        "spawn_chance": [-1, ""],
        "army_modifier": [-1, ""],
    }
    block_name = None
    list_of_complex_blocks = re.findall(complex_block_regex, input_string)
    list_of_complex_blocks.reverse()

    for i, char in enumerate(input_string):
        if char == "{":
            brace_level += 1
            # Entered a = { } block
            if brace_level == 2:
                block_name = list_of_complex_blocks.pop()
                if block_name:
                    block_data[block_name][0] = i

        elif char == "}":
            brace_level -= 1
            # Exited a = { } block
            if brace_level == 1:
                if block_name:
                    block_data[block_name][1] = input_string[
                        block_data[block_name][0] + 1 : i
                    ]

    # Find and assign the simple inputs
    field_value_tuple = re.findall(field_value_pair_regex, input_string) + re.findall(
        field_bool_pair_regex, input_string
    )
    field_value_dict = {
        item[0]: (
            True if item[1] == "yes" else False if item[1] == "no" else float(item[1])
        )
        for item in field_value_tuple
    }

    input_army_name = re.match(block_regex, input_string).group(1)
    input_defensive = get_field_value(field_value_dict, "defensive", False)
    input_occupation = get_field_value(field_value_dict, "occupation", False)
    input_is_pop_spawned = get_field_value(field_value_dict, "is_pop_spawned", False)
    input_rebel = get_field_value(field_value_dict, "rebel", False)
    input_health = get_field_value(field_value_dict, "health", 1.00)
    input_damage = get_field_value(field_value_dict, "damage", 1.00)
    input_has_morale = get_field_value(field_value_dict, "has_morale", True)
    input_morale = get_field_value(field_value_dict, "morale", 1.00)
    input_morale_damage = get_field_value(field_value_dict, "morale_damage", 1.00)
    input_collateral_damage = get_field_value(
        field_value_dict, "collateral_damage", 1.00
    )
    input_war_exhaustion = get_field_value(field_value_dict, "war_exhaustion", 1.00)
    input_time = get_field_value(field_value_dict, "time", 0.00)
    input_has_species = get_field_value(field_value_dict, "has_species", True)
    input_disband_if_species_lacks_right = get_field_value(
        field_value_dict, "disband_if_species_lacks_right", True
    )

    icon_match = re.search(icon_regex, input_string)
    input_icon = icon_match.group(1) if icon_match else "GFX_army_type_defensive"

    # Handle complex (nested braces) inputs
    input_resource_table_category, input_resource_table = parse_resource_table(
        block_data.get("resources")[1]
    )
    input_prerequisites = block_data.get("prerequisites")[1]
    input_show_tech_unlock_if = block_data.get("show_tech_unlock_if")[1]
    input_potential = block_data.get("potential")[1]
    input_potential_country = block_data.get("potential_country")[1]
    input_allow = block_data.get("allow")[1]
    input_on_queued = block_data.get("on_queued")[1]
    input_on_unqueued = block_data.get("on_unqueued")[1]
    input_ai_weight_base, input_ai_weight_extra = parse_ai_weight(
        block_data.get("ai_weight")[1]
    )
    input_spawn_chance = block_data.get("spawn_chance")[1]
    input_army_modifier = block_data.get("army_modifier")[1]

    new_army = PDSArmy(
        army_name=input_army_name,
        defensive=input_defensive,
        occupation=input_occupation,
        is_pop_spawned=input_is_pop_spawned,
        rebel=input_rebel,
        damage=input_damage,
        health=input_health,
        has_morale=input_has_morale,
        morale=input_morale,
        morale_damage=input_morale_damage,
        collateral_damage=input_collateral_damage,
        war_exhaustion=input_war_exhaustion,
        time=input_time,
        has_species=input_has_species,
        disband_if_species_lacks_right=input_disband_if_species_lacks_right,
        icon=input_icon,
        prerequisites=input_prerequisites,
        resource_table_category=input_resource_table_category,
        resource_table=input_resource_table,
        show_tech_unlock_if=input_show_tech_unlock_if,
        potential=input_potential,
        potential_country=input_potential_country,
        allow=input_allow,
        on_queued=input_on_queued,
        on_unqueued=input_on_unqueued,
        ai_weight_base=input_ai_weight_base,
        ai_weight_extra=input_ai_weight_extra,
        spawn_chance=input_spawn_chance,
        army_modifier=input_army_modifier,
    )

    return new_army


def get_field_value(dictionary: dict, search_item: any, default_if_none: any) -> any:
    """Gets a value from a dictionary if possible

    Args:
        dictionary (dict): Dictionary to search
        search_item (any): What to search for
        default_if_none (any): If search_item doesn't exist

    Returns:
        any: Value of search_item, or default_if_none
    """
    return dictionary.get(search_item, default_if_none)


def parse_resource_table(input_string: str) -> tuple[str, list]:
    """Parses a valid resource table

    Args:
        input_string (str): A valid resource table as a string

    Returns:
        tuple[str, list]: [0] is the economic category | [1] is a list of pdscript_resource_table_subsection
    """
    current_brace_level = 0
    RESOURCE_TABLE_BRACE_LEVEL = 0
    SUBSECTION_BRACE_LEVEL = 1
    SUBSECTION_TRIGGER_BRACE_LEVEL = 2

    opening_brace_stack = []

    category = ""
    subsection_type = ""
    subsection_trigger_data = ""
    subsection_data = ""
    resource_pairs = {}
    mult_value = 1.0

    list_of_subsections = []

    category_match = re.search(category_regex, input_string)
    category = category_match.group(1) if category_match else "armies"

    subection_types = re.findall(subsection_type_regex, input_string)
    subection_types.reverse()

    for i, char in enumerate(input_string):
        if char == "{":
            current_brace_level += 1

            # Must have entered a subsection
            if current_brace_level == SUBSECTION_BRACE_LEVEL:
                opening_brace_stack.append(i)
                subsection_type = subection_types.pop()

            # Must have entered the subsection's trigger block
            elif current_brace_level == SUBSECTION_TRIGGER_BRACE_LEVEL:
                opening_brace_stack.append(i)
                subsection_trigger_data += "trigger = "

        elif char == "}":
            current_brace_level -= 1

            # Must have exited the subsection's trigger block
            if current_brace_level == SUBSECTION_BRACE_LEVEL:
                subsection_trigger_data += input_string[
                    opening_brace_stack.pop() : i + 1
                ]

            # Must have exited the subsection
            elif current_brace_level == RESOURCE_TABLE_BRACE_LEVEL:
                # Capture the subsections data
                subsection_data = input_string[opening_brace_stack.pop() + 1 : i]
                # Already have the trigger block, no need for another
                subsection_data = subsection_data.replace(subsection_trigger_data, "")
                # Capture the trigger's data
                trigger_first_brace_index = subsection_trigger_data.find("{")
                trigger_last_brace_index = subsection_trigger_data.rfind("}")
                subsection_trigger_data = subsection_trigger_data[
                    trigger_first_brace_index + 1 : trigger_last_brace_index
                ]

                # If there's anything in the subsection...
                if subsection_data.strip():
                    # Try to find all of the resource = value pairs
                    temp_resource_tuples = re.findall(
                        field_value_pair_regex, subsection_data
                    )
                    resource_pairs = {
                        key: float(value) for key, value in temp_resource_tuples
                    }
                    # Try to find the multiplier if it exists
                    if "mult" in subsection_data or "multiplier" in subsection_data:
                        if resource_pairs.get("mult"):
                            mult_value = resource_pairs.get("mult")
                            resource_pairs.pop("mult")
                        elif resource_pairs.get("multiplier"):
                            mult_value = resource_pairs.get("multiplier")
                            resource_pairs.pop("multiplier")
                        else:
                            mult_match = re.search(mult_field_regex, subsection_data)
                            mult_value = mult_match.group(1) if mult_match else 1.0

                    # If there's no trigger, default to always = yes
                    if not (subsection_trigger_data.strip()):
                        subsection_trigger_data = "always = yes"

                    new_resource_subsection = pdscript_resource_table_subsection(
                        sub_type=subsection_type,
                        trigger_block=subsection_trigger_data,
                        resource_value_pairs=resource_pairs,
                        multiplier=mult_value,
                    )

                    list_of_subsections.append(new_resource_subsection)

                # Set to blank for safety
                subsection_type = ""
                subsection_trigger_data = ""
                subsection_data = ""
                resource_pairs = {}
                mult_value = 1.0

    return category, list_of_subsections


def parse_ai_weight(input_string: str) -> tuple[float, str]:
    """Parses a valid AI weight block

    Args:
        input_string (str): A valid ai_weight block

    Returns:
        tuple[float, str]: [0] is the first instance of 'base', defaults to 0 | [1] is the rest of the input
    """
    ai_weight_base = 0
    ai_weight_string = ""

    ai_weight_base_match = re.search(ai_weight_base_regex, input_string)
    ai_weight_base = (
        float(ai_weight_base_match.group(1)) if ai_weight_base_match else 0.00
    )

    ai_weight_string = re.sub(ai_weight_base_regex, "", input_string, 1)

    return ai_weight_base, ai_weight_string


##################################
### CONDENSED ARMIES FUNCTIONS ###
##################################


directory = ".\PMCA_GEN_OUTPUT"
common_folder = os.path.join(directory, "common")
armies_folder = os.path.join(common_folder, "armies")
localisation_folder = os.path.join(directory, "localisation")


def multiply_stats(input_army: PDSArmy, factor: float | int) -> None:
    """Multiplies an army's stats by a number

    Args:
        input_army (pdscript_army): A valid army object
        factor (float | int): A number to multiply the stats by
    """
    # Multiply regular stats
    input_army.damage *= factor
    input_army.health *= factor
    input_army.morale *= factor
    input_army.collateral_damage *= factor
    input_army.war_exhaustion *= factor
    for subsection in input_army.resource_table:
        subsection.multiply_economy(factor)


def condense_armies(input_army: PDSArmy, is_hundred: bool) -> None:
    """Turns an army into a x10/x100 pmca army

    Args:
        input_army (pdscript_army): A valid army object
        is_hundred (bool): Are you going from vanilla > x10 or x10 > x100?
    """
    input_army.pmca_mult = "hundred" if is_hundred else "ten"

    if not is_hundred:
        for subsection in input_army.resource_table:
            if subsection.sub_type == "cost":
                for key, value in subsection.resource_value_pairs.items():
                    priority = resource_priority_dict.get(key, 7)
                    if priority >= resource_priority_dict.get(
                        input_army.pmca_resource, 7
                    ):
                        input_army.pmca_resource = key
                        input_army.pmca_resource_value = value
    else:
        input_army.pmca_resource_value *= 10

    ai_weight_multiplier = (2 / 3 * 2) if is_hundred else 1.5
    input_army.ai_weight_base *= ai_weight_multiplier


trigger_regex_patterns = {
    # NOT = { } checks have to be first to prevent weirdness
    # Authority Checks
    re.compile(
        r"NOT\s*=\s*{\s*\n?has_authority\s*=\s*auth_machine_intelligence\s*\n?}"
    ): "is_machine_empire = no",
    re.compile(
        r"has_authority\s*=\s*auth_machine_intelligence"
    ): "is_machine_empire = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?has_authority\s*=\s*auth_hive_mind\s*\n?}"
    ): "is_hive_empire = no",
    re.compile(r"has_authority\s*=\s*auth_hive_mind"): "is_hive_empire = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?has_ethic\s*=\s*ethic_gestalt_consciousness\s*\n?}"
    ): "is_gestalt = no",
    re.compile(r"has_ethic\s*=\s*ethic_gestalt_consciousness"): "is_gestalt = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?has_authority\s*=\s*auth_corporate\s*\n?}"
    ): "is_megacorp = no",
    re.compile(r"has_authority\s*=\s*auth_corporate"): "is_megacorp = yes",
    # DLC Checks
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Leviathans Story Pack\s*\n?}"
    ): "has_leviathans = no",
    re.compile(r"host_has_dlc\s*=\s*Leviathans Story Pack"): "has_leviathans = yes",
    re.compile(r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Utopia\s*\n?}"): "has_utopia = no",
    re.compile(r"host_has_dlc\s*=\s*Utopia"): "has_utopia = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Plantoids Species Pack\s*\n?}"
    ): "has_plantoids = no",
    re.compile(r"host_has_dlc\s*=\s*Plantoids Species Pack"): "has_plantoids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Synthetic Dawn Story Pack\s*\n?}"
    ): "has_synthethic_dawn = no",
    re.compile(
        r"host_has_dlc\s*=\s*Synthetic Dawn Story Pack"
    ): "has_synthethic_dawn = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Humanoids Species Pack\s*\n?}"
    ): "has_humanoids = no",
    re.compile(r"host_has_dlc\s*=\s*Humanoids Species Pack"): "has_humanoids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?local_has_dlc\s*=\s*Humanoids Species Pack\s*\n?}"
    ): "has_humanoids_local = no",
    re.compile(
        r"local_has_dlc\s*=\s*Humanoids Species Pack"
    ): "has_humanoids_local = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Lithoids Species Pack\s*\n?}"
    ): "has_lithoids = no",
    re.compile(r"host_has_dlc\s*=\s*Lithoids Species Pack"): "has_lithoids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Federations\s*\n?}"
    ): "has_federations_dlc = no",
    re.compile(r"host_has_dlc\s*=\s*Federations"): "has_federations_dlc = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Necroids Species Pack\s*\n?}"
    ): "has_necroids = no",
    re.compile(r"host_has_dlc\s*=\s*Necroids Species Pack"): "has_necroids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Nemesis\s*\n?}"
    ): "has_nemesis = no",
    re.compile(r"host_has_dlc\s*=\s*Nemesis"): "has_nemesis = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Aquatics Species Pack\s*\n?}"
    ): "has_aquatics = no",
    re.compile(r"host_has_dlc\s*=\s*Aquatics Species Pack"): "has_aquatics= yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Overlord\s*\n?}"
    ): "has_overlord_dlc = no",
    re.compile(r"host_has_dlc\s*=\s*Overlord"): "has_overlord_dlc = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Toxoids Species Pack\s*\n?}"
    ): "has_toxoids = no",
    re.compile(r"host_has_dlc\s*=\s*Toxoids Species Pack"): "has_toxoids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*First Contact Story Pack\s*\n?}"
    ): "has_first_contact_dlc = no",
    re.compile(
        r"host_has_dlc\s*=\s*First Contact Story Pack"
    ): "has_first_contact_dlc = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Astral Planes\s*\n?}"
    ): "has_astral_planes_dlc = no",
    re.compile(r"host_has_dlc\s*=\s*Astral Planes"): "has_astral_planes_dlc = yes",
}


def optimize_trigger(input_army: PDSArmy) -> None:
    """Converts common triggers with vanilla scripted_triggers for compatibility

    Args:
        input_army (pdscript_army): Army object to optimize
    """

    for pattern, replacement in trigger_regex_patterns.items():
        input_army.show_tech_unlock_if = re.sub(
            pattern, replacement, input_army.show_tech_unlock_if
        )
        input_army.potential = re.sub(pattern, replacement, input_army.potential)
        input_army.potential_country = re.sub(
            pattern, replacement, input_army.potential_country
        )
        input_army.allow = re.sub(pattern, replacement, input_army.allow)
        input_army.ai_weight_extra = re.sub(
            pattern, replacement, input_army.ai_weight_extra
        )


def create_folders() -> None:
    """Creates the required folders"""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    os.makedirs(common_folder)
    os.makedirs(armies_folder)
    os.makedirs(localisation_folder)
    for language in stellaris_languages:
        os.makedirs(os.path.join(localisation_folder, language))


def generate_defs(file_prefix: str, mod_variable: str) -> None:
    """Generates and writes the required syntax for the inline_script to work

    Args:
        file_prefix (str): Newly created files will start with this
        mod_variable (str): Scripted variable to detect for the conditional inline to work
    """
    # Needed so Irony doesn't troll us
    army_output = "# Dear Irony please fallback to simple parser\n# x10 and x100 army definition(s) generated via Python\n\n"
    army_defs = os.path.join(armies_folder, f"{file_prefix}_armies.txt")

    # Syntax for the inline
    army_output += "inline_script = {\n"
    army_output += "\tscript = army/pmca_conditional_inline_p1\n"
    army_output += f"\tMOD_VARIABLE = {mod_variable}\n"
    army_output += '\tCONTENT = "\n'

    for army in list_of_armies:
        multiply_stats(army, 10)
        condense_armies(army, False)
        army_output += f"{army.convert_to_pdscript()}\n"

    for army in list_of_armies:
        multiply_stats(army, 10)
        condense_armies(army, True)
        army_output += f"{army.convert_to_pdscript()}\n"

    # Get rid of the double newline
    army_output = army_output[:-1]

    # Closing quote and brace for the inline
    army_output += '\t"\n'
    army_output += "}\n"

    with open(army_defs, "w+") as fout:
        fout.write(army_output)


def generate_localisation_keys(file_name_prefix: str) -> None:
    """Generates the necessary localisation keys

    Args:
        file_name_prefix (str): Newly created files will start with this
    """
    localisation_output = ""
    army_name_keys = []

    for army in list_of_armies:
        if (
            file_name_prefix == "pmca_vanilla"
            or file_name_prefix == "pmca"
            or army.use_army_names_from not in vanilla_army_keys
        ):
            army_name_keys.append(army.use_army_names_from)

    for key in army_name_keys:
        comment_block = "#" * len(f"### {key} ###")
        localisation_output += f"\n {comment_block}\n"
        localisation_output += f" ### {key.upper()} ###\n"
        localisation_output += f" {comment_block}\n"
        localisation_output += f' pmca_ten_{key}: "$pmca_ten$ ${key}$"\n'
        localisation_output += f' pmca_ten_{key}_plural: "${key}_plural$"\n'
        localisation_output += f' pmca_ten_{key}_desc: "${key}_desc$"\n'
        localisation_output += f' pmca_hundred_{key}: "$pmca_hundred$ ${key}$"\n'
        localisation_output += f' pmca_hundred_{key}_plural: "${key}_plural$"\n'
        localisation_output += f' pmca_hundred_{key}_desc: "${key}_desc$"\n\n'

    for language in stellaris_languages:
        language_folder = os.path.join(localisation_folder, language)
        file_name = os.path.join(
            language_folder, f"{file_name_prefix}_l_{language}.yml"
        )
        with open(file_name, "w", encoding="utf-8-sig") as file_output:
            file_output.write(
                f"l_{language}:\n\n # Localisation generated using Python\n{localisation_output}"
            )


def print_stats(file_name_prefix: str, time_taken: float) -> None:
    """Prints some stats

    Args:
        file_name_prefix (str): Needed to check for if vanilla loc keys were generated
        time_taken (float): How much time the progam took
    """

    modded_set = set(army.army_name for army in list_of_armies)
    num_common_elements = vanilla_army_keys.intersection(modded_set)

    print("Done! Please check './PMCA_GEN_OUTPUT/' for your Condensed Armies!\n")
    print("\n------------------------\n")
    print("Stats:")
    print(f"  - Number of Army Definitions: {len(list_of_armies)}")
    print(f"  - Number of Vanilla Overwrites: {len(num_common_elements)}")
    print(f"  - Number of languages supported by Stellaris: {len(stellaris_languages)}")
    num_generated_loc_keys = len(list_of_armies) * 6 * len(stellaris_languages)
    if not (file_name_prefix == "pmca_vanilla" or file_name_prefix == "pmca"):
        num_generated_loc_keys -= (
            len(num_common_elements) * 6 * len(stellaris_languages)
        )
    print(
        f"  - Number of localisation keys generated: {num_generated_loc_keys} total | {num_generated_loc_keys // len(stellaris_languages)} per locale"
    )
    print(f"  - Estimated time to complete: {round(time_taken, 3)} milliseconds\n")


def scan_armies_for_issues() -> bool:
    """Adds armies that are unbuildable to a list for viewing later

    Returns:
        bool: True if any armies were added to the issues list, False otherwise
    """

    added_any_army_to_issues_list = False
    attributes_to_check = [
        "potential_country",
        "potential",
        "allow",
        "on_queued",
        "on_unqueued",
        "ai_weight_extra",
        "show_tech_unlock_if",
    ]
    variable_modification_regex = re.compile(r".+_variable(?:.+)?\s*=\s*{")

    for army in list_of_armies:
        if army.unbuildable:
            armies_with_issues["Unbuildable"].append(army.army_name)
            added_any_army_to_issues_list = True
        if army.defensive or army.occupation or army.rebel or army.is_pop_spawned:
            armies_with_issues["Odd Property"].append(army.army_name)
            added_any_army_to_issues_list = True
        for attribute in attributes_to_check:
            variable_modification_match = re.search(
                variable_modification_regex, getattr(army, attribute)
            )
            if variable_modification_match:
                armies_with_issues["Variable Manipulation"].append(army.army_name)
                added_any_army_to_issues_list = True

    return added_any_army_to_issues_list


def armies_with_issues_handler() -> None:
    """Handles outputting armies w/ concerning properties to pcma_issues.txt"""

    issue_string = ""

    if armies_with_issues["Unbuildable"]:
        issue_string += "Armies that are unbuildable:\n"
        for value in armies_with_issues["Unbuildable"]:
            issue_string += f"\t- {value}\n"

    if armies_with_issues["Odd Property"]:
        issue_string += "Armies with Odd Properties:\n"
        for value in armies_with_issues["Odd Property"]:
            issue_string += f"\t- {value}\n"

    if armies_with_issues["Variable Manipulation"]:
        issue_string += "Armies with Variable Manipulation:\n"
        for value in armies_with_issues["Variable Manipulation"]:
            issue_string += f"\t- {value}\n"

    issue_string += f"\n\nHere's a quick breakdown of the terms:\n"
    issue_string += f"\t- 'Armies that are unbuildable'\n\t\t* The armies' potential, potential_country, or allow starts with 'always = no'\n"
    issue_string += f"\t- 'Armies with Odd Properties'\n\t\t* The army is one of the following: defensive, occupation, rebel, or is_pop_spawned\n"
    issue_string += f"\t- 'Armies with Variable Manipulation'\n\t\t* The armies' potential_country, potential, allow, on_queued, on_unqueued, ai_weight, or show_tech_unlock_if include some sort of variable effect or trigger"
    issue_string += (
        f"\nKeep in mind that these are merely warnings and can be ignored if needed."
    )

    with open("pmca_issues.txt", "w") as fout:
        fout.write(issue_string)


def clean_up() -> None:
    """Resets variables for potential reruns
    """
    global list_of_armies
    list_of_armies.clear()


def pmca() -> None:
    """Main function"""

    if os.path.isfile("input.txt"):
        input_file_prefix = input(
            "\nEnter a custom file prefix, or leave blank to default to 'REPLACE_ME': "
        )

        file_prefix = input_file_prefix if input_file_prefix.strip() else "REPLACE_ME"

        input_mod_variable = input(
            "Enter the mod's ID Variable, or leave blank if making an external patch: "
        )
        if input_mod_variable.strip() and input_mod_variable.strip()[0] == "@":
            mod_variable = input_mod_variable.strip()
        else:
            mod_variable = (
                "@" + input_mod_variable
                if input_mod_variable.strip()
                else "@has_condensed_armies"
            )

        start = time.time()

        print("\nSetting up folders...")
        create_folders()

        print("Scanning input.txt...")
        scan_input_file()

        for army in list_of_armies:
            optimize_trigger(army)

        print("Generating condensed army definitions...")
        generate_defs(file_prefix, mod_variable)

        print("Generating localisation...")
        generate_localisation_keys(file_prefix)

        end = time.time()
        time_duration = (end - start) * 1000

        print_stats(file_prefix, time_duration)

        if (
            scan_armies_for_issues()
            and input(
                "Some armies were detected as having concerning properties, would you like to print them to 'pmca_issues.txt'? Y/N: "
            ).upper()[:1]
            == "Y"
        ):
            armies_with_issues_handler()

        # Keep stats on screen
        if input("Do you wish to rerun the program? Y/N: ").upper() == "Y":
            clean_up()
            pmca()

    else:
        print("ERROR: 'input.txt' was not found!")


if __name__ == "__main__":
    pmca()

# Set file prefix to pmca or pmca_vanilla to generate localisation keys for vanilla armies
#
# Common scripted variables for copy pasting
# @has_gigastructures
# @ESC_WEAPON_crystalline_s_t6_cost_crystals
# @has_ancient_caches
# @has_acquisition_of_tech
# @has_stellaris_evolved
# @slgt_Tier6_cost
#
#
#
#
#
#
#
#
