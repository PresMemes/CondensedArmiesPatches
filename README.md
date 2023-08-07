# How to make a patch for Condensed Armies
This guide will assume:
1. You know how to mod Stellaris. (Required)
2. How to run Python scripts. (Optional, but heavily recommended)

If you do not know how to mod Stellaris, I'd recommend starting with the [Modding Tutorial](https://stellaris.paradoxwikis.com/Modding_tutorial).

# Patching with Python (Recommended)
**Required: Python 3.8.10 or Later**

1. Download pmca_generator.py.

2. In the same directory as pmca_generator.py, create a new file named input.txt.

3. Inside the input.txt file, paste all the army definitions that you want patches.

4. Open a terminal/command prompt, navigate to the directory containing pmca_generator.py, and execute the program using the following command:
```bash
python pmca_generator.py
```
5. After running the program, you will be prompted to input a custom file name. This name will be used to generate the following file structure in the PMCA_GEN_OUTPUT directory:
```
PMCA_GEN_OUTPUT/
├─ common/
│  ├─ armies/
│  │  ├─ <custom_file_name>_x10_armies.txt
│  │  ├─ <custom_file_name>_x100_armies.txt
├─ localisation/
│  ├─ <custom_file_name>_l_braz_por.yml
│  ├─ <custom_file_name>_l_english.yml
│  ├─ <custom_file_name>_l_french.yml
│  ├─ <custom_file_name>_l_german.yml
│  ├─ <custom_file_name>_l_japanese.yml
│  ├─ <custom_file_name>_l_korean.yml
│  ├─ <custom_file_name>_l_polish.yml
│  ├─ <custom_file_name>_l_russian.yml
│  ├─ <custom_file_name>_l_simp_chinese.yml
│  ├─ <custom_file_name>_l_spanish.yml

```
Note: `<custom_file_name>` will be replaced by whatever you input, or `REPLACE_ME` if no input is given.
Also, please avoid naming your file `pmca_<mod_name>` as that is what I usually name my files.

6. After the main script finishes, you might be prompted with a Y/N question about seeing unbuildable armies or armies that shouldn't be condensed. You can ignore them if you wish, but I wouldn't recommend it.
    * Another Y/N prompt will appear after you enter Y to explain the warnings.


#### Input sanitization
<details>
<summary>Weird Formatting</summary>
If the script is acting weird, try formatting the armies similar to how PDS does it (Shift + Alt + F with VSCode + CWTools)
</details>

<details>
<summary>Empty Resource Tables</summary>

```
resources = {
  category = armies
  cost = {

  }
  upkeep = {
    energy = 10
  }
}
```
The empty cost block WILL screw the entire table up, as the script assumes each sub block (cost, upkeep, produces) contains at least one `resource = value` set.

</details>


#### Script clean-up
The script is usually pretty good at it, but just in case.
* CTRL + F `pmca_materiel_policy_check` and make sure that:
  * `PMCA_RESOURCE` points towards the most difficult resource to maintain. This is entirely subjective, so there's no issue with picking the "wrong resource"
  * `PMCA_VALUE` matches `PMCA_RESOURCE` cost.
    * Resources in triggered cost blocks should be ignored, but it's your choice.

And always make sure to actually test the mod in-game!

# Patching Manually
To be honest, it's pretty dull.

Delete army if it's unbuildable or does anything with variables
Multiply everything (except build_time and morale_damage) by x10
Do it again, then do localisation.

please just use the python script, life's too short to waste a few hours adding 0 to a bunch of numbers.