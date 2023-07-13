# How to make a patch for Condensed Armies
This guide will assume:
1. You know how to mod Stellaris. (Required)
2. How to run Python scripts. (Optional, but heavily recommended)

If you do not know how to mod Stellaris, I'd recommend starting with the [Modding Tutorial](https://stellaris.paradoxwikis.com/Modding_tutorial).

Table of Contents:
  - Patching With Python (Recommended)
  - Patching Manually

# Patching with Python (Recommended)
**Required: Python 3.8.10 or Later**

1. Download `pmca_generator.py` and extract it wherever, then create a new file called `input.txt` (An example input.txt has been provided if you want to see how it should look)
2. Paste the army definitions that you want to patch inside `input.txt`
3. Run `pmca_generator.py` and enter a custom mod prefix (or leave it blank) and press enter. A new folder with the following file structure should be visible (replace pmca with your prefix):
```
PMCA_GEN_OUTPUT/
├─ common/
│  ├─ armies/
│  │  ├─ 01_pmca_ten_defs.txt
│  │  ├─ 02_pmca_hundred_defs.txt
├─ localisation/
│  ├─ pmca_l_braz_por.yml
│  ├─ pmca_l_english.yml
│  ├─ pmca_l_french.yml
│  ├─ pmca_l_german.yml
│  ├─ pmca_l_japanese.yml
│  ├─ pmca_l_korean.yml
│  ├─ pmca_l_polish.yml
│  ├─ pmca_l_russian.yml
│  ├─ pmca_l_simp_chinese.yml
│  ├─ pmca_l_spanish.yml
├─ 00_pmca_post_insert_defs.txt
```

### What types of armies shouldn't be condensed? ###
- Anything that involves variables
- Unbuildable Armies (i.e event spawn armies)
- Defensive Armies are your choice tbh, I personally don't but the script doesn't care either way

### Comments, Ignored lines, and editing post_insert_defs ###
PLEASE make sure to delete any commented-out lines with braces in them! The script does NOT ignore them and can cause massive issues.

Otherwise, the script will try to ignore any lines that start with a `#`. But if you want it to ignore a certain line, include `# PMCA_GEN: IGNORE` at the end of the line and the script should skip it.

If you want to edit `00_pmca_post_insert_defs.txt` after running the script (as that's what the x10 and x100 scripts use), comment out `pmca_automater.insert_pmca_army_defs()` around line 1102. 


## Script clean-up

* Firstly, I recommend CTRL + F `# PMCA_GEN:` as that's where the script couldn't find an existing property and generated it on its own, and will probably be where it messed up.

* After that, CTRL + F `pmca_materiel_policy_check` and make sure that:

  * `PMCA_RESOURCE` points towards the most difficult resource to maintain. This is entirely subjective, so there's no issue with picking the "wrong resource"

  * `PMCA_VALUE` matches `PMCA_RESOURCE` cost.


And always make sure to actually test the mod in-game!

## Localisation
Check the `localisation` folder inside `PMCA_GEN_OUTPUT`
 
 
# Patching Manually
To be honest, it's pretty dull. Just go through every. single. line. and multiply the number by x10/x100, except for build time and morale damage.
For AI weight, the x10 version should have a 1.5x higher base, with x100 armies having a 2x base. So a vanilla army with an AI weight of 100 should have a weight of 150/200 for x10 and x100 respectively.
