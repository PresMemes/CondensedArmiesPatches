# How to make a patch for Condensed Armies
This guide will assume:
1. You know how to mod Stellaris. (Required)
2. How to run python scripts. (Optional, but heavily recommended)

If you do not know how to mod Stellaris, I'd recommend starting with the [Modding Tutorial](https://stellaris.paradoxwikis.com/Modding_tutorial).

Table of Contents:
  - [Patching With Python (Recommended)](https://github.com/PresMemes/CondensedArmiesPatches/new/main?readme=1#patching-with-python-recommended)
    - [The Imporant Part (Post-Insert)](https://github.com/PresMemes/CondensedArmiesPatches/new/main?readme=1#patching-manually)
    - [Localisation](https://github.com/PresMemes/CondensedArmiesPatches/new/main?readme=1#localisation)
  - [Patching Manually WIP](https://github.com/PresMemes/CondensedArmiesPatches/new/main?readme=1#patching-manually)

# Patching with Python (Recommended)
**Required: Python 3.8.10 or Later, VSCode with CWTools addon**

First things first, download `pmca_main.py`, `pmca_inserter.py`, `pmca_multiplier.py`, and `pmca_locmaker.py` and extract them wherever you want.

Create two (2) new files where you extracted the python scripts called `input.txt` and `output.txt`.

Paste whatever mod's armies you want to patch inside of `input.txt`.
Open `pmca_main.py` and change "acot_" to whatever prefix the mod uses. If the mod doesn't use one, just set to something random like "asbdujhdaw"
```py
InsertOperation = pmca_insertOp("input.txt", "output.txt", False, "acot_")
```
↓ ↓ ↓
```py
InsertOperation = pmca_insertOp("input.txt", "output.txt", False, "giga_")
```
Now run `main.py` and copy the contents of `output.txt` INTO `input.txt`

### The Important Part
Now: Go through the entirety of `input.txt` and make sure nothing is missing or obviously incorrect.
In particular, what you'll usually be fixing some (or all) of the following:
  - Missing pmca_ten_ at the first line of an army definition
  - Missing or incorrect `uses_armynames_from`
  - Missing `potential_country`
  - Missing or incorrect `pmca_materiel_policy_check`
  
Check the below collapsed sections for more details on how to fix them. (Do NOT change the numbers for damage, health, etc)
  
<details><summary>Missing pmca_ten_</summary>
<p>

Sometimes, armies don't have a prefix which will get missed by the script. Simply put `pmca_ten_` in front of the army def. Example below: 
```
riesigerkatzenpanzer_assault = {
```
↓ ↓ ↓
```
pmca_ten_riesigerkatzenpanzer_assault = {
```

</p>
</details>

<details><summary>Missing/incorrect uses_armynames_from</summary>
<p>

If the line `uses_armynames_from` is at the very bottom of an army definition, it was probably added by the script.
If it looks like `uses_armynames_from = some_name` or `some_name` is replaced by the **previous** army, replace `some_name` with the non-condensed army
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

Sometimes, armies don't have a `potential_country` block. Simply insert the following code into the army def:
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

By default, pmca_materiel_policy will pretty much always be wrong. So just change `PMCA_RESOURCE` and `PMCA_VALUE` to something that fits the army.
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
```
↓ ↓ ↓
```py
#InsertOperation.readAndWrite()
MultiplyOperation.readAndWrite()
```
And run `pmca_main.py` again.
Congratulations, you (should) now have the x10 variations of some modded armies! Now, copy and paste `output.txt` into `input.txt` AND your x10 army file in your mod.

Run `pmca_main.py` again, and copy `output.txt` to your x100 army file.


#### Localisation
 1. Copy CWtools auto-generated missing loc into `input.txt`
 2. Run `pmca_locmaker.py` NOT `pmca_main.py`
 3. Copy `output.txt` to your .yml file
 
 
# Patching manually
tl;dr, multiply numbers by 10/100, and add missing stuff. Check the collapsed sections for stuff to add in.
TODO: Write this
