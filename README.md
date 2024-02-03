# Condensed Armies Logistics Mananger Patcher

## Introduction
The Condensed Armies Logistics Manager Patcher (`C.A.L.M.P.`) is a little Python script that I've been semi-frequently working on since early 2023 to help maintain my mod Condensed Armies and its various patches. 

Turning what normally could be a few minutes to a few hours worth of work into only a minute or so is incredibly useful, especially if I want to do more iterative changes with my mod as PDS constantly updates the game.

Feel free to use the script yourself, either to make a patch or to make your own parser for PDScript[^1].

[^1]: Nested braces and resource tables... I feel bad for whoever at PDS had to code the parser for PDScript. Admittedly my code only works because there are no repeating elements (triggered_x_modifer), but if there were I'd have to switch to something like pyparsing to handle it.

### Prerequisites
Requirements:
  - [Ability to mod Stellaris](https://stellaris.paradoxwikis.com/Modding_tutorial)
  - Can run Python scripts

Python Information:
  - Version: 3.10.6
  - Modules: `re, time, os, shutil` 

## Installation
1. Download pmca_generator_v2.py
2. Create a file wherever pmca_generator_v2.py is called `input.txt`

## Usage
### Input Sanitization
Before continuing, make sure that whatever armies you want to patch aren't going cause issues.
<details>
<summary>Multiple army defs on a single line</summary>

`C.A.L.M.P.` detects army definitions by iterating line-by-line and counting braces. If the number of unmatched braces is 0, C.A.L.M.P. tries to send whatever was between the first brace and the last to be parsed. In short:

```txt
# This is bad, don't do this
some_army_definition = { ... } another_army_definition = { ... }
```

```txt
# This, on the other hand, is fine
some_army_definition = { ... }
another_army_definition = { ... }

my_cool_army_definition = {
  ...
}
```
</details>

<details>
<summary>Inline Scripts</summary>

`C.A.L.M.P.` currently (and probably never will) handle inline_scripts, and will probably throw an error and cry if it sees one.

To fix: Replace the inline_script with whatever is meant to go there.

</details>

<details>
<summary>Quotation Marks</summary>

`C.A.L.M.P.` deletes all quotation marks as to not screw with the inline_script Condensed Armies uses.

To fix: Make sure that whatever used quotation marks works fine without them.

</details>

<details>
<summary>Scripted Variables</summary>

`C.A.L.M.P` *can* handle some scripted_variable, with a few caveats. If you use a scripted_variable for something that will be multiplied (damage, cost, morale, produces, etc), you must do one of following:

A. Replace every scripted_variable with whatever value it represents (e.g. `@b1_minerals` -> `400`)

B. Define the scripted_variable at the top[^2] of the file like so:
```txt
@b1_minerals = 400

army_with_scripted_variable = {
  ...
  resources = {
    category = armies
    cost = {
      minerals = @b1_minerals # will be replaced with 400 during run-time
    }
  }
}
```
And `C.A.L.M.P` will replace every instance of that scripted_variable with whatever value was assigned to it during run-time.

[^2]: The script scans the whole file using [regex](https://regex101.com/r/NwasGq/1) to find scripted_variable declarations, so there's technically nothing stopping you from defining it anywhere.
</details>

Now that you've made sure that the `C.A.L.M.P` won't throw a hissy-fit, you can finally start using the script.

### Instructions

1. Paste the armies you want to patch into `input.txt`
2. Run `pmca_generator_v2.py`, either by double-clicking or via the command prompt or w/e
3. You will be prompted for two inputs:
    - Custom file prefix: Pretty much anything is valid, but please avoid doing `pmca_<mod_prefix>` as that is the format I use for Condensed Armies
    - Mod ID Variable: Unless you're making an integrated patch, just press enter
4. If something breaks, you'll know by now.
5. If nothing breaks, a bunch of stats should've been printed and a folder called `PMCA_GEN_OUTPUT` should now be visible along with all of the necessary[^3] files to make the armies work. Just drag and drop and you're pretty much done.
6. You'll be given a prompt to rerun the program, if you want to.
    - If you're given a prompt about "concering armies", enter Y if you want to see why they're considered concerning. You could also just ignore it if you want[^4].

[^3]: If, for whatever reason, you want to generate localisation keys vanilla Condensed Armies, enter `pmca` or `pmca_vanilla` for the file prefix
[^4]: For the moment, the only mod that triggers these warnings that I ignore is ACOT since I simulate similar army mechanics for Condensed Armies. Otherwise, there's little point in Condensing armies that are usually only spawned via script.

## Troubleshooting
If `C.A.L.M.P` ever crashes for non-obvious reasons, feel free to make a bug report with the army in question.

