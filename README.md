# How to make a patch for Condensed Armies
This guide will assume:
1. You know how to mod Stellaris. (Required)
2. How to run Python scripts. (Optional, but heavily recommended)

If you do not know how to mod Stellaris, I'd recommend starting with the [Modding Tutorial](https://stellaris.paradoxwikis.com/Modding_tutorial).

Table of Contents:
  - [Patching With Python (Recommended)](https://github.com/PresMemes/CondensedArmiesPatches/new/main?readme=1#patching-with-python-recommended)
    - [The Important Part (Post-Insert)](https://github.com/PresMemes/CondensedArmiesPatches/new/main?readme=1#patching-manually)
    - [Localisation](https://github.com/PresMemes/CondensedArmiesPatches/new/main?readme=1#localisation)
  - [Patching Manually WIP](https://github.com/PresMemes/CondensedArmiesPatches/new/main?readme=1#patching-manually)

# Patching with Python (Recommended)
**Required: Python 3.8.10 or Later, VSCode with CWTools addon**

First things first, download `pmca_main.py`, `pmca_inserter.py`, `pmca_multiplier.py`, and `pmca_locmaker.py` and extract them wherever you want.

Create two (2) new files where you extracted the Python scripts called `input.txt` and `output.txt`.

Paste whatever mod's armies you want to patch inside `input.txt`.
Now run `main.py` and copy the contents of `output.txt` INTO `input.txt`

### The Important Part
Now: Go through the entirety of `input.txt` and make sure nothing is missing or obviously incorrect.
In particular, what you'll usually be fixing some (or all) of the following:
  - Missing `pmca_ten_` prefix
  - Missing or incorrect `use_armynames_from`
  - Missing `potential_country`
  - Missing or incorrect `pmca_materiel_policy_check`
  
Check the collapsed sections below for more details on how to fix them. (Do NOT change the numbers for damage, health, etc)
  
<details><summary>Missing pmca_ten_ prefix</summary>
<p>

If the script somehow forgets to place it, put `pmca_ten_` in front of the army def. Example below: 
```
riesigerkatzenpanzer_assault = {
```
↓ ↓ ↓
```
pmca_ten_riesigerkatzenpanzer_assault = {
```

</p>
</details>

<details><summary>Missing/incorrect use_armynames_from</summary>
<p>

If the line `use_armynames_from` is at the very bottom of an army definition, it was probably added by the script.
Make sure it points to the non-condensed version of the army.
Example below: 
```
pmca_ten_shroud_summoned_army = {
  <script>
  use_armynames_from = giga_eaw_crystal_army_drone

}
```
↓ ↓ ↓
```
pmca_ten_shroud_summoned_army = {
  <script>
  use_armynames_from = shroud_summoned_army

}
```

</p>
</details>

<details><summary>Missing potential_country</summary>
<p>

Sometimes, armies don't have a `potential_country` block. Insert the following block and make sure it lines up with the actual cost of the army.
```
potential_country = {
  pmca_materiel_policy_check = {
    PMCA_MULT = ten 
    PMCA_RESOURCE = minerals
    PMCA_VALUE = 100
  }
}
```

</p>
</details>

<details><summary>Incorrect pmca_materiel_policy_check</summary>
<p>

By default, pmca_materiel_policy will always assume an army will cost 100 minerals, change what `PMCA_RESOURCE` and `PMCA_VALUE` are to fix this.
Example:
```
cost = {
  alloys = 10000
  exotic_gases = 500
  rare_crystals = 500
  volatile_motes = 500
}
```
In this scenario, I'd pick the alloys as they're (probably) the hardest resource to maintain a high stockpile of.
```
pmca_materiel_policy_check = {
  PMCA_MULT = ten 
  PMCA_RESOURCE = alloys
  PMCA_VALUE = 10000
}
```
Don't be afraid of picking the wrong resource, this is mostly to keep the recruitment UI clean.

</p>
</details>

Now that you've gone through and changed everything to your liking, comment out `InsertOperation.readAndWrite()` and uncomment `MultiplyOperation.readAndWrite()`
```py
InsertOperation.readAndWrite()
#MultiplyOperation.readAndWrite()
#MultiplyOperationp2.readAndWrite()
```
↓ ↓ ↓
```py
#InsertOperation.readAndWrite()
MultiplyOperation.readAndWrite()
#MultiplyOperationp2.readAndWrite()
```
And run `pmca_main.py` again.
Congratulations, you (should) now have the x10 variations of some modded armies! Now, copy and paste `output.txt` into `input.txt` AND your x10 army file in your mod.

Comment out `MultiplyOperation.readAndWrite()` and uncomment `MultiplyOperationp2.readAndWrite()`
```py
#InsertOperation.readAndWrite()
MultiplyOperation.readAndWrite()
#MultiplyOperationp2.readAndWrite()
```
↓ ↓ ↓
```py
#InsertOperation.readAndWrite()
#MultiplyOperation.readAndWrite()
MultiplyOperationp2.readAndWrite()
```
Run `pmca_main.py` again, and copy `output.txt` to your x100 army file.


#### Localisation

 1. Delete all army_def_plural, as the script doesn't handle it at the moment. Also, make sure there are no empty lines in the file.
 2. Copy auto-generated missing loc into `input.txt`
 3. Run `pmca_locmaker.py` by itself
 4. Copy `output.txt` to your .yml file
 
 
# Patching manually
To be honest, it's pretty boring. Just go through every. single. line. and change the value to x10/x100. Except for build time and morale damage. See the above collapsed sections for things to add.
For AI weight, the x10 version should have a 1.5x higher base, with x100 armies having a 2x base. So a vanilla army with an AI weight of 100 should have a weight of 150/200 for x10 and x100 respectively.
