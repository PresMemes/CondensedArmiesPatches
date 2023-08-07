import re
import time
import os


directory = ".\PMCA_GEN_OUTPUT"
common_folder = os.path.join(directory, "common")
armies_folder = os.path.join(common_folder, "armies")
localisation_folder = os.path.join(directory, "localisation")

list_of_CArmies = []
concerning_CArmies = {}
stellaris_languages = [
    "l_braz_por",
    "l_english",
    "l_french",
    "l_german",
    "l_japanese",
    "l_korean",
    "l_polish",
    "l_russian",
    "l_simp_chinese",
    "l_spanish",
]

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


class CArmy:
    def __init__(
        self,
        script_army_name: str,
        script_damage: str,
        script_health: str,
        script_morale: str,
        script_morale_damage: str,
        script_collateral_damaage: str,
        script_war_exhaustion: str,
        script_build_time: str,
        script_icon: str,
        script_prereqs: str,
        script_ai_weight_base: float=0.0,
        script_show_tech_unlock_if: str="",
        script_potential_country: str="",
        script_potential: str="",
        script_allow: str="",
        script_on_queued: str="",
        script_on_unqueued: str="",
        script_ai_weight_modifiers: str="",
        script_resource_table: str="",
        script_has_species: str="yes",
        script_disband_if_species_lacks_rights: str="yes",
        script_defensive: str="no",
        script_occupation: str="no",
        script_pop_limited: str="yes",
        script_use_armynames_from: str="",
        script_is_pop_spawned: str="no",
    ):
        self.category = ""
        self.sub_block_type = []
        self.trigger_list = []
        self.resource_pairs = []
        self.mult_values = []

        self.persistent_army_name = script_army_name
        self.army_name = script_army_name
        self.defensive = script_defensive
        self.occupation = script_occupation
        self.damage = float(script_damage)
        self.health = float(script_health)

        if not script_morale:
            self.has_morale = False
            self.morale = False
        else:
            self.morale = float(script_morale)
            self.has_morale = True

        if script_morale_damage is None:
            if self.has_morale:
                self.morale_damage = self.morale
            else:
                self.morale_damage = 1.0
        else:
            self.morale_damage = script_morale_damage

        self.collateral_damage = float(script_collateral_damaage)
        self.war_exhaustion = float(script_war_exhaustion)
        self.build_time = script_build_time
        self.icon = script_icon
        self.pop_limited = script_pop_limited
        self.has_species = script_has_species
        self.is_pop_spawned = script_is_pop_spawned
        self.disband_if_species_lacks_rights = script_disband_if_species_lacks_rights
        self.use_armynames_from = script_use_armynames_from if script_use_armynames_from else self.persistent_army_name

        self.prerequisites = script_prereqs if script_prereqs is not None else []

        if script_resource_table:
            self.parse_resource_table(script_resource_table)

        self.show_tech_unlock_if = script_show_tech_unlock_if

        self.potential_country = script_potential_country

        self.potential = script_potential

        self.allow = script_allow

        self.on_queued = script_on_queued

        self.on_unqueued = script_on_unqueued

        self.ai_weight = float(script_ai_weight_base) if script_ai_weight_base else None
        self.ai_weight_conditions = script_ai_weight_modifiers

    def __str__(self):
        allow_one_line = self.allow.replace("\n", " ").replace("\t", "\\t")
        show_tech_unlock_if_one_line = self.show_tech_unlock_if.replace("\n", "").replace("\t", "")
        potential_country_one_line = self.potential_country.replace("\n", "").replace("\t", "")
        potential_one_line = self.potential.replace("\n", "").replace("\t", "")
        on_queued_one_line = self.on_queued.replace("\n", "").replace("\t", "")
        on_unqueued_one_line = self.on_unqueued.replace("\n", "").replace("\t", "")
        ai_weight_conditions_one_line = self.ai_weight_conditions.replace("\n", "").replace("\t", "")

        if self.morale:
            morale_string = f"Morale = {self.morale}"
        else:
            morale_string = f"Has Morale = {self.has_morale}"

        return (
            f"Army Def = {self.army_name}\n"
            f"Health = {self.health}\n"
            f"Damage = {self.damage}\n"
            f"{morale_string}\n"
            f"Morale Damage = {self.morale_damage}\n"
            f"Collateral Damage = {self.collateral_damage}\n"
            f"War Exhaustion = {self.war_exhaustion}\n"
            f"Build Time = {self.build_time}\n"
            f"Icon = {self.icon}\n"
            f"Has Species = {self.has_species}\n"
            f"Disband if no rights = {self.disband_if_species_lacks_rights}\n"
            f"Defensive = {self.defensive}\n"
            f"Occupation = {self.occupation}\n"
            f"Pop Limited = {self.pop_limited}\n"
            f"Prereqs = {self.prerequisites}\n"
            f"Show Tech Unlock If = {{ {show_tech_unlock_if_one_line} }}\n"
            f"Potential Country = {{ {potential_country_one_line} }} \n"
            f"Potential = {{ {potential_one_line} }}\n"
            f"Allow = {{ {allow_one_line} }}\n"
            f"On Queued = {{ {on_queued_one_line} }}\n"
            f"On Unqueued = {{ {on_unqueued_one_line} }}\n"
            f"AI Weight Base = {self.ai_weight}\n"
            f"AI Weight Modifiers = {{ {ai_weight_conditions_one_line} }}\n"
            f"Economic Category = {self.category}\n"
            f"  Resource Subblocks = {self.sub_block_type}\n"
            f"  Subblock Trigger(s) = {self.trigger_list}\n"
            f"  Subblock Resource Pairs = {self.resource_pairs}\n"
            f"  Subblock Multipliers = {self.mult_values}"
        )

    def convert_to_pdscript(self) -> str:
        """Appends all of the class' variables into a string"""

        PDScript_string = ""
        PDScript_string += f"{self.army_name} = {{\n"
        PDScript_string += f"\tuse_armynames_from = {self.use_armynames_from}\n"
        if self.defensive == "yes":
            PDScript_string += f"\tdefensive = yes\n"
        if self.occupation == "yes":
            PDScript_string += f"\toccupation = yes\n"
        PDScript_string += f"\tdamage = {self.damage}\n"
        PDScript_string += f"\thealth = {self.health}\n"
        if self.has_morale:
            PDScript_string += f"\tmorale = {self.morale}\n"
        else:
            PDScript_string += f"\thas_morale = no\n"
        PDScript_string += f"\tmorale_damage = {self.morale_damage}\n"
        PDScript_string += f"\tcollateral_damage = {self.collateral_damage}\n"
        PDScript_string += f"\twar_exhaustion = {self.war_exhaustion}\n"
        PDScript_string += f"\ttime = {self.build_time}\n"
        PDScript_string += f"\ticon = {self.icon}\n"

        if self.pop_limited == "no":
            PDScript_string += f"\tpop_limited = no\n"

        if self.is_pop_spawned == "yes":
            PDScript_string += f"\tis_pop_spawned = yes\n"

        if self.has_species == "no":
            PDScript_string += f"\thas_species  = no\n"

        if self.disband_if_species_lacks_rights == "no":
            PDScript_string += f"\tdisband_if_species_lacks_rights = no\n"

        if self.prerequisites:
            PDScript_string += f"\tprerequisites = {{"
            if len(self.prerequisites) == 1:
                PDScript_string += f' "{self.prerequisites[0]}" }}\n'
            else:
                PDScript_string += "\n" + "\n".join(f'\t\t"{item}"' for item in self.prerequisites)
                PDScript_string += f"\n\t}}\n"

        PDScript_string += self.reconstruct_resource_table()

        if self.show_tech_unlock_if:
            PDScript_string += f"\n\tshow_tech_unlock_if = {{\n"
            PDScript_string += f"\t\t{self.show_tech_unlock_if.strip()}\n"
            PDScript_string += f"\t}}\n"

        if self.potential_country:
            PDScript_string += f"\n\tpotential_country = {{\n"
            PDScript_string += f"\t\t{self.potential_country.strip()}\n"
            PDScript_string += f"\t}}\n"

        if self.potential:
            PDScript_string += f"\n\tpotential = {{\n"
            PDScript_string += f"\t\t{self.potential.strip()}\n"
            PDScript_string += f"\t}}\n"

        if self.allow:
            PDScript_string += f"\n\tallow = {{\n"
            PDScript_string += f"\t\t{self.allow.strip()}\n"
            PDScript_string += f"\t}}\n"

        if self.on_queued:
            PDScript_string += f"\n\ton_queued = {{\n"
            PDScript_string += f"\t\t{self.on_queued.strip()}\n"
            PDScript_string += f"\t}}\n"

        if self.on_unqueued:
            PDScript_string += f"\n\ton_unqueued = {{\n"
            PDScript_string += f"\t\t{self.on_unqueued.strip()}\n"
            PDScript_string += f"\t}}\n"

        if self.ai_weight is not None:
            PDScript_string += f"\n\tai_weight = {{\n"
            PDScript_string += f"\t\tbase = {self.ai_weight}\n"
            if self.ai_weight_conditions:
                PDScript_string += f"\t\t{self.ai_weight_conditions}\n"
            PDScript_string += f"\t}}\n"

        PDScript_string += f"}}\n\n"
        return PDScript_string

    def parse_resource_table(self, input_string: str) -> None:
        """Turns a resource table into variables for later"""

        split_string = input_string.splitlines()
        num_unpaired_braces = 0
        inside_sub_block = False
        seen_trigger_block = False
        trigger_block = []
        type_regex = r"\w+"
        category_regex = r"(\w+)"
        resource_pair_regex = r"(\w+)\s*=\s*(\d+\.?\d*)"
        temp_resource_pairs = None
        seen_mult = False

        # Find the economic category, if it exists
        self.category = get_attribute_value(input_string.strip(), "category", category_regex)

        # Iterate through every line in a resource table to find the subblocks, resource_pairs, mults, etc
        for line in split_string:
            if "{" in line:
                num_unpaired_braces += 1
                if num_unpaired_braces == 2:
                    self.sub_block_type.append(re.match(type_regex, line.strip()).group(0))
                    inside_sub_block = True
                    seen_mult = False
                if num_unpaired_braces == 3:
                    seen_trigger_block = True
            if "}" in line:
                num_unpaired_braces -= 1
                if num_unpaired_braces == 1:
                    if temp_resource_pairs is not None:
                        self.resource_pairs.append(temp_resource_pairs.copy())
                        temp_resource_pairs = None
                    if not seen_mult:
                        self.mult_values.append(0.0)
                    if not seen_trigger_block:
                        self.trigger_list.append(["always = yes"])
                    else:
                        self.trigger_list.append(trigger_block.copy())
                        trigger_block.clear()
                    inside_sub_block = False
                    seen_trigger_block = False

            if inside_sub_block and num_unpaired_braces == 3 and not line.strip().startswith("trigger = {"):
                trigger_block.append(line.strip())

            # Add name = value pair to dictionary, or add it to the mult list
            if inside_sub_block and num_unpaired_braces == 2:
                if re.search(resource_pair_regex, line):
                    match = re.match(resource_pair_regex, line.strip())
                    resource_name = match.group(1)
                    resource_value = match.group(2)
                    if resource_name == "mult" or resource_name == "multiplier":
                        self.mult_values.append(float(resource_value))
                        seen_mult = True
                    else:
                        if temp_resource_pairs is None:
                            temp_resource_pairs = {}
                        temp_resource_pairs[resource_name] = resource_value

        print(self.category)
        print(self.sub_block_type)
        print(self.trigger_list)
        print(self.resource_pairs)
        print(self.mult_values)

    def reconstruct_resource_table(self) -> str:
        """Appends various variables into a string"""

        output = f"\tresources = {{\n\t\tcategory = {self.category}"

        for sub_type, trigger, resource, mult in zip(self.sub_block_type, self.trigger_list, self.resource_pairs, self.mult_values):
            output += f"\n\t\t{sub_type} = {{"

            if len(trigger) >= 1 and trigger != ["always = yes"]:
                output += "\n\t\t\ttrigger = {"
                for line in trigger:
                    output += f"\n\t\t\t\t{line}"
                output += "\n\t\t\t}"

            for key, value in resource.items():
                output += f"\n\t\t\t{key} = {value}"

            if mult != 0.0:
                output += f"\n\t\t\tmultiplier = {mult}"

            output += "\n\t\t}"

        output += "\n\t}\n"
        return output


