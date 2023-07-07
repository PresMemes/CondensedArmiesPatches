# How to make a patch for Condensed Armies
This guide will assume:
1. You know how to mod Stellaris. (Required)
2. How to run Python scripts. (Optional, but heavily recommended)

If you do not know how to mod Stellaris, I'd recommend starting with the [Modding Tutorial](https://stellaris.paradoxwikis.com/Modding_tutorial).

Table of Contents:
  - Patching With Python (Recommended)
    - Localisation
  - Patching Manually

# Patching with Python (Recommended)
**Required: Python 3.8.10 or Later**

First things first, download `pmca_generator.py` and extract it wherever. `pmca_locmaker.py` is not required but highly recommended so you don't need to manually type every line of loc yourself.

Create one (1) new file where you extracted the Python scripts called input.txt.

`pmca_generator.py` will generate three (3) new .txt files after running: pmca_post_insert_defs.txt, pmca_ten_defs.txt, and pmca_hundred_defs.txt.

Paste whatever mod's armies you want to patch inside input.txt.
For maximum safety, make sure to remove commented-out code when possible as it may confuse the script.

Then run `pmca_generator.py`, and viola: You (should) have all the armies generated and fully functioning (except for localisation).
Now do a quick check of your x10 and x100 armies and make sure nothing is broken.

<details>
  
<summary>Editing pmca_post_insert_defs.txt</summary>

If you need to, you can directly edit pmca_post_insert_defs.txt as that's where the x10/x100 script will read from. To do so, open `pmca_generator.py` and comment out the following line:

```py
pmca_automater = pmca_generate_defs()
pmca_automater.insert_pmca_army_defs()
pmca_automater.multiply_values_by_ten()
pmca_automater.multiply_values_by_hundred()
```
↓↓↓
```py
pmca_automater = pmca_generate_defs()
# pmca_automater.insert_pmca_army_defs()
pmca_automater.multiply_values_by_ten()
pmca_automater.multiply_values_by_hundred()
```

Afterwards, just run the file like normal and any changes you make won't get deleted.

</details>

Firstly, I recommend CTRL + F `# PMCA_GEN:` as that's where the script couldn't find an existing property and generated it on its own, and will probably be where it messed up.

After that, CTRL + F `pmca_materiel_policy_check` and make sure that:

A) PMCA_RESOURCE points towards the most difficult resource to maintain. This is entirely subjective, so there's no issue with picking the "wrong resource"

B) PMCA_VALUE matches PMCA_RESOURCE cost.


And always make sure to actually test the mod in-game!

#### Localisation
Generate your localisation keys in this order:

<army_def>: "REPLACE ME"

<army_def>_plural: "REPLACE ME"

<army_def>_desc: "REPLACE ME"


Leave no empty lines between keys.
You'll have to edit the file itself to change the order or number of keys.
 
 
# Patching Manually
To be honest, it's pretty boring. Just go through every. single. line. and multiply the number by x10/x100. Except for build time and morale damage.
For AI weight, the x10 version should have a 1.5x higher base, with x100 armies having a 2x base. So a vanilla army with an AI weight of 100 should have a weight of 150/200 for x10 and x100 respectively.
