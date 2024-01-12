import re, time, os, shutil

stellaris_languages = [
    "braz_por",
    "english",
    "french",
    "german",
    "japanese",
    "korean",
    "polish",
    "russian",
    "simp_chinese",
    "spanish",
]

vanilla_army_keys = [
    "assault_army",
    "slave_army",
    "clone_army",
    "robotic_army",
    "psionic_army",
    "xenomorph_army",
    "gene_warrior_army",
    "machine_assault_1",
    "machine_assault_2",
    "machine_assault_3",
    "undead_army",
    "warpling_army",
    "flamestorm_troopers_army",
    "cybrex_warform",
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
    "astral_threads": 9,
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
    "giga_sr_amb_megaconstruction": 12,
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

list_of_armies = []
armies_with_issues = {
    "Unbuildable": [],
    "Variable Manipulation": [],
    "Odd Property": [],
}
block_regex = re.compile(r"(\w+)\s*=\s*{")
complex_block_regex = re.compile(
    r"(prerequisites|resources|show_tech_unlock_if|potential|potential_country|allow|on_queued|on_unqueued|ai_weight|spawn_chance|army_modifier)\s*=\s*{"
)
field_value_pair_regex = re.compile(r"(\w+)\s*=\s*([-+]?\d+\.?\d*)")
field_bool_pair_regex = re.compile(r"(\w+)\s*=\s*(yes|no)")
icon_regex = re.compile(r"icon\s*=\s*(\w+)")
prerequisites_regex = re.compile(r"prerequisites\s*=\s*{(.*)}")
category_regex = re.compile(r"category\s*=\s*(\w+)")
subsection_type_regex = re.compile(r"(cost|upkeep|produces)\s*=\s*{")
mult_field_regex = re.compile(r"(?:multiplier|mult)\s*=\s*(\S+)")
ai_weight_base_regex = re.compile(r"base\s*=\s*([-+]?\d+\.?\d*)")


class pdscript_resource_table_subsection:
    def __init__(
        self,
        sub_type: str,
        trigger_block: str,
        resource_value_pairs: dict,
        multiplier: str,
    ):
        self.sub_type = sub_type
        self.trigger_block = trigger_block
        self.resource_value_pairs = resource_value_pairs
        self.multiplier = multiplier

    def multiply_economy(self, factor: float | int) -> None:
        """Multplies all valid resources = value pairs by a factor

        Args:
            factor (float | int): Number to multiply by
        """
        self.resource_value_pairs = {
            key: value * factor for key, value in self.resource_value_pairs.items()
        }

    def construct_subsection(self) -> str:
        """Constructs a valid resource subsection

        Returns:
            str: The resource subsection
        """
        if self.trigger_block.strip().startswith("always = no"):
            return ""

        subsection_output = f"\t\t{self.sub_type} = {{\n"

        if self.trigger_block.strip() != "always = yes":
            subsection_output += "\t\t\t\ttrigger = {\n"
            subsection_output += f"\t\t\t\t\t{self.trigger_block}\n"
            subsection_output += "\t\t\t\t}\n"

        for key, value in self.resource_value_pairs.items():
            subsection_output += f"\t\t\t\t{key} = {value}\n"

        if self.multiplier != 1.0:
            subsection_output += f"\t\t\t\tmultiplier = {self.multiplier}\n"

        subsection_output += "\t\t\t}"
        return subsection_output


class pdscript_army:
    def __init__(
        self,
        army_name: str,
        defensive: bool,
        occupation: bool,
        is_pop_spawned: bool,
        rebel: bool,
        damage: float,
        health: float,
        has_morale: bool,
        morale: float,
        morale_damage: float,
        collateral_damage: float,
        war_exhaustion: float,
        time: float,
        has_species: bool,
        disband_if_species_lacks_right: bool,
        icon: str,
        prerequisites: str,
        resource_table_category: str,
        resource_table: list[pdscript_resource_table_subsection],
        show_tech_unlock_if: str,
        potential: str,
        potential_country: str,
        allow: str,
        on_queued: str,
        on_unqueued: str,
        ai_weight_base: float,
        ai_weight_extra: str,
        spawn_chance: str,
        army_modifier: str,
    ):
        self.army_name = army_name
        self.use_army_names_from = self.army_name
        self.defensive = defensive
        self.occupation = occupation
        self.is_pop_spawned = is_pop_spawned
        self.rebel = rebel
        self.damage = damage
        self.health = health
        self.has_morale = has_morale
        self.morale = morale
        self.morale_damage = morale_damage
        self.collateral_damage = collateral_damage
        self.war_exhaustion = war_exhaustion
        self.time = time
        self.has_species = has_species
        self.disband_if_species_lacks_right = disband_if_species_lacks_right
        self.icon = icon
        self.prerequisites = prerequisites
        self.resource_table_category = resource_table_category
        self.resource_table = resource_table
        self.show_tech_unlock_if = show_tech_unlock_if
        self.potential = potential
        self.potential_country = potential_country.strip()
        self.allow = allow
        self.on_queued = on_queued
        self.on_unqueued = on_unqueued
        self.ai_weight_base = ai_weight_base
        self.ai_weight_extra = ai_weight_extra
        self.spawn_chance = spawn_chance
        self.army_modifier = army_modifier

        self.pmca_mult = "ten"
        self.pmca_resource = "food"
        self.pmca_resource_value = "0"

        if (
            self.potential.strip().startswith("always = no")
            or self.potential_country.strip().startswith("always = no")
            or self.allow.strip().startswith("always = no")
        ):
            self.unbuildable = True
        else:
            self.unbuildable = False

        blocks_to_indent = [
            "show_tech_unlock_if",
            "potential",
            "potential_country",
            "allow",
            "on_queued",
            "on_unqueued",
            "ai_weight_extra",
            "spawn_chance",
            "army_modifier",
        ]

        for block in blocks_to_indent:
            lines = self.__getattribute__(block).splitlines()
            tabbed_lines = ["\t" + line for line in lines]
            tabbed_string = "\n".join(tabbed_lines)
            self.__setattr__(block, tabbed_string)

    def convert_to_pdscript(self) -> str:
        """Turns all of the class variables into a string

        Returns:
            str: A string that should make a functioning army in PDScript
        """
        pdscript_output = ""

        pdscript_output += f"\tpmca_{self.pmca_mult}_{self.army_name} = {{\n"
        pdscript_output += f"\t\tuse_armynames_from = {self.use_army_names_from}\n"

        if self.defensive:
            pdscript_output += f"\t\tdefensive = yes\n"
        if self.occupation:
            pdscript_output += f"\t\toccupation = yes\n"
        if self.is_pop_spawned:
            pdscript_output += f"\t\tis_pop_spawned = yes\n"
        if self.rebel:
            pdscript_output += f"\t\trebel = yes\n"

        pdscript_output += f"\t\tdamage = {self.damage}\n"
        pdscript_output += f"\t\thealth = {self.health}\n"

        if not self.has_morale:
            pdscript_output += f"\t\thas_morale = no\n"
        else:
            pdscript_output += f"\t\tmorale = {self.morale}\n"

        pdscript_output += f"\t\tmorale_damage = {self.morale_damage}\n"
        pdscript_output += f"\t\tcollateral_damage = {self.collateral_damage}\n"
        pdscript_output += f"\t\twar_exhaustion = {self.war_exhaustion}\n"
        pdscript_output += f"\t\ttime = {self.time}\n"

        if not self.has_species:
            pdscript_output += f"\t\thas_species = no\n"
        if not self.disband_if_species_lacks_right:
            pdscript_output += f"\t\tdisband_if_species_lacks_right = no\n"

        pdscript_output += f"\t\ticon = {self.icon}\n"

        if len(self.prerequisites) > 0:
            list_of_techs = re.findall(r"\w+", str(self.prerequisites))
            pdscript_output += f"\t\tprerequisites = {{"
            if len(list_of_techs) == 1:
                pdscript_output += f" {list_of_techs[0]} }}\n"
            else:
                pdscript_output += "\n" + "\n".join(
                    f"\t\t\t{item}" for item in list_of_techs
                )
                pdscript_output += f"\n\t\t}}\n"

        if len(self.resource_table) > 0:
            pdscript_output += f"\t\tresources = {{\n"
            pdscript_output += f"\t\t\tcategory = {self.resource_table_category}\n"
            pdscript_output += "\n".join(
                f"\t{subsection.construct_subsection()}"
                for subsection in self.resource_table
            )
            pdscript_output += f"\n\t\t}}\n"

        if self.show_tech_unlock_if.strip():
            pdscript_output += f"\t\tshow_tech_unlock_if = {{\n"
            pdscript_output += f"\t\t\t{self.show_tech_unlock_if.strip()}\n"
            pdscript_output += f"\t\t}}\n"

        if self.unbuildable:
            pdscript_output += "\t\tpotential = { always = no }\n"
        else:
            if self.potential.strip():
                pdscript_output += f"\t\tpotential = {{\n"
                pdscript_output += f"\t\t\t{self.potential.strip()}\n"
                pdscript_output += f"\t\t}}\n"

            pdscript_output += f"\t\tpotential_country = {{\n"
            pdscript_output += (
                f"\t\t\t{self.potential_country.strip()}\n"
                if self.potential_country.strip()
                else ""
            )
            pdscript_output += f"\t\t\tpmca_materiel_policy_check = {{\n\t\t\t\tPMCA_MULT = {self.pmca_mult}\n\t\t\t\tPMCA_RESOURCE = {self.pmca_resource}\n\t\t\t\tPMCA_VALUE = {self.pmca_resource_value}\n\t\t\t}}\n"
            pdscript_output += f"\t\t}}\n"

            if self.allow.strip():
                pdscript_output += f"\t\tallow = {{\n"
                pdscript_output += f"\t\t\t{self.allow.strip()}\n"
                pdscript_output += f"\t\t}}\n"

            if self.on_queued.strip():
                pdscript_output += f"\t\ton_queued = {{\n"
                pdscript_output += f"\t\t\t{self.on_queued.strip()}\n"
                pdscript_output += f"\t\t}}\n"

            if self.on_unqueued.strip():
                pdscript_output += f"\t\ton_unqueued = {{\n"
                pdscript_output += f"\t\t\t{self.on_unqueued.strip()}\n"
                pdscript_output += f"\t\t}}\n"

            pdscript_output += f"\t\tai_weight = {{\n"
            pdscript_output += f"\t\t\tbase = {self.ai_weight_base}\n"
            pdscript_output += (
                f"\t\t\t{self.ai_weight_extra.strip()}\n"
                if self.ai_weight_extra.strip()
                else ""
            )
            pdscript_output += f"\t\t}}\n"

        if self.spawn_chance.strip():
            pdscript_output += f"\t\tspawn_chance = {{\n"
            pdscript_output += f"\t\t\t{self.spawn_chance.strip()}\n"
            pdscript_output += f"\t\t}}\n"

        if self.army_modifier.strip():
            pdscript_output += f"\t\tarmy_modifier = {{\n"
            pdscript_output += f"\t\t\t{self.army_modifier.strip()}\n"
            pdscript_output += f"\t\t}}\n"

        pdscript_output += f"\t}}\n"
        return pdscript_output


###########################
### NON-CLASS FUNCTIONS ###
###########################


def scan_input_file() -> None:
    """Scans input.txt for army definitions"""

    with open("input.txt", "r") as file_input:
        file_content = file_input.readlines()

    brace_level = 0
    army_definition = ""

    for line in file_content:
        line = line.replace('"', "")
        if line.strip() and not line.strip().startswith("#"):
            if "{" in line:
                brace_level += line.count("{")
            if "}" in line:
                brace_level -= line.count("}")
            army_definition += line
            if brace_level == 0:
                list_of_armies.append(parse_army(army_definition))
                army_definition = ""


def parse_army(input_string: str):
    """Parses a given string into the various parts needed to make a valid PDScript army

    Args:
        input_string (str): A string containing an army definition
    """

    brace_level = 0
    block_data = {
        "resources": [-1, ""],
        "show_tech_unlock_if": [-1, ""],
        "potential": [-1, ""],
        "potential_country": [-1, ""],
        "allow": [-1, ""],
        "on_queued": [-1, ""],
        "on_unqueued": [-1, ""],
        "ai_weight": [-1, ""],
        "spawn_chance": [-1, ""],
        "army_modifier": [
            -1,
            "",
        ],
    }
    block_name = None
    list_of_complex_blocks = re.findall(complex_block_regex, input_string)
    list_of_complex_blocks.reverse()

    for i, char in enumerate(input_string):
        if char == "{":
            brace_level += 1
            # Entered a = { } block
            if brace_level == 2:
                block_name = list_of_complex_blocks.pop()
                if block_name and not block_name == "prerequisites":
                    block_data[block_name][0] = i

        elif char == "}":
            brace_level -= 1
            # Exited a = { } block
            if brace_level == 1:
                if block_name and not block_name == "prerequisites":
                    block_data[block_name][1] = input_string[
                        block_data[block_name][0] + 1 : i
                    ]

    # Find and assign the simple inputs
    field_value_tuple = re.findall(field_value_pair_regex, input_string) + re.findall(
        field_bool_pair_regex, input_string
    )
    field_value_dict = {
        item[0]: (
            True if item[1] == "yes" else False if item[1] == "no" else float(item[1])
        )
        for item in field_value_tuple
    }

    input_army_name = re.match(block_regex, input_string).group(1)
    input_defensive = get_field_value(field_value_dict, "defensive", False)
    input_occupation = get_field_value(field_value_dict, "occupation", False)
    input_is_pop_spawned = get_field_value(field_value_dict, "is_pop_spawned", False)
    input_rebel = get_field_value(field_value_dict, "rebel", False)
    input_health = get_field_value(field_value_dict, "health", 1.00)
    input_damage = get_field_value(field_value_dict, "damage", 1.00)
    input_has_morale = get_field_value(field_value_dict, "has_morale", True)
    input_morale = get_field_value(field_value_dict, "morale", 1.00)
    input_morale_damage = get_field_value(field_value_dict, "morale_damage", 1.00)
    input_collateral_damage = get_field_value(
        field_value_dict, "collateral_damage", 1.00
    )
    input_war_exhaustion = get_field_value(field_value_dict, "war_exhaustion", 1.00)
    input_time = get_field_value(field_value_dict, "time", 0.00)
    input_has_species = get_field_value(field_value_dict, "has_species", True)
    input_disband_if_species_lacks_right = get_field_value(
        field_value_dict, "disband_if_species_lacks_right", True
    )

    icon_match = re.search(icon_regex, input_string)
    input_icon = icon_match.group(1) if icon_match else "GFX_army_type_defensive"

    prerequisites_match = re.findall(prerequisites_regex, input_string)
    input_prerequisites = prerequisites_match if prerequisites_match else ""

    # Handle complex (nested braces) inputs
    input_resource_table_category, input_resource_table = parse_resource_table(
        block_data.get("resources")[1]
    )
    input_show_tech_unlock_if = block_data.get("show_tech_unlock_if")[1]
    input_potential = block_data.get("potential")[1]
    input_potential_country = block_data.get("potential_country")[1]
    input_allow = block_data.get("allow")[1]
    input_on_queued = block_data.get("on_queued")[1]
    input_on_unqueued = block_data.get("on_unqueued")[1]
    input_ai_weight_base, input_ai_weight_extra = parse_ai_weight(
        block_data.get("ai_weight")[1]
    )
    input_spawn_chance = block_data.get("spawn_chance")[1]
    input_army_modifier = block_data.get("army_modifier")[1]

    new_army = pdscript_army(
        army_name=input_army_name,
        defensive=input_defensive,
        occupation=input_occupation,
        is_pop_spawned=input_is_pop_spawned,
        rebel=input_rebel,
        damage=input_damage,
        health=input_health,
        has_morale=input_has_morale,
        morale=input_morale,
        morale_damage=input_morale_damage,
        collateral_damage=input_collateral_damage,
        war_exhaustion=input_war_exhaustion,
        time=input_time,
        has_species=input_has_species,
        disband_if_species_lacks_right=input_disband_if_species_lacks_right,
        icon=input_icon,
        prerequisites=input_prerequisites,
        resource_table_category=input_resource_table_category,
        resource_table=input_resource_table,
        show_tech_unlock_if=input_show_tech_unlock_if,
        potential=input_potential,
        potential_country=input_potential_country,
        allow=input_allow,
        on_queued=input_on_queued,
        on_unqueued=input_on_unqueued,
        ai_weight_base=input_ai_weight_base,
        ai_weight_extra=input_ai_weight_extra,
        spawn_chance=input_spawn_chance,
        army_modifier=input_army_modifier,
    )

    return new_army


def get_field_value(dictionary: dict, search_item, default_if_none):
    """Gets a value from a dictionary if possible

    Args:
        dictionary (dict): Dictionary to search
        search_item (any): What to search for
        default_if_none (any): If search_item doesn't exist

    Returns:
        any: Value of search_item, or default_if_none
    """
    return dictionary.get(search_item, default_if_none)


def parse_resource_table(input_string: str) -> tuple[str, list]:
    """Parses a valid resource table

    Args:
        input_string (str): A valid resource table as a string

    Returns:
        tuple[str, list]: [0] is the economic category | [1] is a list of pdscript_resource_table_subsection
    """
    current_brace_level = 0
    resource_table_brace_level = 0
    subsection_brace_level = 1
    subsection_trigger_brace_level = 2

    opening_brace_stack = []

    category = ""
    subsection_type = ""
    subsection_trigger_data = ""
    subsection_data = ""
    resource_pairs = {}
    mult_value = 1.0

    list_of_subsections = []

    category_match = re.search(category_regex, input_string)
    category = category_match.group(1) if category_match else "armies"

    subection_types = re.findall(subsection_type_regex, input_string)
    subection_types.reverse()

    for i, char in enumerate(input_string):
        if char == "{":
            current_brace_level += 1

            # Must have entered a subsection
            if current_brace_level == subsection_brace_level:
                opening_brace_stack.append(i)
                subsection_type = subection_types.pop()

            # Must have exited the subsection's trigger block
            if current_brace_level == subsection_trigger_brace_level:
                opening_brace_stack.append(i)
                subsection_trigger_data += "trigger = "

        if char == "}":
            current_brace_level -= 1

            # Must have exited the subsection's trigger block
            if current_brace_level == subsection_brace_level:
                subsection_trigger_data += input_string[
                    opening_brace_stack.pop() : i + 1
                ]

            # Must have exited the subsection
            if current_brace_level == resource_table_brace_level:
                subsection_data = input_string[opening_brace_stack.pop() + 1 : i]
                subsection_data = subsection_data.replace(subsection_trigger_data, "")
                trigger_first_brace_index = subsection_trigger_data.find("{")
                trigger_last_brace_index = subsection_trigger_data.rfind("}")
                subsection_trigger_data = subsection_trigger_data[
                    trigger_first_brace_index + 1 : trigger_last_brace_index
                ]

                if subsection_data.strip():
                    temp_resource_tuples = re.findall(
                        field_value_pair_regex, subsection_data
                    )
                    resource_pairs = {
                        key: float(value) for key, value in temp_resource_tuples
                    }
                    if resource_pairs.get("mult"):
                        mult_value = resource_pairs.get("mult")
                        resource_pairs.pop("mult")
                    elif resource_pairs.get("multiplier"):
                        mult_value = resource_pairs.get("multiplier")
                        resource_pairs.pop("multiplier")
                    else:
                        mult_match = re.search(mult_field_regex, subsection_data)
                        mult_value = mult_match.group(1) if mult_match else 1.0

                    if not (subsection_trigger_data.strip()):
                        subsection_trigger_data = "always = yes"

                    new_resource_subsection = pdscript_resource_table_subsection(
                        sub_type=subsection_type,
                        trigger_block=subsection_trigger_data,
                        resource_value_pairs=resource_pairs,
                        multiplier=mult_value,
                    )

                    list_of_subsections.append(new_resource_subsection)

                # Set to blank for safety
                subsection_type = ""
                subsection_trigger_data = ""
                subsection_data = ""
                resource_pairs = {}
                mult_value = 1.0

    return category, list_of_subsections


def parse_ai_weight(input_string: str) -> tuple[float, str]:
    """Parses a valid AI weight block

    Args:
        input_string (str): A valid ai_weight block

    Returns:
        tuple[float, str]: [0] is the first instance of 'base', defaults to 0 | [1] is the rest of the input
    """
    ai_weight_base = 0
    ai_weight_string = ""

    ai_weight_base_match = re.search(ai_weight_base_regex, input_string)
    ai_weight_base = (
        float(ai_weight_base_match.group(1)) if ai_weight_base_match else 0.00
    )

    ai_weight_string = re.sub(ai_weight_base_regex, "", input_string, 1)

    return ai_weight_base, ai_weight_string


##################################
### CONDENSED ARMIES FUNCTIONS ###
##################################


directory = ".\PMCA_GEN_OUTPUT"
common_folder = os.path.join(directory, "common")
armies_folder = os.path.join(common_folder, "armies")
localisation_folder = os.path.join(directory, "localisation")


def multiply_stats(input_army: pdscript_army, factor: float | int) -> None:
    """Multiplies an army's stats by a number

    Args:
        input_army (pdscript_army): A valid army object
        factor (float | int): A number to multiply the stats by
    """
    # Multiply regular stats
    input_army.damage *= factor
    input_army.health *= factor
    input_army.morale *= factor
    input_army.collateral_damage *= factor
    input_army.war_exhaustion *= factor
    for subsection in input_army.resource_table:
        subsection.multiply_economy(factor)


def condense_armies(input_army: pdscript_army, is_hundred: bool) -> None:
    """Turns an army into a x10/x100 pmca army

    Args:
        input_army (pdscript_army): A valid army object
        is_hundred (bool): Are you going from vanilla > x10 or x10 > x100?
    """
    input_army.pmca_mult = "hundred" if is_hundred else "ten"

    if not is_hundred:
        for subsection in input_army.resource_table:
            if subsection.sub_type == "cost":
                for key, value in subsection.resource_value_pairs.items():
                    priority = resource_priority_dict.get(key)
                    if priority >= resource_priority_dict.get(input_army.pmca_resource):
                        input_army.pmca_resource = key
                        input_army.pmca_resource_value = value
    else:
        input_army.pmca_resource_value *= 10

    ai_weight_multiplier = (2 / 3 * 2) if is_hundred else 1.5
    input_army.ai_weight_base *= ai_weight_multiplier


trigger_regex_patterns = {
    # NOT = { } checks have to be first to prevent weirdness
    # Authority Checks
    re.compile(
        r"NOT\s*=\s*{\s*\n?has_authority\s*=\s*auth_machine_intelligence\s*\n?}"
    ): "is_machine_empire = no",
    re.compile(
        r"has_authority\s*=\s*auth_machine_intelligence"
    ): "is_machine_empire = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?has_authority\s*=\s*auth_hive_mind\s*\n?}"
    ): "is_hive_empire = no",
    re.compile(r"has_authority\s*=\s*auth_hive_mind"): "is_hive_empire = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?has_ethic\s*=\s*ethic_gestalt_consciousness\s*\n?}"
    ): "is_gestalt = no",
    re.compile(r"has_ethic\s*=\s*ethic_gestalt_consciousness"): "is_gestalt = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?has_authority\s*=\s*auth_corporate\s*\n?}"
    ): "is_megacorp = no",
    re.compile(r"has_authority\s*=\s*auth_corporate"): "is_megacorp = yes",
    # DLC Checks
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Leviathans Story Pack\s*\n?}"
    ): "has_leviathans = no",
    re.compile(r"host_has_dlc\s*=\s*Leviathans Story Pack"): "has_leviathans = yes",
    re.compile(r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Utopia\s*\n?}"): "has_utopia = no",
    re.compile(r"host_has_dlc\s*=\s*Utopia"): "has_utopia = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Plantoids Species Pack\s*\n?}"
    ): "has_plantoids = no",
    re.compile(r"host_has_dlc\s*=\s*Plantoids Species Pack"): "has_plantoids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Synthetic Dawn Story Pack\s*\n?}"
    ): "has_synthethic_dawn = no",
    re.compile(
        r"host_has_dlc\s*=\s*Synthetic Dawn Story Pack"
    ): "has_synthethic_dawn = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Humanoids Species Pack\s*\n?}"
    ): "has_humanoids = no",
    re.compile(r"host_has_dlc\s*=\s*Humanoids Species Pack"): "has_humanoids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?local_has_dlc\s*=\s*Humanoids Species Pack\s*\n?}"
    ): "has_humanoids_local = no",
    re.compile(
        r"local_has_dlc\s*=\s*Humanoids Species Pack"
    ): "has_humanoids_local = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Lithoids Species Pack\s*\n?}"
    ): "has_lithoids = no",
    re.compile(r"host_has_dlc\s*=\s*Lithoids Species Pack"): "has_lithoids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Federations\s*\n?}"
    ): "has_federations_dlc = no",
    re.compile(r"host_has_dlc\s*=\s*Federations"): "has_federations_dlc = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Necroids Species Pack\s*\n?}"
    ): "has_necroids = no",
    re.compile(r"host_has_dlc\s*=\s*Necroids Species Pack"): "has_necroids = yes",
    re.compile(r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Nemesis\s*\n?}"): "has_nemesis = no",
    re.compile(r"host_has_dlc\s*=\s*Nemesis"): "has_nemesis = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Aquatics Species Pack\s*\n?}"
    ): "has_aquatics = no",
    re.compile(r"host_has_dlc\s*=\s*Aquatics Species Pack"): "has_aquatics= yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Overlord\s*\n?}"
    ): "has_overlord_dlc = no",
    re.compile(r"host_has_dlc\s*=\s*Overlord"): "has_overlord_dlc = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Toxoids Species Pack\s*\n?}"
    ): "has_toxoids = no",
    re.compile(r"host_has_dlc\s*=\s*Toxoids Species Pack"): "has_toxoids = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*First Contact Story Pack\s*\n?}"
    ): "has_first_contact_dlc = no",
    re.compile(
        r"host_has_dlc\s*=\s*First Contact Story Pack"
    ): "has_first_contact_dlc = yes",
    re.compile(
        r"NOT\s*=\s*{\s*\n?host_has_dlc\s*=\s*Astral Planes\s*\n?}"
    ): "has_astral_planes_dlc = no",
    re.compile(r"host_has_dlc\s*=\s*Astral Planes"): "has_astral_planes_dlc = yes",
}


