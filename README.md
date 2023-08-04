# How to make a patch for Condensed Armies
This guide will assume:
1. You know how to mod Stellaris. (Required)
2. How to run Python scripts. (Optional, but heavily recommended)

If you do not know how to mod Stellaris, I'd recommend starting with the [Modding Tutorial](https://stellaris.paradoxwikis.com/Modding_tutorial).

# Patching with Python (Recommended)
**Required: Python 3.8.10 or Later**

1. Download `pmca_generator.py` and extract it wherever, then create a new file called `input.txt` (An example input.txt has been provided if you want to see how it should look)
2. Paste the army definitions that you want to patch inside `input.txt` (See below for what armies should be deleted)
3. Run `pmca_generator.py`. It will ask for an input for a custom file name. Assuming you did not enter one, here's what the resulting file structure will look like:
```
PMCA_GEN_OUTPUT/
├─ common/
│  ├─ armies/
│  │  ├─ REPLACE_ME_x10_armies.txt
│  │  ├─ REPLACE_ME_x100_armies.txt
├─ localisation/
│  ├─ REPLACE_ME_l_braz_por.yml
│  ├─ REPLACE_ME_l_english.yml
│  ├─ REPLACE_ME_l_french.yml
│  ├─ REPLACE_ME_l_german.yml
│  ├─ REPLACE_ME_l_japanese.yml
│  ├─ REPLACE_ME_l_korean.yml
│  ├─ REPLACE_ME_l_polish.yml
│  ├─ REPLACE_ME_l_russian.yml
│  ├─ REPLACE_ME_l_simp_chinese.yml
├─ ├─ REPLACE_ME_l_spanish.yml
```
If you did enter a custom file name, just replace REPLACE_ME with whatever you entered.

### What types of armies shouldn't be condensed? ###
- Anything that involves variables
- Unbuildable Armies (i.e event spawn armies)
- Defensive Armies are your choice tbh, I personally don't but the script doesn't care either way

### Ignored Lines ###
The script will disregard empty lines and any lines beginning with the `#` character.

## Script clean-up
* CTRL + F `pmca_materiel_policy_check` and make sure that:
  * `PMCA_RESOURCE` points towards the most difficult resource to maintain. This is entirely subjective, so there's no issue with picking the "wrong resource"
  * `PMCA_VALUE` matches `PMCA_RESOURCE` cost.
    * Resources in triggered cost blocks should be ignored, but it's your choice.


And always make sure to actually test the mod in-game!

## Localisation
Check the `localisation` folder inside `PMCA_GEN_OUTPUT`
 
# Patching Manually
To be honest, it's pretty dull. Just go through every. single. line. and multiply the number by x10/x100, except for build time and morale damage.
For AI weight, the x10 version should have a 1.5x higher base, with x100 armies having a 2x base. So a vanilla army with an AI weight of 100 should have a weight of 150/200 for x10 and x100 respectively.
And make sure to add the pmca_materiel_policy_check scripted_trigger to the potential_country block (or create it if it doesn't exist)