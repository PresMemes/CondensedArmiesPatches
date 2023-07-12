import re
import os
import time


class pmca_generate_defs:
    input_file_name = "input.txt"
    post_insert_path = "PMCA_GEN_OUTPUT/00_pmca_post_insert_defs.txt"
    x10_path = "PMCA_GEN_OUTPUT/01_pmca_ten_defs.txt"
    x100_path = "PMCA_GEN_OUTPUT/02_pmca_hundred_defs.txt"
    placeholder_loc_path = "PMCA_GEN_OUTPUT/03_pmca_loc_keys_placeholders.txt"
    loc_keys_path = "PMCA_GEN_OUTPUT/04_pmca_loc_keys_complete.txt"

    in_resource_table = False
    in_cost_table = False
    current_resource_name = "food"
    current_resource_value = 0
    # Please fold the dictionary because holy frick URP has a lot of resources
    resource_priority_dict = {
        "food": 0,
        "energy": 1,
        "unity": 2,
        "minerals": 3,
        "consumer_goods": 4,
        "alloys": 6,
        "minor_artifacts": 10,
        "influence": 10,
        "volatile_motes": 7,
        "rare_crystals": 7,
        "exotic_gases": 7,
        "sr_living_metal": 7,
        "sr_zro": 7,
        "sr_dark_matter": 7,
        "nanites": 7,
        "sr_latinum": 7,
        "sr_crew": 7,
        "sr_dilithium": 7,
        "sr_dilithium_raw": 7,
        "sr_dilithium_processed": 7,
        "sr_cpm": 7,
        "sr_ketracel_white": 7,
        "sr_water": 7,
        "sr_brizeen": 7,
        "sr_deuterium": 7,
        "sr_luxuries": 7,
        "sr_cordrazine": 7,
        "sr_duranium": 7,
        "sr_tallonian": 7,
        "sr_kemocite": 7,
        "sr_topaline": 7,
        "sr_magnesite": 7,
        "sr_boronite": 7,
        "sr_time_crystal": 7,
        "sr_trellium": 7,
        "sr_pergium": 7,
        "mec_biotics": 7,
        "vmods_spice": 7,
        "sr_eludium": 7,
        "sr_acean": 7,
        "sr_rad_bloom": 7,
        "sr_tiyanki_parts": 7,
        "sr_strange_matter": 7,
        "sr_quark_gluon_plasma": 7,
        "sr_antimatter": 7,
        "fold_quartz": 7,
        "sr_iodizium": 7,
        "sr_solar_energy": 7,
        "sr_magical_neutronium": 7,
        "sr_psionic_sublimate": 7,
        "ehof_sr_negative_mass": 7,
        "ehof_sr_sentient_metal": 7,
        "giga_sr_amb_megaconstruction": 7,
        "apsr_knowledge": 7,
        "sr_ltd_firaxus_gas": 7,
        "sr_ltd_kiraxus_gas": 7,
        "sr_ltd_firaxus_energy": 7,
        "sr_ltd_neptunium_material": 7,
        "sr_ltd_spaceship_crew": 7,
        "sr_ltd_manpower_crew": 7,
        "sr_ltd_share_energy": 7,
        "sr_ltd_aiko_manju": 7,
        "sr_ltd_planeptunium_energy": 7,
        "sr_ltd_planeptunium_material": 7,
        "mind_club": 7,
        "azur_shippartbox": 7,
        "azur_red_diamond": 7,
        "sr_infinity_stone_soul": 7,
        "sr_infinity_stone_mind": 7,
        "sr_infinity_stone_reality": 7,
        "sr_infinity_stone_power": 7,
        "sr_infinity_stone_time": 7,
        "sr_infinity_stone_space": 7,
        "datealive_crystals": 7,
        "leng_breeder": 7,
        "sr_pantsu": 7,
        "sr_neo": 7,
        "sr_alpha": 7,
        "sr_se": 7,
        "sr_uf": 7,
        "sr_tiberium_green": 7,
        "sr_tiberium_blue": 7,
        "sr_tiberium_liquid": 7,
        "arcane_power_tw": 7,
        "malice": 7,
        "sr_lingli": 7,
        "sr_fuka": 7,
        "esc_psionic_charge": 7,
        "esc_gravitic_anomaly": 7,
        "esc_living_crystal": 7,
        "esc_transdimensional_vortex": 7,
        "esc_enigmatic_energy": 7,
        "components": 7,
        "dilithium": 7,
        "deuterium": 7,
        "crew": 7,
        "latinum": 7,
        "ketracel_white": 7,
        "manpower": 7,
        "kyber_crystals": 7,
        "sr_hongjianjian": 7,
        "sr_mofang": 7,
        "grief_cube": 7,
        "shoujo_army": 7,
        "corechip": 7,
        "gf_core_chip": 7,
        "GF_nyto_collapse_liquid": 7,
        "GF_nyto_mental_fragments": 7,
        "GF_nyto_new_fire_control_unit": 7,
        "GF_nyto_dark_star_core": 7,
        "GF_nyto_training_key": 7,
        "favour": 7,
        "sr_kyber_swgs": 7,
        "sr_tibanna_swgs": 7,
        "sr_tanatonium": 7,
        "aot_sr_runic_power": 7,
        "ngm_order_of_merit": 7,
        "honkai648_energy": 7,
        "sr_strange_matter_LsE": 7,
        "sr_pieces_data_LsE": 7,
        "sr_crystal_adf": 7,
        "sr_parts_adf": 7,
        "sr_jingling": 7,
        "energon": 7,
        "dark_energon": 7,
        "energon_crystals": 7,
        "dark_energon_crystals": 7,
        "techcaches": 7,
        "acot_sr_dark_energy": 7,
        "acot_sr_stellarite": 10,
        "acot_sr_light_matter": 11,
        "acot_sr_bandwidth": 7,
        "acot_sr_essence": 7,
        "sr_carolin_crystals": 7,
        "sr_qingchu": 7,
        "sr_automaton_core": 7,
        "psi_energy": 7,
        "sr_ancient_zpm": 7,
        "sr_goauld_symbiote": 7,
        "sw_credit": 7,
        "private_sector_sw_credit": 7,
        "swua_kyber_crystal": 7,
        "ionized_tibanna_gas": 7,
        "high_quality_tibanna_gas": 7,
        "low_quality_tibanna_gas": 7,
        "swua_energy_cells": 7,
        "blastech_weapons": 7,
        "jedi_robes": 7,
        "sith_robes": 7,
        "fett_dna": 7,
        "clone_troopers": 7,
        "phase_1_armor": 7,
        "phase_2_armor": 7,
        "specialized_clone_armor": 7,
        "at_rt_variants": 7,
        "tx_130_variants": 7,
        "at_te_variants": 7,
        "laat_variants": 7,
        "fett_dna_empire": 7,
        "clone_troopers_empire": 7,
        "imperial_citizen": 7,
        "imperial_uniforms": 7,
        "phase_2_armor_empire": 7,
        "specialized_clone_armor_empire": 7,
        "tx_130_variants_empire": 7,
        "at_rt_variants_empire": 7,
        "at_te_variants_empire": 7,
        "laat_variants_empire": 7,
        "rebel_cells": 7,
        "tx_130_variants_rebellion": 7,
        "at_rt_variants_rebellion": 7,
        "at_te_variants_rebellion": 7,
        "laat_variants_rebellion": 7,
        "fett_dna_ku": 7,
        "clone_troopers_ku": 7,
        "phase_1_armor_ku": 7,
        "specialized_clone_armor_ku": 7,
        "at_rt_variants_ku": 7,
        "tx_130_variants_ku": 7,
        "at_te_variants_ku": 7,
        "laat_variants_ku": 7,
        "dna": 7,
        "biomass": 7,
        "kinetic_ammo": 7,
        "vehicle_chasis": 7,
        "military_equipment": 7,
        "small_arms": 7,
        "able_bodied_recruit": 7,
        "basic_solider": 7,
        "basic_officer": 7,
        "supplies": 7,
        "combustible_mg_fuel": 7,
        "spare_parts": 7,
        "robotic_chasis": 7,
        "light_energy": 7,
        "dark_energy": 7,
        "arcane_energy": 7,
        "fire_energy": 7,
        "water_energy": 7,
        "air_energy": 7,
        "earth_energy": 7,
        "sc_mineral": 7,
        "vespene_gas": 7,
        "plate_armor": 7,
        "gold_coins": 7,
        "mind_energy": 7,
        "xeno_abled_bodies": 7,
        "tc_essences": 7,
        "tc_thaumium": 7,
        "tc_element_shard": 7,
        "tc_void_metal": 7,
        "tc_knowledge_fragment": 7,
        "unkowne_visib": 7,
        "tiber": 7,
        "sr_hypernuclear": 7,
        "sr_muonic_hydrogen": 7,
        "sr_quantanium": 7,
        "sr_dilithium_crystals": 7,
        "sr_quartz_crystals": 7,
        "sr_neutroniumm": 7,
        "sr_garanthiumm": 7,
        "sr_precious_stoness": 7,
        "sr_plastic_metal": 7,
        "sr_satramenee": 7,
        "sr_yuranticc": 7,
        "sr_heliumm": 7,
        "sr_miriumm": 7,
        "sr_waterr": 7,
        "union_core": 7,
        "nanomaterial": 7,
        "hyperfuel": 7,
        "tibanna_gas": 7,
        "ammunition": 7,
        "electronics": 7,
        "bacta": 7,
        "spice": 7,
        "sr_agrocite": 7,
        "sr_kyber": 7,
        "sr_wealth": 7,
        "sr_natural_fuels": 7,
        "sr_actinides": 7,
        "sr_biomass": 7,
        "sr_waste": 7,
        "sr_ice": 7,
        "sr_plastics": 7,
        "sr_electronics": 7,
        "sr_protomatter": 7,
        "sr_comms": 7,
        "sr_logistics": 7,
        "sr_precious_stones": 7,
        "sr_rare_metals": 7,
        "excellent_slave": 7,
        "love_juice": 7,
        "holylight_crystal": 7,
        "sr_christian": 7,
        "sr_ten": 7,
        "sr_beauty": 7,
        "automatic_drone": 7,
        "treasures": 7,
        "anti_matter": 7,
        "sr_null": 7,
        "power": 7,
        "evm_components": 7,
        "weapons_components": 7,
        "vsp_components": 7,
        "pol_components": 7,
        "hyper_fuel": 7,
        "sr_nomadic_population": 7,
        "AL_magi_crystal": 7,
        "AL_magi_crystal_core": 7,
        "AL_magi_alloy": 7,
        "AL_faith_num": 7,
        "AL_arsenal_shop_coin": 7,
        "AL_lily_diary": 7,
        "AL_magic_bullet": 7,
        "sr_khaydarin_pylon": 7,
        "sr_terrazine": 7,
        "sr_blood": 7,
        "sm_sr_perfect_runic_energy": 7,
        "originiums": 7,
        "d32_steels": 7,
        "multipole_nanosheets": 7,
        "arkseaborn_cells": 7,
        "sr_investment": 7,
        "medicine": 7,
        "sr_warped_matter": 7,
        "larva": 7,
        "diplodrugs": 7,
        "diploforce": 7,
        "empy_exotic_matter": 7,
        "manacite": 7,
        "unfertilized_eggs": 7,
        "fertilized_eggs": 7,
        "riggan": 7,
        "sr_light_gases": 7,
        "sr_natural_liquids": 7,
        "sr_lythuric": 7,
        "sr_engos": 7,
        "sr_teldar": 7,
        "sr_pitharan": 7,
        "sr_orillium": 7,
        "sr_betharian": 7,
        "sr_alien_pets": 7,
        "gpm_arcane_technology": 7,
        "sr_GAPS_psychic_power": 7,
        "sr_GAPS_water": 7,
        "honkai_energy": 7,
        "zzzZaath_Resources": 7,
        "Zdecadence": 7,
        "ZPsionicPower": 7,
        "hfe_sr_micro_robots": 7,
        "sr_energybottle": 7,
        "sr_ocoin": 7,
        "salt_crystals": 7,
        "sweets": 7,
        "clean_coal": 7,
        "fossil_fuels": 7,
        "polution": 7,
        "toys": 7,
        "rare_minerals": 7,
        "gold": 7,
        "military_electronics": 7,
        "grief_seed": 7,
        "sr_megalogistic": 7,
        "uploaded_pops": 7,
        "cybernewtypes": 7,
        "efsf_pilots": 7,
        "efsf_ace_pilots": 7,
        "luna_titanium": 7,
        "mobile_suits": 7,
        "newtypes": 7,
        "zeon_pilots": 7,
        "zeon_ace_pilots": 7,
        "luminescent_ferns": 7,
        "rlc_raw_material": 7,
        "rlc_light_substance": 7,
        "rlc_machine_part": 7,
        "rlc_electronic_component": 7,
        "rlc_fuel": 7,
        "rlc_pharmaceuticals": 7,
        "rlc_alloys": 7,
        "rlc_advanced_part": 7,
        "rlc_advanced_fuel": 7,
        "Tasrydine": 7,
        "stable_antimatte": 7,
        "Adamantium": 7,
        "dsa_paperclips": 7,
        "commercial_materials": 7,
        "magic_crystals": 7,
        "spacemonster_supertissue": 7,
        "tiyanki_milk": 7,
        "sr_hydrogen": 7,
        "sr_helium_3": 7,
        "sr_carbon": 7,
        "sr_ammonia": 7,
        "sr_oxygen": 7,
        "sr_noble_gases": 7,
        "sr_silicon": 7,
        "sr_transition_metals": 7,
        "sr_rare_earth_metals": 7,
        "stella_grief_cube": 7,
        "SE_strange_matter": 7,
        "sr_hypermatter": 7,
        "sr_tibanna_gas": 7,
        "sr_laser_cells": 7,
        "sr_plasma_cells": 7,
        "sr_ordnance": 7,
        "sr_starfighter_parts": 7,
        "sr_hyperfuel": 7,
        "sr_focus": 7,
        "sr_bacta": 7,
        "sr_sw_spice": 7,
        "sr_kyber": 7,
        "yin": 7,
        "sr_mat_lv_exotic_fauna": 7,
        "sr_WL_lv_exotic_fauna": 7,
        "virtue": 7,
        "ancient_knowldege": 7,
        "ambrosia": 7,
        "eternium": 7,
        "void_matter": 7,
        "machinedlc_processing_capacity": 7,
        "machinedlc_processing_demand": 7,
        "planetary_industry_equipments": 7,
        "rift_matter": 7,
        "resource_starcore": 7,
        "resource_illunia": 7,
        "sr_paperclips": 7,
        "sr_waaagh": 7,
        "life_tree_seed": 7,
        "sr_stellar_plasma": 7,
        "helium_3": 7,
        "hydrogen": 7,
        "element_zero": 7,
        "iridium": 7,
        "platinum": 7,
        "palladium": 7,
        "hive_worm": 7,
        "cabal_oil": 7,
        "vex_radiolaria": 7,
        "fallen_ether": 7,
        "scorn_dark_ether": 7,
        "ichor_green_crystals": 7,
        "ichor_blue_crystals": 7,
        "ichor_green": 7,
        "ichor_blue": 7,
        "sr_rosa_mystica": 7,
        "sr_void_core": 7,
        "helium": 7,
        "sr_kancolle_material": 7,
        "sr_kancolle_repair": 7,
        "sr_kancolle_renovate": 7,
        "sr_kancolle_build": 7,
        "sr_void_energy": 7,
        "sr_coffee": 7,
        "sr_coffee_beans": 7,
        "dave_bucks": 7,
        "pvza_brain": 7,
        "pvza_sun": 7,
        "ls_soul_crystals": 7,
        "sentm": 7,
        "cruelsanity": 7,
        "cruelpain": 7,
        "cruelsuffering": 7,
        "cruelagony": 7,
        "crueldespair": 7,
        "cruelannihilation": 7,
        "cruel_red_giga_mass": 7,
        "uma_threegodness_knowledge": 7,
        "uma_crystal_carrot": 7,
        "gs_premium_currency": 7,
        "gs_freemium_currency": 7,
        "sr_N_ISBS_DWP": 7,
        "seeds": 7,
        "greenhouse_gases": 7,
        "water_ices": 7,
        "sr_grox_metal": 7,
        "sr_spice": 7,
        "sr_ixian": 7,
        "sr_mentats": 7,
        "sr_truthsayers": 7,
        "sr_tleilaxu": 7,
        "sr_guild": 7,
        "sr_sardaukar": 7,
        "sr_swordmasters": 7,
        "sr_elacca": 7,
        "sr_suk": 7,
        "sxx_stones": 7,
        "sxx_pills": 7,
        "sxx_gongfa": 7,
        "sxx_qiyun": 7,
        "sr_pyroxenes": 7,
        "sr_keystone": 7,
        "sr_starlight_stone": 7,
        "sr_clea": 7,
        "SG_shine": 7,
        "originium": 7,
        "originiumunit": 7,
        "exo_triiodide": 7,
        "exo_vantablack": 7,
        "exo_gallium": 7,
        "exo_plutonium": 7,
        "exo_adamantite": 7,
        "exo_administrantium": 7,
        "exo_coaxium": 7,
        "exo_hyperion": 7,
        "exo_dust": 7,
        "exo_stalinium": 7,
        "exo_kruppstahl": 7,
        "exo_tachyon": 7,
        "darkness_resonance": 7,
        "ad_mana": 7,
        "ad_hellfire": 7,
        "cr_phase_phasewave_matter": 7,
        "cr_phase_phasewave_energy": 7,
        "sr_meds": 7,
        "sr_isotope5": 7,
        "fuel": 7,
        "sr_heavy_alloys": 7,
        "gundarium": 7,
        "mobile_frame": 7,
        "sr_regenex": 7,
        "mana_crystals": 7,
        "arcane_technology": 7,
        "arcane_insights": 7,
        "ecocontinuity": 7,
        "sr_semen": 7,
        "sr_elemental_crystal": 7,
        "sr_pantyhose_slave": 7,
        "sr_semen_ten": 7,
        "sr_live_pantyhose": 7,
        "sr_pantyhose_sister": 7,
        "sr_theta": 7,
        "sr_st": 7,
        "mtp_tanatnim": 7,
        "mtp_elementenzyme": 7,
        "mtp_soulence": 7,
        "ukn_neutronium": 7,
        "ukn_electroweak_matter": 7,
        "ukn_quasi_matter": 7,
        "ukn_exotic_matter": 7,
        "ukn_exions": 7,
        "ukn_e3z0": 7,
        "ukn_tachyons": 7,
        "urp_000": 7,
        "urp_000": 7,
        "urp_001": 7,
        "urp_002": 7,
        "urp_003": 7,
        "urp_004": 7,
        "urp_005": 7,
        "urp_006": 7,
        "urp_007": 7,
        "urp_008": 7,
        "urp_009": 7,
        "urp_010": 7,
        "urp_011": 7,
        "urp_012": 7,
        "urp_013": 7,
        "urp_014": 7,
        "urp_015": 7,
        "urp_016": 7,
        "urp_017": 7,
        "urp_018": 7,
        "urp_019": 7,
        "urp_020": 7,
        "urp_021": 7,
        "urp_022": 7,
        "urp_023": 7,
        "urp_024": 7,
        "urp_025": 7,
        "urp_026": 7,
        "urp_027": 7,
        "urp_028": 7,
        "urp_029": 7,
        "urp_030": 7,
        "urp_031": 7,
        "urp_032": 7,
        "urp_033": 7,
        "urp_034": 7,
        "urp_035": 7,
        "urp_036": 7,
        "urp_037": 7,
        "urp_038": 7,
        "urp_039": 7,
        "urp_040": 7,
        "urp_041": 7,
        "urp_042": 7,
        "urp_043": 7,
        "urp_044": 7,
        "urp_045": 7,
        "urp_046": 7,
        "urp_047": 7,
        "urp_048": 7,
        "urp_049": 7,
        "urp_050": 7,
        "urp_051": 7,
        "urp_052": 7,
        "urp_053": 7,
        "urp_054": 7,
        "urp_055": 7,
        "urp_056": 7,
        "urp_057": 7,
        "urp_058": 7,
        "urp_059": 7,
        "urp_060": 7,
        "urp_061": 7,
        "urp_062": 7,
        "urp_063": 7,
        "urp_064": 7,
        "urp_065": 7,
        "urp_066": 7,
        "urp_067": 7,
        "urp_068": 7,
        "urp_069": 7,
        "urp_070": 7,
        "urp_071": 7,
        "urp_072": 7,
        "urp_073": 7,
        "urp_074": 7,
        "urp_075": 7,
        "urp_076": 7,
        "urp_077": 7,
        "urp_078": 7,
        "urp_079": 7,
        "urp_080": 7,
        "urp_081": 7,
        "urp_082": 7,
        "urp_083": 7,
        "urp_084": 7,
        "urp_085": 7,
        "urp_086": 7,
        "urp_087": 7,
        "urp_088": 7,
        "urp_089": 7,
        "urp_090": 7,
        "urp_091": 7,
        "urp_092": 7,
        "urp_093": 7,
        "urp_094": 7,
        "urp_095": 7,
        "urp_096": 7,
        "urp_097": 7,
        "urp_098": 7,
        "urp_099": 7,
        "urp_100": 7,
        "urp_101": 7,
        "urp_102": 7,
        "urp_103": 7,
        "urp_104": 7,
        "urp_105": 7,
        "urp_106": 7,
        "urp_107": 7,
        "urp_108": 7,
        "urp_109": 7,
        "urp_110": 7,
        "urp_111": 7,
        "urp_112": 7,
        "urp_113": 7,
        "urp_114": 7,
        "urp_115": 7,
        "urp_116": 7,
        "urp_117": 7,
        "urp_118": 7,
        "urp_119": 7,
        "urp_120": 7,
        "urp_121": 7,
        "urp_122": 7,
        "urp_123": 7,
        "urp_124": 7,
        "urp_125": 7,
        "urp_126": 7,
        "urp_127": 7,
        "urp_128": 7,
        "urp_129": 7,
        "urp_130": 7,
        "urp_131": 7,
        "urp_132": 7,
        "urp_133": 7,
        "urp_134": 7,
        "urp_135": 7,
        "urp_136": 7,
        "urp_137": 7,
        "urp_138": 7,
        "urp_139": 7,
        "urp_140": 7,
        "urp_141": 7,
        "urp_142": 7,
        "urp_143": 7,
        "urp_144": 7,
        "urp_145": 7,
        "urp_146": 7,
        "urp_147": 7,
        "urp_148": 7,
        "urp_149": 7,
        "urp_150": 7,
        "urp_151": 7,
        "urp_152": 7,
        "urp_153": 7,
        "urp_154": 7,
        "urp_155": 7,
        "urp_156": 7,
        "urp_157": 7,
        "urp_158": 7,
        "urp_159": 7,
        "urp_160": 7,
        "urp_161": 7,
        "urp_162": 7,
        "urp_163": 7,
        "urp_164": 7,
        "urp_165": 7,
        "urp_166": 7,
        "urp_167": 7,
        "urp_168": 7,
        "urp_169": 7,
        "urp_170": 7,
        "urp_171": 7,
        "urp_172": 7,
        "urp_173": 7,
        "urp_174": 7,
        "urp_175": 7,
        "urp_176": 7,
        "urp_177": 7,
        "urp_178": 7,
        "urp_179": 7,
        "urp_180": 7,
        "urp_181": 7,
        "urp_182": 7,
        "urp_183": 7,
        "urp_184": 7,
        "urp_185": 7,
        "urp_186": 7,
        "urp_187": 7,
        "urp_188": 7,
        "urp_189": 7,
        "urp_190": 7,
        "urp_191": 7,
        "urp_192": 7,
        "urp_193": 7,
        "urp_194": 7,
        "urp_195": 7,
        "urp_196": 7,
        "urp_197": 7,
        "urp_198": 7,
        "urp_199": 7,
        "urp_200": 7,
        "urp_201": 7,
        "urp_202": 7,
        "urp_203": 7,
        "urp_204": 7,
        "urp_205": 7,
        "urp_206": 7,
        "urp_207": 7,
        "urp_208": 7,
        "urp_209": 7,
        "urp_210": 7,
        "urp_211": 7,
        "urp_212": 7,
        "urp_213": 7,
        "urp_214": 7,
        "urp_215": 7,
        "urp_216": 7,
        "urp_217": 7,
        "urp_218": 7,
        "urp_219": 7,
        "urp_220": 7,
        "urp_221": 7,
        "urp_222": 7,
        "urp_223": 7,
        "urp_224": 7,
        "urp_225": 7,
        "urp_226": 7,
        "urp_227": 7,
        "urp_228": 7,
        "urp_229": 7,
        "urp_230": 7,
        "urp_231": 7,
        "urp_232": 7,
        "urp_233": 7,
        "urp_234": 7,
        "urp_235": 7,
        "urp_236": 7,
        "urp_237": 7,
        "urp_238": 7,
        "urp_239": 7,
        "urp_240": 7,
        "urp_241": 7,
        "urp_242": 7,
        "urp_243": 7,
        "urp_244": 7,
        "urp_245": 7,
        "urp_246": 7,
        "urp_247": 7,
        "urp_248": 7,
        "urp_249": 7,
        "urp_250": 7,
        "urp_251": 7,
        "urp_252": 7,
        "urp_253": 7,
        "urp_254": 7,
        "urp_255": 7,
    }

    pmca_scripted_trigger_block = ""
    seen_potential_country_block = False

    brace_count_updated = False
    num_isolated_braces = 0

    army_def_name = "PLACEHOLDER_ARMY_PLEASE_REPLACE_ME"
    seen_use_armynames_from = False

    army_def_list = []

    replacement_patterns = {
        "NOT = { has_authority = auth_machine_intelligence }": "is_machine_empire = no",
        "has_authority = auth_machine_intelligence": "is_machine_empire = yes",
        "NOT = { has_authority = auth_hive_mind }": "is_hive_empire = no",
        "has_authority = auth_hive_mind": "is_hive_empire = yes",
        "NOT = { has_ethic = ethic_gestalt_consciousness }": "is_gestalt = no",
        "has_ethic = ethic_gestalt_consciousness": "is_gestalt = yes",
    }

    # Change a variable whenever we see a brace
    def update_brace_count(self, input_line, reset_seen_blocks):
        if not reset_seen_blocks:
            if "{" in input_line:
                self.num_isolated_braces += 1
            if "}" in input_line:
                self.num_isolated_braces -= 1
                self.in_cost_table = False
        elif self.num_isolated_braces == 0:
            self.seen_use_armynames_from = False
            self.seen_potential_country_block = False
            self.current_resource_name = "food"
            self.current_resource_value = 0

        if self.num_isolated_braces == 1:
            self.in_resource_table = False

    # Save the army def for later if needed, and prepend pmca_ten_ to the line
    def fetch_army_def_and_prepend(self, input_line):
        if (
            self.num_isolated_braces == 1
            and "= {" in input_line
            and "}" not in input_line
            and "pmca_ten" not in input_line
            and "pmca_hundred" not in input_line
        ):
            self.army_def_name = re.match(r"\w+", input_line).group(0)
            self.army_def_list.append(self.army_def_name)
            return "pmca_ten_" + input_line.strip() + " # PMCA_GEN: Inserted prefix\n"

        return input_line

    # Return a int for output when given a line, meant for inserting the pmca_materiel_policy_check scripted_trigger
    def insert_materiel_policy_check(self, input_line):
        if "potential_country = {" in input_line:
            self.seen_potential_country_block = True
            if "}" in input_line:
                return -1
            else:
                return 1

        return 0

    # Try to update the cost of an army for later
    def update_army_costs(self, input_line):
        clean_string = input_line.strip()
        match_value = re.match(r"[^ ]*", clean_string).group(0)
        if (
            self.resource_priority_dict[match_value]
            > self.resource_priority_dict[self.current_resource_name]
        ):
            self.current_resource_name = match_value
            self.current_resource_value = self.convert_list(
                re.findall(r"\d+(?:\.\d+)?", input_line), False
            )

    # Convert input_list into a float then return it as a string
    def convert_list(self, input_list, multiply):
        output = float(input_list[0])
        if multiply:
            output *= 10
        return str(output)

    def convert_to_scripted_trigger(self, input_string):
        for pattern, replacement in self.replacement_patterns.items():
            input_string = input_string.replace(pattern, replacement)
        return input_string

    # If the line has PMCA_GEN: IGNORE || starts with a #, return false
    def should_read_line(self, input_line):
        return (
            "PMCA_GEN: IGNORE" not in input_line
            and input_line.strip()
            and input_line.strip()[0] != "#"
        )

    def insert_pmca_army_defs(self):
        insert_notification = True
        with open(self.input_file_name, "r") as file_input, open(
            self.post_insert_path, "w"
        ) as file_output:
            for line in file_input:
                string_to_output = line
                self.update_brace_count(line, False)
                if self.should_read_line(string_to_output):
                    string_to_output = self.fetch_army_def_and_prepend(line)

                    string_to_output = self.convert_to_scripted_trigger(
                        string_to_output
                    )

                    if "resources = {" in line:
                        self.in_resource_table = True
                    if (
                        "cost = {" in line
                        and "}" not in line
                        and self.in_resource_table
                    ):
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
                    match_value = self.insert_materiel_policy_check(string_to_output)
                    if match_value == 1:
                        file_output.write(string_to_output)
                        string_to_output = ""
                        file_output.write(self.pmca_scripted_trigger_block + "\n")
                    elif match_value == -1:
                        string_to_output = ""
                        nested_string = self.convert_to_scripted_trigger(
                            re.search(r"\{ (.*?) \}\n", line).group(0).strip()[2:-2]
                        )
                        file_output.write(
                            "    potential_country = { # PMCA_GEN: Modified trigger block, probably was a nested 1-line statement\n"
                        )
                        file_output.write(self.pmca_scripted_trigger_block + "\n")
                        file_output.write("        " + nested_string + "\n")
                        file_output.write("    }\n")
                    else:
                        pass

                    if (
                        self.num_isolated_braces == 0
                        and not self.seen_potential_country_block
                        and "}" in string_to_output
                    ):
                        file_output.write(
                            "    potential_country = { # PMCA_GEN: No potential_country detected, inserted best guess\n"
                        )
                        file_output.write(self.pmca_scripted_trigger_block)
                        file_output.write("    }\n")

                    # Create use_armynames_from if it doesn't exist
                    if "use_armynames_from" in line:
                        self.seen_use_armynames_from = True
                    if (
                        self.num_isolated_braces == 0
                        and not self.seen_use_armynames_from
                        and "}" in line
                    ):
                        file_output.write(
                            "    use_armynames_from = "
                            + self.army_def_name
                            + " # PMCA_GEN: No use_armynames_from detected, inserted best guess\n"
                        )

                self.update_brace_count(string_to_output, True)
                if insert_notification:
                    file_output.write(
                        "# PMCA_GEN: Army definitions patched using python, please check for errors\n"
                    )
                    insert_notification = False

                file_output.write(string_to_output)

    # Does input_line have a int/float?
    def has_number(self, input_line):
        return bool(re.search(r"\d", input_line))

    # What lines should the script multiply numbers in?
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
    def handle_ai_base(self, input_value, is_hundred):
        output = float(input_value)
        if is_hundred:
            output *= 4 / 3
        else:
            output *= 1.5
        return str(output)

    # Get the number in a string and send it to another function for multiplying
    # PM: So, the lambda match is getting a group from re.sub? That's my only explanation on how this shit works tbh, ChatGPT is wildin
    def factor_number_in_string(self, input_line, is_hundred):
        if "base" in input_line:
            return re.sub(
                r"\d+(?:\.\d+)?",
                lambda match: self.handle_ai_base(match.group(0), is_hundred),
                input_line,
            )
        else:
            return re.sub(
                r"\d+(?:\.\d+)?",
                lambda match: self.convert_list([match.group(0)], True),
                input_line,
            )

    def multiply_values_by_ten(self):
        with open(self.post_insert_path, "r") as file_input, open(
            self.x10_path, "w"
        ) as file_output:
            for line in file_input:
                self.update_brace_count(line, False)
                if self.should_read_line(line):
                    if "resources = {" in line:
                        self.in_resource_table = True
                    if self.valid_lines_to_multiply(line) and self.has_number(line):
                        line = self.factor_number_in_string(line, False)
                self.update_brace_count(line, True)
                file_output.write(line)

    def multiply_values_by_hundred(self):
        with open(self.x10_path, "r") as file_input, open(
            self.x100_path, "w"
        ) as file_output:
            for line in file_input:
                self.update_brace_count(line, False)
                if self.should_read_line(line):
                    if "resources = {" in line:
                        self.in_resource_table = True
                    if self.valid_lines_to_multiply(line) and self.has_number(line):
                        line = self.factor_number_in_string(line, True)
                    line = line.replace("PMCA_MULT = ten", "PMCA_MULT = hundred")
                    line = line.replace("pmca_ten_", "pmca_hundred_")
                self.update_brace_count(line, True)
                file_output.write(line)

    def generate_placeholder_loc_keys(self):
        with open(self.placeholder_loc_path, "w") as file_output:
            for key in self.army_def_list:
                file_output.write(f'pmca_ten_{key}: "REPLACE_ME"\n')
                file_output.write(f'pmca_ten_{key}_plural: "REPLACE_ME"\n')
                file_output.write(f'pmca_ten_{key}_desc: "REPLACE_ME"\n')
            for key in self.army_def_list:
                file_output.write(f'pmca_hundred_{key}: "REPLACE_ME"\n')
                file_output.write(f'pmca_hundred_{key}_plural: "REPLACE_ME"\n')
                file_output.write(f'pmca_hundred_{key}_desc: "REPLACE_ME"\n')

    pmcaTen = "$pmca_ten$ "
    pmcaHundred = "$pmca_hundred$ "

    def combineStrings(self, prefix, input_list):
        return str('"' + prefix + "$" + input_list[0] + "$" + '"')

    def complete_loc_keys(self):
        with open(self.placeholder_loc_path, "r") as file_input, open(
            self.loc_keys_path, "w"
        ) as file_output:
            count = 0
            for line in file_input:
                count += 1
                loc_keys = re.findall(r"(?:pmca_ten_|pmca_hundred_)([^:]*)", line)
                if count % 3 == 1:  # Army Name Singular
                    if loc_keys:
                        output_line = re.sub(
                            r'"REPLACE_ME"',
                            self.combineStrings(self.pmcaTen, loc_keys),
                            line,
                        )
                    else:
                        output_line = line
                elif count % 3 == 2:  # Army Name Plural
                    output_line = re.sub(
                        r'"REPLACE_ME"', self.combineStrings("", loc_keys), line
                    )
                else:  # Army Description
                    output_line = re.sub(
                        r'"REPLACE_ME"', self.combineStrings("", loc_keys), line
                    )
                file_output.write(output_line)