def optimize_trigger(input_army: pdscript_army) -> None:
    """Converts common triggers with vanilla scripted_triggers for compatibility

    Args:
        input_army (pdscript_army): _description_
    """

    for pattern, replacement in trigger_regex_patterns.items():
        input_army.show_tech_unlock_if = re.sub(
            pattern, replacement, input_army.show_tech_unlock_if
        )
        input_army.potential = re.sub(pattern, replacement, input_army.potential)
        input_army.potential_country = re.sub(
            pattern, replacement, input_army.potential_country
        )
        input_army.allow = re.sub(pattern, replacement, input_army.allow)
        input_army.ai_weight_extra = re.sub(
            pattern, replacement, input_army.ai_weight_extra
        )


def create_folders() -> None:
    """Creates the required folders"""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    os.makedirs(common_folder)
    os.makedirs(armies_folder)
    os.makedirs(localisation_folder)
    for language in stellaris_languages:
        os.makedirs(os.path.join(localisation_folder, language))


def generate_defs(file_prefix: str, mod_variable: str) -> None:
    """Generates and writes the required syntax for the inline_script to work

    Args:
        file_prefix (str): Newly created files will start with this
        mod_variable (str): Scripted variable to detect for the conditional inline to work
    """
    army_output = "# Dear Irony please fallback to simple parser\n# x10 and x100 army definition(s) generated via Python\n\n"
    army_defs = os.path.join(armies_folder, f"{file_prefix}_armies.txt")

    # Syntax for the inline
    army_output += f"inline_script = {{\n"
    army_output += f"\tscript = army/pmca_conditional_inline_p1\n"
    army_output += f"\tMOD_VARIABLE = {mod_variable}\n"
    army_output += f'\tCONTENT = "\n'

    for army in list_of_armies:
        multiply_stats(army, 10)
        condense_armies(army, False)
        army_output += f"{army.convert_to_pdscript()}\n"

    for army in list_of_armies:
        multiply_stats(army, 10)
        condense_armies(army, True)
        army_output += f"{army.convert_to_pdscript()}\n"

    # Get rid of the double newline
    army_output = army_output[:-1]

    # Closing quote and brace for the inline
    army_output += f'\t"\n'
    army_output += f"}}\n"

    with open(army_defs, "w+") as fout:
        fout.write(army_output)