###########################
### NON-CLASS FUNCTIONS ###
###########################


def scan_input_file() -> None:
    """Scans input.txt for army definitions, then sends every army definition to parse_armies_for_creation"""

    with open("input.txt", "r", encoding="utf-8") as file_input:
        file_contents = file_input.readlines()

    num_isolated_braces = 0
    army_string = ""
    for line in file_contents:
        if should_read_line(line):
            num_isolated_braces += line.count("{")
            num_isolated_braces -= line.count("}")
            army_string += line
            if num_isolated_braces == 0:
                parse_armies_for_creation(army_string)
                army_string = ""


def should_read_line(input_string: str) -> bool:
    """If the given string is empty or starts with a #, return false"""
    return input_string.strip() and not input_string.strip().startswith("#")

def parse_armies_for_creation(input_string: str) -> None:
    """Turn a given string into a CArmy object"""

    number_regex = r"\d+\.?\d*"

    # Get the army def
    scan_army_name = re.match(r"\w+", input_string.strip()).group(0)

    # Extract attributes using regex
    scan_damage = get_attribute_value(input_string, "damage", number_regex)
    scan_health = get_attribute_value(input_string, "health", number_regex)
    scan_morale = get_attribute_value(input_string, "morale", number_regex, default=False)
    scan_morale_damage = get_attribute_value(input_string, "morale_damage", number_regex)
    scan_collateral = get_attribute_value(input_string, "collateral_damage", number_regex)
    scan_war_exhaustion = get_attribute_value(input_string, "war_exhaustion", number_regex)
    scan_time = get_attribute_value(input_string, "time", number_regex)
    scan_icon = get_attribute_value(input_string, "icon", r"\w+")
    scan_defensive = get_attribute_value(input_string, "defensive", r"yes", default="no")
    scan_occupation = get_attribute_value(input_string, "occupation", r"yes", default="no")
    scan_pop_limited = get_attribute_value(input_string, "pop_limited", r"no", default="yes")
    scan_is_pop_spawned = get_attribute_value(input_string, "is_pop_spawned", r"yes", default="no")
    scan_has_species = get_attribute_value(input_string, "has_species", r"no", default="yes")
    scan_disband_if_species_lacks_rights = get_attribute_value(input_string, "disband_if_species_lacks_rights", r"no", default="yes")
    scan_use_armynames_from = get_attribute_value(input_string, "use_armynames_from", r"\w+")

    # Try to find the prerequisites block
    prerequisites_pattern = r'prerequisites\s*=\s*{([^}]*)}'
    prerequisites_block = None

    for match in re.finditer(prerequisites_pattern, input_string, flags=re.DOTALL):
        prerequisites_block = match.group(1)
        break

    if prerequisites_block:
        scan_prerequisites_list = re.findall(r'"([^"]+)"|(\S+)', prerequisites_block)
        scan_prerequisites_list = [item[0] if item[0] else item[1] for item in scan_prerequisites_list]
    else:
        scan_prerequisites_list = None

    # Find blocks of code with 1..inf amount of opening and closing curly braces (How the fuck does PDS do this???)
    num_unpaired_braces = 0
    scan_variables = {
        "resources": [False, ""],
        "show_tech_unlock_if": [False, ""],
        "potential": [False, ""],
        "potential_country": [False, ""],
        "allow": [False, ""],
        "on_queued": [False, ""],
        "on_unqueued": [False, ""],
        "ai_weight": [False, ""],
    }

    for line in input_string.splitlines():
        if "{" in line:
            num_unpaired_braces += 1

        if num_unpaired_braces >= 1:
            for key, (inside_flag, scan_data) in scan_variables.items():
                if f"{key} = {{" in line:
                    inside_flag = True
                if inside_flag:
                    scan_data += line + "\n"
                    if line.rstrip().endswith("}") and num_unpaired_braces == 2:
                        inside_flag = False
                scan_variables[key] = [inside_flag, scan_data]

        if "}" in line:
            num_unpaired_braces -= 1

    for key, (inside_flag, scan_data) in scan_variables.items():
        if key != "resources" and key != "ai_weight" and scan_data:
            scan_variables[key][1] = strip_first_and_last_brace(scan_data)
        if key == "ai_weight":
            scan_ai_weight_base = handle_ai_weight(scan_data, True)
            scan_ai_weight_modifiers = handle_ai_weight(scan_data, False)

    # Retrieve the scan results
    scan_resource_table = scan_variables["resources"][1]
    scan_show_tech_unlock = scan_variables["show_tech_unlock_if"][1]
    scan_potential = scan_variables["potential"][1]
    scan_potential_country = scan_variables["potential_country"][1]
    scan_allow = scan_variables["allow"][1]
    scan_on_queued = scan_variables["on_queued"][1]
    scan_on_unqueued = scan_variables["on_unqueued"][1]

    # NOTE: Never actually called, but whatever lmao
    # scan_ai_weight = scan_variables["ai_weight"][1]

    # Make the CArmy object and append it to the list
    army = CArmy(
        script_army_name=scan_army_name,
        script_damage=scan_damage,
        script_health=scan_health,
        script_morale=scan_morale,
        script_morale_damage=scan_morale_damage,
        script_collateral_damaage=scan_collateral,
        script_war_exhaustion=scan_war_exhaustion,
        script_build_time=scan_time,
        script_icon=scan_icon,
        script_prereqs=scan_prerequisites_list,
        script_ai_weight_base=scan_ai_weight_base,
        script_show_tech_unlock_if=scan_show_tech_unlock,
        script_potential_country=scan_potential_country,
        script_potential=scan_potential,
        script_allow=scan_allow,
        script_on_queued=scan_on_queued,
        script_on_unqueued=scan_on_unqueued,
        script_ai_weight_modifiers=scan_ai_weight_modifiers,
        script_resource_table=scan_resource_table,
        script_has_species=scan_has_species,
        script_disband_if_species_lacks_rights=scan_disband_if_species_lacks_rights,
        script_defensive=scan_defensive,
        script_occupation=scan_occupation,
        script_pop_limited=scan_pop_limited,
        script_is_pop_spawned=scan_is_pop_spawned,
        script_use_armynames_from=scan_use_armynames_from,
    )
    list_of_CArmies.append(army)