start = time.time()
if os.path.isfile("./input.txt"):
    directory = "PMCA_GEN_OUTPUT"
    path = os.path.join(os.getcwd(), directory)
    print(f"Trying to create Directory '{directory}'...")
    try:
        os.mkdir(path)
        print(f"Directory '{directory}' does NOT exist, creating...")
    except OSError as error:
        print(f"Directory '{directory}' exists, continuing...")

    pmca_automater = pmca_generate_defs()

    print("Inserting required army properties...")
    pmca_automater.insert_pmca_army_defs()
    print(f"Number of Army Definitions: {len(pmca_generate_defs.army_def_list)}")

    print("Multiplying values to x10...")
    pmca_automater.multiply_values_by_ten()

    print("Multiplying values to x100...")
    pmca_automater.multiply_values_by_hundred()

    print("Generating placeholder localisation keys...")
    pmca_automater.generate_placeholder_loc_keys()

    print("Replacing placeholder lines with preferred text and format...")
    pmca_automater.complete_loc_keys()

    print(f"Done! Check the Directory '{directory}' for your freshly Condensed Armies!")
else:
    print(
        "ERROR: input.txt does NOT exist! Please create it and put your army definitions inside it."
    )
end = time.time()
print(f"\nTime to complete: {(end - start) * 1000} milliseconds (ms)")
print(
    f"Estimated Time per Army Definition: {((end - start) * 1000) / len(pmca_generate_defs.army_def_list)} milliseconds (ms)"
)