def generate_localisation_keys(file_name_prefix: str) -> None:
    """Generates the necessary localisation keys

    Args:
        file_name_prefix (str): Newly created files will start with this
    """
    localisation_output = ""
    army_name_keys = []

    for army in list_of_armies:
        if (
            file_name_prefix == "pmca_vanilla" or file_name_prefix == "pmca"
        ) or army.use_army_names_from not in vanilla_army_keys:
            army_name_keys.append(army.use_army_names_from)

    for key in army_name_keys:
        comment_block = "#" * len(f"### {key} ###")
        localisation_output += f"\n {comment_block}\n"
        localisation_output += f" ### {key.upper()} ###\n"
        localisation_output += f" {comment_block}\n"
        localisation_output += f' pmca_ten_{key}: "$pmca_ten$ ${key}$"\n'
        localisation_output += f' pmca_ten_{key}_plural: "${key}_plural$"\n'
        localisation_output += f' pmca_ten_{key}_desc: "${key}_desc$"\n'
        localisation_output += f' pmca_hundred_{key}: "$pmca_hundred$ ${key}$"\n'
        localisation_output += f' pmca_hundred_{key}_plural: "${key}_plural$"\n'
        localisation_output += f' pmca_hundred_{key}_desc: "${key}_desc$"\n\n'

    for language in stellaris_languages:
        language_folder = os.path.join(localisation_folder, language)
        file_name = os.path.join(
            language_folder, f"{file_name_prefix}_l_{language}.yml"
        )
        with open(file_name, "w", encoding="utf-8-sig") as file_output:
            file_output.write(
                f"l_{language}:\n\n # Localisation generated using Python\n{localisation_output}"
            )