def get_attribute_value(input_string: str, attribute: str, pattern: str, default=None) -> str:
    """Gets an attribute when given an regex pattern, returns default otherwise. Ignores case and is multiline"""
    match = re.search(
        rf"{attribute}\s*=\s*({pattern})", input_string, flags=re.DOTALL | re.IGNORECASE
    )
    return match.group(1) if match else default


def strip_first_and_last_brace(input_string: str) -> str:
    """Returns everything between the first and last brace"""
    first_brace_index = input_string.find("{")
    last_brace_index = input_string.rfind("}")

    # Account for leading spaces and get the substring between the braces
    return input_string[first_brace_index + 1 : last_brace_index].strip()


def handle_ai_weight(input_string: str, is_base: bool=False) -> str:
    """Returns either the AI Weight base or the modifiers for it, depending on is_base"""
    if is_base:
        return get_attribute_value(input_string, "base", r"\d+\.?\d*")
    else:
        lines = input_string.splitlines()[2:-1]
        return "\n".join(lines).strip()


# If you want to use this code to make your own parser for PDScript, everything above this comment is probably what you want.


def create_folders() -> None:
    """Creates the required folders"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(common_folder):
        os.makedirs(common_folder)
    if not os.path.exists(armies_folder):
        os.makedirs(armies_folder)
    if not os.path.exists(localisation_folder):
        os.makedirs(localisation_folder)


def generate_loc_keys(file_name_prefix: str) -> None:
    """Generates every loc key for every language"""

    file_content = ""
    for key in list_of_CArmies:
        comment_block = "#" * len(f"### {key.persistent_army_name} ###")
        file_content += f"\n {comment_block}\n"
        file_content += f" ### {key.persistent_army_name.upper()} ###\n"
        file_content += f" {comment_block}\n"
        file_content += f' pmca_ten_{key.persistent_army_name}: "$pmca_ten$ ${key.persistent_army_name}$"\n'
        file_content += f' pmca_ten_{key.persistent_army_name}_plural: "${key.persistent_army_name}_plural$"\n'
        file_content += f' pmca_ten_{key.persistent_army_name}_desc: "${key.persistent_army_name}_desc$"\n'
        file_content += f' pmca_hundred_{key.persistent_army_name}: "$pmca_hundred$ ${key.persistent_army_name}$"\n'
        file_content += f' pmca_hundred_{key.persistent_army_name}_plural: "${key.persistent_army_name}_plural$"\n'
        file_content += f' pmca_hundred_{key.persistent_army_name}_desc: "${key.persistent_army_name}_desc$"\n'

    for language in stellaris_languages:
        file_name = os.path.join(localisation_folder, f"{file_name_prefix}_{language}.yml")
        with open(file_name, "w", encoding="utf-8-sig") as file_output:
            file_output.write(f"{language}:\n\n # Localisation generated using Python\n{file_content}")


def multiply_army_stats_by_factor(input_CArmy: CArmy, factor: float, is_hundred: bool=False) -> None:
    """Multiplies a given CArmy stats by 10"""

    # Multiply resource stats
    for item in input_CArmy.resource_pairs:
        for key, value in item.items():
            try:
                multiplied_value = float(value) * factor
                item[key] = str(multiplied_value)
            except ValueError:
                pass

    # Multiply regular stats
    input_CArmy.damage *= factor
    input_CArmy.health *= factor
    if input_CArmy.has_morale:
        input_CArmy.morale *= factor
    input_CArmy.collateral_damage *= factor
    input_CArmy.war_exhaustion *= factor

    # Multiply AI Weight base
    if input_CArmy.ai_weight is not None:
        ai_weight_multiplier = 2 / 3 * 2 if is_hundred else 1.5
        input_CArmy.ai_weight *= ai_weight_multiplier

    update_potential_country(input_CArmy, is_hundred)


def update_potential_country(input_CArmy: CArmy, is_hundred: bool=False) -> None:
    """Adds the pmca_materiel_policy_check to self.potential_country"""

    pmca_mult = "ten" if not is_hundred else "hundred"
    current_resource = "food"
    current_resource_value = 0

    # NOTE: how the fuck do lambda functions work
    for sub_type, trigger, resource in zip(input_CArmy.sub_block_type, input_CArmy.trigger_list, input_CArmy.resource_pairs):
        if sub_type == "cost" and trigger == ["always = yes"]:
            current_resource, current_resource_value = max(resource.items(), key=lambda x: resource_priority_dict[x[0]])

    conditional_newline = "\n" if not is_hundred else ""

    # NOTE: This looks terrible I know, but I GitHub will scream at me for spaces vs tabs in the diffs
    scripted_trigger = f"pmca_materiel_policy_check = {{\n\t\t\tPMCA_MULT = {pmca_mult}\n\t\t\tPMCA_RESOURCE = {current_resource}\n\t\t\tPMCA_VALUE = {current_resource_value}\n\t\t}}\n{conditional_newline}"

    if (
        not is_hundred
        and input_CArmy.potential_country
        and not input_CArmy.potential_country.startswith("\t\t")
    ):
        input_CArmy.potential_country = "\t\t" + input_CArmy.potential_country

    # HACK: This is a really stupid way to stop duplication of the scripted_trigger and I don't care
    input_CArmy.potential_country = re.sub(
        r"pmca_materiel_policy_check\s*=\s*{[^}]*}\n?",
        "",
        input_CArmy.potential_country,
    )
    input_CArmy.potential_country = scripted_trigger + input_CArmy.potential_country

    optimize_triggers(input_CArmy)


def optimize_triggers(input_CArmy: CArmy) -> None:
    """Replaces common triggers with scripted triggers"""

    # Add your trigger to scripted trigger replacements here
    replacement_patterns = {
        "NOT = { has_authority = auth_machine_intelligence }": "is_machine_empire = no",
        "has_authority = auth_machine_intelligence": "is_machine_empire = yes",
        "NOT = { has_authority = auth_hive_mind }": "is_hive_empire = no",
        "has_authority = auth_hive_mind": "is_hive_empire = yes",
        "NOT = { has_ethic = ethic_gestalt_consciousness }": "is_gestalt = no",
        "has_ethic = ethic_gestalt_consciousness": "is_gestalt = yes",
        "NOT = { has_authority = auth_corporate }": "is_megacorp = no",
        "has_authority = auth_corporate": "is_megacorp = yes",
    }

    for trigger in replacement_patterns:
        input_CArmy.show_tech_unlock_if = input_CArmy.show_tech_unlock_if.replace(trigger, replacement_patterns[trigger])
        input_CArmy.potential_country = input_CArmy.potential_country.replace(trigger, replacement_patterns[trigger])
        input_CArmy.potential = input_CArmy.potential.replace(trigger, replacement_patterns[trigger])
        input_CArmy.allow = input_CArmy.allow.replace(trigger, replacement_patterns[trigger])
        input_CArmy.ai_weight_conditions = input_CArmy.ai_weight_conditions.replace(trigger, replacement_patterns[trigger])


def generate_army_defs(file_prefix: str) -> None:
    """Generates all of the army definitions"""

    times_ten_defs = os.path.join(armies_folder, f"{file_prefix}_x10_armies.txt")
    times_hundred_defs = os.path.join(armies_folder, f"{file_prefix}_x100_armies.txt")
    x10_output = "# x10 army definitions generated using Python\n\n"
    x100_output = "# x100 army definitions generated using Python\n\n"

    for army in list_of_CArmies:
        army.army_name = "pmca_ten_" + army.army_name
        multiply_army_stats_by_factor(army, 10)
        x10_output += army.convert_to_pdscript()
    for army in list_of_CArmies:
        army.army_name = army.army_name.replace("pmca_ten_", "pmca_hundred_")
        multiply_army_stats_by_factor(army, 10, True)
        x100_output += army.convert_to_pdscript()

    with open(times_ten_defs, "w", encoding="utf-8") as file_output:
        file_output.write(x10_output)

    with open(times_hundred_defs, "w", encoding="utf-8") as file_output:
        file_output.write(x100_output)

def add_concerning_armies_to_list() -> None:
    """Adds armies that are unbuildable to a list for viewing later"""
    global concerning_CArmies  # python being quirky for some reason

    for army in list_of_CArmies:
        key = army.persistent_army_name
        value = []

        if army.defensive == "yes":
            value.append("The 'defensive' property is set to 'yes' in the army definition.")

        if army.occupation == "yes":
            value.append("The 'occupation' property is set to 'yes' in the army definition.")

        blocks_to_check = ["potential_country", "potential", "allow", "on_queued", "on_unqueued"]

        blocks_with_always_no = []
        blocks_with_variable_modification = []

        for block in blocks_to_check:
            if army.__getattribute__(block).strip().startswith("always = no"):
                blocks_with_always_no.append(block)

            if army.__getattribute__(block).find("variable = {") != -1:
                blocks_with_variable_modification.append(block)

        if blocks_with_always_no:
            value.append(f"The '{', '.join(blocks_with_always_no)}' {'blocks' if len(blocks_with_always_no) > 1 else 'block'} starts with 'always = no'.")

        if blocks_with_variable_modification:
            value.append(f"Variable modification detected in the '{', '.join(blocks_with_variable_modification)}' {'blocks' if len(blocks_with_variable_modification) > 1 else 'block'}.")

        concerning_CArmies[key] = value

    concerning_CArmies = {key: value for key, value in concerning_CArmies.items() if value}



def generate_pm_condensed_armies() -> None:
    """Actually runs stuff"""

    if os.path.isfile(".\input.txt"):
        input_file_prefix = input("Enter a custom file prefix, or leave blank to default to 'REPLACE_ME': ")

        if not input_file_prefix.strip():
            file_prefix = "REPLACE_ME"
        else:
            file_prefix = input_file_prefix

        start = time.time()
        print("\nCreating directories...")

        create_folders()

        print("Scanning input...")
        scan_input_file()

        add_concerning_armies_to_list()

        print("Writing x10 and x100 definitions...")
        generate_army_defs(file_prefix)

        print("Generating localisation keys...")
        generate_loc_keys(file_prefix)

        print(f"Done! Check the Directory '{directory}' for your freshly Condensed Armies!")

        end = time.time()
        time_in_milliseconds = round((end - start) * 1000, 2)
        print("\n------------------------\n")
        print("Stats:")
        print(f"  - Number of Army Definitions: {len(list_of_CArmies)}")
        print(f"  - Number of languages supported by Stellaris: {len(stellaris_languages)}")
        print(f"  - Number of localisation keys generated: {len(list_of_CArmies) * 6 * len(stellaris_languages)} total | {len(list_of_CArmies) * 6} per file")
        print(f"  - Estimated time to complete: {time_in_milliseconds} milliseconds\n")

        if len(concerning_CArmies) > 0 and input("Some armies were detected as unbuildable and/or should not be condensed. Would you like to see the details? [Y/N]: ").upper() == "Y":
            print("\n------------------------\n")
            for key, values in concerning_CArmies.items():
                print(f"{key}:")
                for value in values:
                    print(f"  - {value}")

            if input("\nWould you like to see a quick explanation of all of the warnings? [Y/N]: ").upper() == "Y":
                print("\n------------------------\n")
                print("The 'defensive' property is set to 'yes' in the army definition:")
                print("  - Defensive armies are usually unbuildable, but condensing is up to personal preference if they are buildable.")
                print("The 'occupation' property is set to 'yes' in the army definition:")
                print("  - I have no idea how Stellaris would handle condensed occupation armies, but they're unbuildable so /shrug.")
                print("The 'BLOCK' block starts with 'always = no':")
                print("  - Literally impossible for either the player and AI to build them.")
                print("  - Only the first line is checked due to the script not understanding nuance, such as banning AI from building a certain army.")
                print("Variable modification detected in the 'BLOCK' block:")
                print("  - Events that handle increasing/decreasing variables usually don't account for condensed versions of armies.")
    else:
        print("ERROR: input.txt does NOT exist! Please create it and put your army definitions inside it.")

generate_pm_condensed_armies()
