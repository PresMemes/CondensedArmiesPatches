## President Memes' Condensed Armies Automatic Patcher (PMCAAP)
This guide will assume the following:
- [You know how to mod Stellaris](https://stellaris.paradoxwikis.com/Modding_tutorial)
  - At the very minimum, how to modify/create new armies
- How to run Python Scripts


### System Info
Python Version used: 3.10.6


### Limitations
There are some things this script cannot parse:
- Inline Scripts
  - To fix: Replace the inline script with the unwrapped version
- Quotes
  - All quotes are deleted so as not to mess with the inline script Condensed Armies uses, make sure that whatever uses them will work fine without them

### Step-by-Step
1. Download `pmca_generator_v2.py`

2. Create a file called `input.txt` in the same directory as `pmca_generator_v2.py`

3. Run the program using the terminal/command prompt/whatever

4. You'll prompted for two inputs

   4a. `Enter a custom file prefix:` This will be used for the file names.
    - Please refrain from naming your files `pmca_<mod_initials>` as that is the format I use.
    - `my_mod_pmca_<mod_initials>_patch` would be fine, however

   4b. `Enter the mod's id variable:` This is for the conditional inline Condensed Armies uses.
    - If you're making an external patch: press `Enter`
    - If you're making an integrated/internal patch: Please refer to the [Conditional Inlines](#Condensed-Armies'-Conditional-Inline) section for more info

6. After the program is done, you should see a new folder in the directory called `PMCA_GEN_OUTPUT` with all the necessary files to make the armies work

7. If you are prompted with `Some armies were detected as having concerning properties:` enter Y to see which armies in a new file called `pmca_issues.txt`
  6a. These are guidelines, not errors, and be can be ignored if you want.

8. (Optional) Use an on-action to mark your Condensed Armies with the appropriate flag

   7a. If it's a x10 army, `set_army_flag = pmca_times_ten_army`

   7b. If it's a x100 army, `set_army_flag = pmca_times_hundred_army`

#### Condensed Armies' Conditional Inline
Here's an explanation on how they work from TTFTCUTS, who pioneered the method:
> I realised since inlines can be picked by name, which can include scripted variables indirectly, they can be used to fully exclude references to missing things without needing placeholders successfully made our unity job inline not complain about missing bug branch jobs.
Since I already had it set up to not include the modifier block at all when given 0 as the job count, I just multiplied the count by a @has_bug_branch var which is 0 in gigas and 1 in bug branch, suddenly, no modifier block at all without bug branch.
In a simpler sense it can be used to just pick between two inlines with stuff or not directly based on the variable.

Condensed Armies uses this concept with an equation made by MrRoAdd that looks like this:
```
|(((x / x) - 1) / ((0/0) - 1)) - 1|
```
In traditional mathematics, this does not work. However, due to a quirk with the Clausewitz Engine division by zero in inline math will consistently return ((2^32) / (10^5)).
In short: If x is 0, output 0. Otherwise, output 1.

To take advantage of this, you need to make a placeholder scripted_variable from the mod you want to patch (e.g.: `@has_ancient_caches`) which must be set to 0. Then just paste the placeholder's name in when the script asks for an id variable and you should have a bunch of armies that will never be compiled unless the mod they're from is present.