def scan_armies_for_issues() -> None:
    """Adds armies that are unbuildable to a list for viewing later"""

    blocks_to_check = [
        "potential_country",
        "potential",
        "allow",
        "on_queued",
        "on_unqueued",
        "ai_weight_extra",
        "show_tech_unlock_if",
    ]
    variable_modification_regex = re.compile(r".+_variable(?:.+)?\s*=\s*{")

    for army in list_of_armies:
        if army.unbuildable:
            armies_with_issues["Unbuildable"].append(army.army_name)
        if army.defensive or army.occupation or army.rebel or army.is_pop_spawned:
            armies_with_issues["Odd Property"].append(army.army_name)
        for block in blocks_to_check:
            variable_modification_match = re.search(variable_modification_regex, block)
            if variable_modification_match:
                armies_with_issues["Variable Manipulation"].append(army.army_name)


def armies_with_issues_handler() -> None:
    """Handles outputting armies w/ concerning properties to output.txt"""

    issue_string = ""

    if armies_with_issues["Unbuildable"]:
        issue_string += "Armies that are unbuildable:\n"
        for value in armies_with_issues["Unbuildable"]:
            issue_string += f"\t- {value}\n"

    if armies_with_issues["Odd Property"]:
        issue_string += "Armies with Odd Properties:\n"
        for value in armies_with_issues["Odd Property"]:
            issue_string += f"\t- {value}\n"

    if armies_with_issues["Variable Manipulation"]:
        issue_string += "Armies with Variable Manipulation:\n"
        for value in armies_with_issues["Variable Manipulation"]:
            issue_string += f"\t- {value}\n"

    issue_string += f"\n\nHere's a quick breakdown of the terms:\n"
    issue_string += f"\t- 'Armies that are unbuildable'\n\t\t* The armies' potential, potential_country, or allow start with 'always = no'\n"
    issue_string += f"\t- 'Armies with Odd Properties'\n\t\t* The army is one of the following: defensive, occupation, rebel, or is_pop_spawned\n"
    issue_string += f"\t- 'Armies with Variable Manipulation'\n\t\t* The armies' potential_country, potential, allow, on_queued, on_unqueued, ai_weight_extra, or show_tech_unlock_if include some sort of variable effect or trigger"

    with open("pmca_issues.txt", "w") as fout:
        fout.write(issue_string)


def pmca() -> None:
    """Main function"""

    if os.path.isfile("input.txt"):
        # Don't need user input for these to work
        start1 = time.time()

        print("Setting up folders...")
        create_folders()

        print("Scanning input.txt...")
        scan_input_file()

        end1 = time.time()

        input_file_prefix = input(
            "\n\nEnter a custom file prefix, or leave blank to default to 'REPLACE_ME': "
        )

        file_prefix = input_file_prefix if input_file_prefix.strip() else "REPLACE_ME"

        input_mod_variable = input(
            "Enter the mod's id variable (Leave blank if making an external patch): "
        )
        if input_mod_variable.strip() and input_mod_variable.strip()[0] == "@":
            mod_variable = input_mod_variable.strip()
        else:
            mod_variable = (
                "@" + input_mod_variable
                if input_mod_variable.strip()
                else "@has_condensed_armies"
            )

        start2 = time.time()

        for army in list_of_armies:
            optimize_trigger(army)

        print("\n\nGenerating condensed army definitions...")
        generate_defs(file_prefix, mod_variable)

        print("Generating localisation...")
        generate_localisation_keys(file_prefix)

        end2 = time.time()
        time_duration1 = (end1 - start1) * 1000
        time_duration2 = (end2 - start2) * 1000

        comparison_army_list = []
        vanilla_set = set(vanilla_army_keys)
        for army in list_of_armies:
            comparison_army_list.append(army.army_name)
        modded_set = set(comparison_army_list)
        num_common_elements = vanilla_set.intersection(modded_set)

        print("Done! Please check './PMCA_GEN_OUTPUT/' for your Condensed Armies!\n")
        print("\n------------------------\n")
        print("Stats:")
        print(f"  - Number of Army Definitions: {len(list_of_armies)}")
        print(f"  - Number of Vanilla Overwrites: {len(num_common_elements)}")
        print(
            f"  - Number of languages supported by Stellaris: {len(stellaris_languages)}"
        )
        if file_prefix == "pmca_vanilla" or file_prefix == "pmca":
            print(
                f"  - Number of localisation keys generated: {len(list_of_armies) * 6 * len(stellaris_languages)} total | {len(list_of_armies) * 6} per file"
            )
        else:
            print(
                f"  - Number of localisation keys generated: {(len(list_of_armies) - len(num_common_elements)) * 6 * len(stellaris_languages)} total | {(len(list_of_armies) - len(num_common_elements)) * 6} per file"
            )
        print(
            f"  - Estimated time to complete: {round(time_duration1 + time_duration2, 3)} milliseconds\n"
        )

        scan_armies_for_issues()
        if (
            any(
                armies_with_issues[key]
                for key in ["Unbuildable", "Odd Property", "Variable Manipulation"]
            )
            and input(
                "Some armies were detected as having concerning properties, would you like to print them to 'pmca_issues.txt'? Y/N: "
            ).upper()[:1]
            == "Y"
        ):
            armies_with_issues_handler()

    else:
        print("ERROR: 'input.txt' was not found!")


if __name__ == "__main__":
    pmca()

# Common scripted variables for copy pasting
# @has_gigastructures
# @ESC_WEAPON_crystalline_s_t6_cost_crystals
# @has_ancient_caches
# @has_acquisition_of_tech
# @has_stellaris_evolved
# @slgt_Tier6_cost
