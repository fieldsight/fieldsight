let datass = [
    {
        "id": 820178,
        "name": "Site Selection",
        "json": {
            "name": "a3ho9BqYojW3KYeGnGZwvB_FvakXL0",
            "name": "Site Selection",
            "sms_keyword": "a3ho9BqYojW3KYeGnGZwvB",
            "default_language": "default",
            "version": "3883",
            "id_string": "a3ho9BqYojW3KYeGnGZwvB",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "geopoint",
                    "name": "location",
                    "label": "Location"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from geological fault or rupture areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_geological_fault_or_rupture_areas_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from landslide susceptible areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_landslide_susceptible_areas_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from liquefaction susceptible areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_liquefaction_susceptible_areas_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from river bank and water logged areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_river_bank_and_water_logged_area_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from rock fall areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_rock_fall_area_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the slope of the site more than 20% ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_slope_of_the_site_more_than_20_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo_",
                    "label": "Add photo."
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "3883"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 820176,
        "name": "NewForm",
        "json": {
            "name": "a2VwCXfM9ZiGX2nbqe4Ci9",
            "name": "NewForm",
            "sms_keyword": "a2VwCXfM9ZiGX2nbqe4Ci9",
            "default_language": "default",
            "version": "vosY9fmF2XmnVjpGYJE2Kc",
            "id_string": "a2VwCXfM9ZiGX2nbqe4Ci9",
            "type": "survey",
            "children": [
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "text",
                    "name": "About",
                    "label": "About"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "ghjkl",
                    "type": "select all that apply",
                    "children": [
                        {
                            "name": "kl",
                            "label": "kl;"
                        },
                        {
                            "name": "option_2",
                            "label": "Option 2"
                        },
                        {
                            "name": "option_3",
                            "label": "Option 3"
                        }
                    ],
                    "name": "ghjkl"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "image",
                    "label": "image?"
                },
                {
                    "bind": {
                        "relevant": "${About} != ''",
                        "required": "true"
                    },
                    "type": "integer",
                    "name": "phone_number",
                    "label": "phone number"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "datetime",
                    "name": "date",
                    "label": "date"
                },
                {
                    "bind": {
                        "calculate": "'vosY9fmF2XmnVjpGYJE2Kc'"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 820170,
        "name": "ticket",
        "json": {
            "name": "agxXgabHoQEQk45yiXoMq6",
            "name": "ticket",
            "sms_keyword": "agxXgabHoQEQk45yiXoMq6",
            "default_language": "default",
            "version": "vzcLpC3DBA65dUYkrciDNY",
            "id_string": "agxXgabHoQEQk45yiXoMq6",
            "type": "survey",
            "children": [
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "text",
                    "name": "caller",
                    "label": "caller"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "decimal",
                    "name": "minutre",
                    "label": "minutre"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "datetime",
                    "name": "date",
                    "label": "date"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "datetime",
                    "name": "fdasfasf",
                    "label": "fdasfasf"
                },
                {
                    "bind": {
                        "calculate": "'vzcLpC3DBA65dUYkrciDNY'"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20373,
        "name": "Plinth",
        "json": {
            "name": "aSPoHwmLR8uRuy82Rvt9x5_0dbhDJq",
            "name": "Plinth",
            "sms_keyword": "aSPoHwmLR8uRuy82Rvt9x5",
            "default_language": "default",
            "version": "4633",
            "id_string": "aSPoHwmLR8uRuy82Rvt9x5",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "geopoint",
                    "name": "location",
                    "label": "Location"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What is the type of building ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_and_rcc_b",
                            "label": "RCC A and RCC B"
                        },
                        {
                            "name": "confined_masonary",
                            "label": "Confined Masonry"
                        }
                    ],
                    "name": "What_is_the_type_of_building_"
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'smm'",
                        "required": "false"
                    },
                    "label": "Is the plinth of timber or house more than one storey?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_plinth_of_timber_or_house_more_than_one_storey_"
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'smm' or ${What_is_the_type_of_building_} = 'bmm'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the plinth of Timber or RC ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "rc",
                                    "label": "RC"
                                }
                            ],
                            "name": "Is_the_plinth_of_Timber_or_RC_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "How many storey is the building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "one_storey",
                                    "label": "One storey"
                                },
                                {
                                    "name": "one_storey_plus_attic",
                                    "label": "One storey plus attic"
                                },
                                {
                                    "name": "two_storey",
                                    "label": "Two storey"
                                }
                            ],
                            "name": "How_many_storey_is_the_buildin"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'timber' and ${How_many_storey_is_the_buildin} = 'one_storey'",
                                "required": "true"
                            },
                            "label": "Is the level of the plinth less than 300mm from ground level?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_plinth_less_than_300mm_from_ground_level_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'timber' and ${How_many_storey_is_the_buildin} = 'one_storey'",
                                "required": "true"
                            },
                            "label": "Are two 75mm x 38mm members used and connected with batten of the same size at a spacing of 500mm c/c or less?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Are_two_75mm_x_38mm_members_us"
                        },
                        {
                            "bind": {
                                "relevant": "${Are_two_75mm_x_38mm_members_us} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc' and ${How_many_storey_is_the_buildin} != 'two_storey'",
                                "required": "true"
                            },
                            "label": "Is the level of the plinth less than 300mm from ground level?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_plinth_less_than_300mm_from_ground_level__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc'",
                                "required": "true"
                            },
                            "label": "Is the thickness of the band 150mm for medium and soft soil or 75mm for hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_thickness_of_the_band_1"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thickness_of_the_band_1} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M15 grade or mix ratio 1:2:4?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m15_grade_or_mix_ratio_1_2_4_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc' and ${How_many_storey_is_the_buildin} != 'two_storey'",
                                "required": "true"
                            },
                            "label": "Is the main reinforcement 4 nos of 12mm dia rebars in case of 150mm thick plinth or 2 nos of 12mm dia rebars in case of 75mm plinth with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_main_reinforcement_4_no"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_main_reinforcement_4_no} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc'",
                                "required": "true"
                            },
                            "label": "Is the width of the band at least equal to the width of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_band_at_least_equal_to_the_width_of_the_wall_"
                        }
                    ],
                    "name": "group_jm5yj65"
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'bmm' and ${Is_the_plinth_of_Timber_or_RC_} = 'rc' and ${How_many_storey_is_the_buildin} != 'two_storey'",
                        "required": "false"
                    },
                    "label": "Is the level of the plinth less than 300mm from ground level?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_level_of_the_plinth_less_than_300mm_from_ground_level__0_0"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_sx4sf08",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'smc'"
                    },
                    "label": "SMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the level of the plinth less than 300mm from ground level?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_plinth_less_than_300mm_from_ground_level__0_0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the thickness of the band atleast 150mm for medium and soft soil or atleast 75mm for hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_thickness_of_the_band_atleast_150mm_for_medium_and_soft_soil_or_atleast_75mm_for_hard_soil_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the band at least equal to the width of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_band_at_least_equal_to_the_width_of_the_wall__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the plinth of Timber or RC ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Timber"
                                },
                                {
                                    "name": "no",
                                    "label": "RC"
                                }
                            ],
                            "name": "Is_the_plinth_of_Timber_or_RC__001"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'smc'"
                    },
                    "label": "SMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC__001} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the main reinforcement 4 nos of 12mm dia rebars in case of 150mm thick plinth or 2 nos of 12mm dia rebars in case of 75mm plinth with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_main_reinforcement_4_no_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_main_reinforcement_4_no_001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_main_reinforcement_4_no_001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0"
                        }
                    ],
                    "name": "group_fr3ya64"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_zt04a44",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'bmc'"
                    },
                    "label": "BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the level of the plinth less than 300mm from ground level?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_plinth_less_than_300mm_from_ground_level__0_0_0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the band at least equal to the width of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_band_at_least_equal_to_the_width_of_the_wall__0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the plinth of Timber or RC ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Timber"
                                },
                                {
                                    "name": "no",
                                    "label": "RC"
                                }
                            ],
                            "name": "Is_the_plinth_of_Timber_or_RC__002"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'bmc'"
                    },
                    "label": "BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC__002} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the thickness of the band 150m for medium and soft soil or 75mm for hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_thickness_of_the_band_1_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thickness_of_the_band_1_001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_clean_and_smooth__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC__002} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the main reinforcement 4 nos of 12mm dia rebars in case of 150mm thick plinth or 2 nos of 12mm dia rebars in case of 75mm plinth with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_main_reinforcement_4_no_002"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_main_reinforcement_4_no_002} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0"
                        }
                    ],
                    "name": "group_co8ar00"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_dm0rt83",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the height at least 450mm from Ground Level?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_at_least_450mm_from_ground_level_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size at least 9 inches X 9 inches?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_at_least_9_inches_x_9_inches_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Main rebar 4 numbers of 12 mm and 8 mm stirrups placed at 6 inches c/c?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_main_rebar_4_numbers_of_12_mm_and_8_mm_stirrups_placed_at_6_inches_c_c_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the splicing of bar equal to or less than 50% at one section and Splice/overlap length atleast 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_splicing_of_bar_equal_to_or_less_than_50_at_one_section_and_splice_overlap_length_atleast_60_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_nc7oo90",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc_a_and_rcc_b'"
                    },
                    "label": "RCC A and RCC B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of the plinth beam section as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_plinth_beam_section_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar size and detailings provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_size_and_detailings_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the connections provided adequate as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_connections_provided_adequate_as_per_approved_design_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_dk45x33",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'confined_masonary'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is plinth band provided?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_plinth_band_provided_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the plinth height more than 300mm from the existing ground level?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_plinth_height_more_than_300mm_from_the_existing_ground_level_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the plinth beam greater than or equal to 150mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_plinth_beam_greater_than_or_equal_to_150mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the plinth beam greater or equal to 200mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_plinth_beam_greater_or_equal_to_200mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the main reinforcement in the plinth, 4 bars of 10mm diameter and 7mm diameter rings provided at 150mm center to center with 50mm hook length and clear cover of 25mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_main_reinforcement_in_the_plinth_4_bars_of_10mm_diameter_and_7mm_diameter_rings_provided_at_150mm_center_to_center_with_50mm_hook_length_and_clear_cover_of_25mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement used of high strength deformed bars of Fe 415 MPa?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_used_of_high_strength_deformed_bars_of_fe_415_mpa_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_"
                        }
                    ]
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "photo",
                    "name": "add_photo",
                    "label": "Add photo"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo_0",
                    "label": "Add photo"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo_0_0",
                    "label": "Add photo"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4633"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20372,
        "name": "Vertical Member",
        "json": {
            "name": "aoc8YbB3Ur7CEpjvFpvGou_f5CeHtr",
            "name": "Vertical Member",
            "sms_keyword": "aoc8YbB3Ur7CEpjvFpvGou",
            "default_language": "default",
            "version": "4833",
            "id_string": "aoc8YbB3Ur7CEpjvFpvGou",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Which type of Building is it ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a___b",
                            "label": "RCC A & B"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        }
                    ],
                    "name": "Which_type_of_Building_is_it_"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_fp8sh06",
                    "bind": {
                        "relevant": "${Which_type_of_Building_is_it_} = 'smm' or ${Which_type_of_Building_is_it_} = 'bmm'"
                    },
                    "label": "SMM & BMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member placed at all corners and junctions of walls and starting from the foundation and continuing upwards ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_and_junctions_of_walls_and_starting_from_the_foundation_and_continuing_upwards_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member placed adjacent to all doors and window openings?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_adjacent_to_all_doors_and_window_openings_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member Timber or Concrete?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Timber"
                                },
                                {
                                    "name": "no",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_Timber_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber_} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the vertical member at corner of size 75mm x 100mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member of timber and house more than one storey ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_of_timber_and_house_more_than_one_storey_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber_} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the vertical member adjacent to all doors and window openings two members of size 75mm x 100mm each ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_adjacent_to_all_doors_and_window_openings_two_members_of_size_75mm_x_100mm_each_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber_} = 'no'",
                                "required": "false"
                            },
                            "label": "Is the vertical member at corner and intersections one bar of at least 12mm dia and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the concrete at least M15 grade or mix ratio 1:2:4 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m15_grade_or_mix_ratio_1_2_4_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${Which_type_of_Building_is_it_} = 'confined_masonry'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there a Tie column provided at each corners, wall intersections and on either side of the doors, which is starting from the foundation and continuing upwards?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_a_tie_column_provided_at_each_corners_wall_intersections_and_on_either_side_of_the_doors_which_is_starting_from_the_foundation_and_continuing_upwards_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical reinforcement in Tie column at least 4 bars of 12mm diameter and 7mm diameter bar stirrups placed at 150mm center to center?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_reinforcement_in_tie_column_at_least_4_bars_of_12mm_diameter_and_7mm_diameter_bar_stirrups_placed_at_150mm_center_to_center_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement used of high strength deformed bars of Fe 415 MPa ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_used_of_high_strength_deformed_bars_of_fe_415_mpa_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_"
                        }
                    ],
                    "name": "group_kd87s93"
                },
                {
                    "bind": {
                        "relevant": "${Which_type_of_Building_is_it_} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the pillar aligned in one line ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_pillar_aligned_in_one_line_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the pillar size at least 12 inches X 12 inches?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_pillar_size_at_least_12_inches_x_12_inches_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar at ground and first floor 4 numbers of 16mm + 4 numbers of 12 mm and third floor 8 numbers of 12 mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_at_ground_and_first_floor_4_numbers_of_16mm_4_numbers_of_12_mm_and_third_floor_8_numbers_of_12_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the stirrups at least 8mm dia and at 4 inch c/c at ends and joints and 6 inch at middle?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_stirrups_atleast_8mm_dia_and_at_4_inch_c_c_at_ends_and_joints_and_6_inch_at_middle_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Lapping in the middle leaving 2 ft from edge and not more than 50% at one section and overlap of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_lapping_in_the_middle_leaving_2_ft_from_edge_and_not_more_than_50_at_one_section_and_overlap_of_60_"
                        }
                    ],
                    "name": "group_gu5yt86"
                },
                {
                    "bind": {
                        "relevant": "${Which_type_of_Building_is_it_} = 'rcc_a___b'"
                    },
                    "label": "RCC A & B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the size of the pillar section as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_pillar_section_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar size and detailings provided as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_size_and_detailings_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the ring provided as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_ring_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the connections provided adequate as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_connections_provided_adequate_as_per_approved_design_"
                        }
                    ],
                    "name": "group_xi1sd13"
                },
                {
                    "bind": {
                        "relevant": "${Which_type_of_Building_is_it_} = 'smc'"
                    },
                    "label": "SMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member placed at all corners, junctions of walls, and adjacent to all openings and starting from the foundation and continuing upwards?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_junctions_of_walls_and_adjacent_to_all_openings_and_starting_from_the_foundation_and_continuing_upwards_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member Timber or Concrete?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Timber"
                                },
                                {
                                    "name": "no",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_Timber__001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber_} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the house one storey ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_house_one_storey_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_house_one_storey_} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner,intersections and adjacent to openings one bar of at least 12mm dia and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_002"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_002} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_002} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_house_one_storey_} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of atleast 16mm dia and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_003"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_003} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_003} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa__0"
                        }
                    ],
                    "name": "group_aj6il51"
                },
                {
                    "bind": {
                        "relevant": "${Which_type_of_Building_is_it_} = 'bmc'"
                    },
                    "label": "BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member placed at all corners, junctions of walls, and adjacent to all openings and starting from the foundation and continuing upwards ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_junctions_of_walls_and_adjacent_to_all_openings_and_starting_from_the_foundation_and_continuing_upwards__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member Timber or Concrete?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Timber"
                                },
                                {
                                    "name": "no",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "is_the_vertical_member_timber_or_concrete_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber__001} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the house one storey ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_house_one_storey_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_house_one_storey_} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of atleast 12mm dia and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_004"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_004} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_004} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_house_one_storey_} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of atleast 16mm dia and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_005"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_005} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_005} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0"
                        }
                    ],
                    "name": "group_cn6cg39"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0_0",
                    "label": "Add photo."
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4833"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20371,
        "name": "Foundation",
        "json": {
            "name": "aAzyZjhKCxy4cDVXV8zMxi_mEyFDoD",
            "name": "Foundation",
            "sms_keyword": "aAzyZjhKCxy4cDVXV8zMxi",
            "default_language": "default",
            "version": "4827",
            "id_string": "aAzyZjhKCxy4cDVXV8zMxi",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "geopoint",
                    "name": "location",
                    "label": "Location"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What is the type of building ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "bmm",
                            "label": "SMM (Stone Mud Masonry)"
                        },
                        {
                            "name": "smc",
                            "label": "SMC (Stone Masonry Cement)"
                        },
                        {
                            "name": "bmm_1",
                            "label": "BMM (Brick Mud Masonry)"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC (Brick Masonry Cement)"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC (Reinforced Cement Concrete)"
                        },
                        {
                            "name": "rcc_a_and_rcc_",
                            "label": "RCC A and RCC B (Reinforced Cement Concrete)"
                        },
                        {
                            "name": "confined_mason",
                            "label": "Confined Masonry"
                        }
                    ],
                    "name": "What_is_the_type_of_building_"
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} != 'rcc' and ${What_is_the_type_of_building_} != 'rcc_a_and_rcc_' and ${What_is_the_type_of_building_} != 'confined_mason'",
                        "required": "false"
                    },
                    "label": "Is the foundation new or old?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Old"
                        },
                        {
                            "name": "no",
                            "label": "New"
                        }
                    ],
                    "name": "Is_the_foundation_new_or_old"
                },
                {
                    "bind": {
                        "relevant": "${Is_the_foundation_new_or_old} = 'yes'",
                        "required": "false"
                    },
                    "label": "Is the existing foundation damaged or settled?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "Is_the_existing_foundation_dam"
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} != 'rcc' and ${What_is_the_type_of_building_} != 'rcc_a_and_rcc_' and ${What_is_the_type_of_building_} != 'confined_mason' and ${Is_the_existing_foundation_dam} = 'no'",
                        "required": "false"
                    },
                    "label": "Is there a good connection between the old foundation and new masonry work?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_there_a_good_connection_between_the_old_foundation_and_new_masonry_work_"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ko0ct18",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'bmm'"
                    },
                    "label": "SMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the foundation continuous and at the same level throughout the foundation in flat area?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_foundation_continuous_and_at_the_same_level_throughout_the_foundation_in_flat_area_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Are the stones rounded, not-dressed, easily breakable soft stone and boulder stones in its natural shape?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_stones_rounded_not_dressed_easily_breakable_soft_stone_and_boulder_stones_in_its_natural_shape_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Are the stones smaller than 50mm in thickness and 150 mm in length or breadth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_stones_smaller_than_50mm_in_thickness_and_150_mm_in_length_or_breadth_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the Mud mortar free from organic materials, pebbles, hard materials?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mud_mortar_free_from_organic_materials_pebbles_hard_materials_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 750mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_750mm_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the width of the base of foundation greater than 800mm in soft soil/ greater than 750mm in medium to hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_800mm_in_soft_soil_greater_than_750mm_in_medium_to_hard_soil_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the width of the wall at the plinth beam 350mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_350mm_or_more_"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'smc'"
                    },
                    "label": "SMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the foundation continuous and at the same level throughout the foundation in flat area?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_foundation_continuous_and_at_the_same_level_throughout_the_foundation_in_flat_area__0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "How many storeys is the building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "one_storey",
                                    "label": "One storey"
                                },
                                {
                                    "name": "more_than_one_storey",
                                    "label": "More than one storey"
                                },
                                {
                                    "name": "more_than_two_plus_attic",
                                    "label": "More than two plus attic"
                                }
                            ],
                            "name": "How_many_storeys_is_the_buildi"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi} = 'one_storey'",
                                "required": "false"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 800mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_depth_of_the_foundation"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_depth_of_the_foundation} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the width of the base of foundation greater than 800mm in soft soil/ greater than 600mm in medium to hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_800mm_in_soft_soil_greater_than_600mm_in_medium_to_hard_soil_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi} = 'one_storey'",
                                "required": "false"
                            },
                            "label": "Is the width of the wall at the plinth beam level 350mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_level_350mm_or_more_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi} = 'more_than_one_storey'",
                                "required": "false"
                            },
                            "label": "Is the type of soil soft?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_type_of_soil_soft"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_type_of_soil_soft} = 'no'",
                                "required": "false"
                            },
                            "label": "Is the width of the base of foundation greater than 800mm in medium soil/ greater than 600mm in hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_800mm_in_medium_soil_greater_than_600mm_in_hard_soil_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the width of the wall at the plinth beam level 450 mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_level_450_mm_or_more_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi} = 'more_than_one_storey' or ${How_many_storeys_is_the_buildi} = 'more_than_two_plus_attic'",
                                "required": "false"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 900mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_900mm_"
                        }
                    ],
                    "name": "group_yj6ec41"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_yk9ho24",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'bmm_1'"
                    },
                    "label": "BMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the foundation continuous and at the same level throughout the foundation in flat area?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_foundation_continuous_and_at_the_same_level_throughout_the_foundation_in_flat_area__0_0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Has Overburnt, underburnt, deformed bricks used?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "has_overburnt_underburnt_deformed_bricks_used_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the Mud mortar free from organic materials, pebbles, hard materials?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mud_mortar_free_from_organic_materials_pebbles_hard_materials__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Mud mortar free from organic materials, pebbles, hard materials?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mud_mortar_free_from_organic_materials_pebbles_hard_materials__0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 750mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_750mm__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the base of foundation greater than 750mm in soft soil/ greater than 650mm in medium soil and greater than 550mm in hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_750mm_in_soft_soil_greater_than_650mm_in_medium_soil_and_greater_than_550mm_in_hard_soil_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the wall at the plinth beam 350 mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_350_mm_or_more_"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'bmc'"
                    },
                    "label": "BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the foundation continuous and at the same level throughout the foundation in flat area?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_foundation_continuous_and_at_the_same_level_throughout_the_foundation_in_flat_area__0_0_0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "How many storeys is the building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "one_storey",
                                    "label": "One storey"
                                },
                                {
                                    "name": "more_than_one_storey",
                                    "label": "More than one storey"
                                }
                            ],
                            "name": "How_many_storeys_is_the_buildi_001"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'one_storey'",
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 800mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_800mm_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'one_storey'",
                                "required": "true"
                            },
                            "label": "Is the width of the base of foundation greater than 650mm in soft soil/ greater than 550mm in medium to hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_650mm_in_soft_soil_greater_than_550mm_in_medium_to_hard_soil_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'one_storey'",
                                "required": "false"
                            },
                            "label": "Is the width of the wall at the plinth beam 230mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_230mm_or_more_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'more_than_one_storey'",
                                "required": "true"
                            },
                            "label": "Is the width of the base of foundation greater than 900mm in soft soil/greater than 650 in medium soil/ greater than 550mm in hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_900mm_in_soft_soil_greater_than_650_in_medium_soil_greater_than_550mm_in_hard_soil_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'more_than_one_storey'",
                                "required": "false"
                            },
                            "label": "Is the width of the wall below the plinth beam 350mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_below_the_plinth_beam_350mm_or_more_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Has Overburnt, underburnt, deformed bricks used?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "has_overburnt_underburnt_deformed_bricks_used__0"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'more_than_one_storey'",
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 900mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_900mm__0"
                        }
                    ],
                    "name": "group_ar8ed89"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_kg1zs39",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the depth at least 5 ft?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_at_least_5_ft_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Choose the type of soil from the options below",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Loose"
                                },
                                {
                                    "name": "no",
                                    "label": "Soft"
                                },
                                {
                                    "name": "medium",
                                    "label": "Medium"
                                },
                                {
                                    "name": "hard",
                                    "label": "Hard"
                                }
                            ],
                            "name": "Choose_the_type_of_soil_from_t"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_gy92w74",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc' and ${Choose_the_type_of_soil_from_t} = 'yes'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at corner loose soil >2.2 m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_corner_loose_soil_2_2_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at front loose soil >2.4m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_front_loose_soil_2_4m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at mid loose soil >3m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_mid_loose_soil_3m_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ar1cn18",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc' and ${Choose_the_type_of_soil_from_t} = 'no'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at corner soft soil >1.5m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_corner_soft_soil_1_5m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at front soft soil >1.65m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_front_soft_soil_1_65m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at mid soft soil >2.1 m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_mid_soft_soil_2_1_m_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ot3xc38",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc' and ${Choose_the_type_of_soil_from_t} = 'medium'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'medium'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at corner medium soil >1.25m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_corner_medium_soil_1_25m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'medium'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at front medium soil >1.4m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_front_medium_soil_1_4m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'medium'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at mid medium soil >1.7 m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_mid_medium_soil_1_7_m_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_et8mt69",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc' and ${Choose_the_type_of_soil_from_t} = 'hard'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'hard'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at corner hard soil >1.2m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_corner_hard_soil_1_2m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'hard'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at front hard soil >1.1 m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_front_hard_soil_1_1_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'hard'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at mid hard soil >1.5 m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_mid_hard_soil_1_5_m_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_or3ei60",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar at base of the foundation at least 12mm Dia?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_at_base_of_the_foundation_at_least_12mm_dia_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the footing 400 mm in middle and 300 mm in other sides?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_footing_400_mm_in_middle_and_300_mm_in_other_sides_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the beam of the foundation atleast 9 inch X 9 inch with 4 numbers of 12mm dia rebar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mud_mortar_free_from_organic_materials_pebbles_hard_materials__0_0_0"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc_a_and_rcc_'"
                    },
                    "label": "RCC A and RCC B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the type of foundation as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_type_of_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of foundation as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar provided in the foundation as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_provided_in_the_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the foundation as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the bottom tie beam required as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_bottom_tie_beam_require"
                        }
                    ],
                    "name": "group_qw1kn28"
                },
                {
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc_a_and_rcc_'"
                    },
                    "label": "RCC A and RCC B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${Is_the_bottom_tie_beam_require} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the size of the beam section as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_beam_section_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_bottom_tie_beam_require} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar size and detailings provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_size_and_detailings_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design_"
                        }
                    ],
                    "name": "group_gb3ks87"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_sn7tp62",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'confined_mason'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the foundation continuous and at the same level throughout the foundation in flat area?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_foundation_continuous_and_at_the_same_level_throughout_the_foundation_in_flat_area__0_0_0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation less than 900mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_less_than_900mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of footing 900mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_footing_900mm_or_more_"
                        }
                    ]
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo_",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0",
                    "label": "Add photo."
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4827"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20370,
        "name": "Materials",
        "json": {
            "name": "aX7z7qrbyC8gMw4WrvkTbP_EnBeKLz",
            "name": "Materials",
            "sms_keyword": "aX7z7qrbyC8gMw4WrvkTbP",
            "default_language": "default",
            "version": "4640",
            "id_string": "aX7z7qrbyC8gMw4WrvkTbP",
            "type": "survey",
            "children": [
                {
                    "label": "Group",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What type of Building is it ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "smm",
                                    "label": "SMM"
                                },
                                {
                                    "name": "smc",
                                    "label": "SMC"
                                },
                                {
                                    "name": "bmm",
                                    "label": "BMM"
                                },
                                {
                                    "name": "bmc",
                                    "label": "BMC"
                                },
                                {
                                    "name": "rcc",
                                    "label": "RCC"
                                },
                                {
                                    "name": "rcc_a___b",
                                    "label": "RCC A & B"
                                },
                                {
                                    "name": "confined_masonry",
                                    "label": "Confined Masonry"
                                }
                            ],
                            "name": "What_type_of_Building_is_it_"
                        }
                    ],
                    "name": "group_zd69a59"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_Building_is_it_} = 'rcc'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the mortar ratio atleast 1:4 for 4\" wall and 1:6 for thicker wall ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_atleast_1_4_for_4_wall_and_1_6_for_thicker_wall_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                        }
                    ],
                    "name": "group_mq7kq25"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_Building_is_it_} = 'rcc_a___b'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the mortar ratio atleast 1:4 for 4\" wall and 1:6 for thicker wall ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_atleast_1_4_for_4_wall_and_1_6_for_thicker_wall__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete mix and quality as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_mix_and_quality_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0"
                        }
                    ],
                    "name": "group_jg4rk12"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_Building_is_it_} = 'confined_masonry'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the mortar ratio 1:5 or richer ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_1_5_or_richer_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy 415Mpa or Fy 500 Mpa with overlap length of 60 times the diameter of the bar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_or_fy_500_mpa_with_overlap_length_of_60_times_the_diameter_of_the_bar_"
                        }
                    ],
                    "name": "group_st4se99"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4640"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20369,
        "name": "Shape and Size",
        "json": {
            "name": "amBo4gEipk4cMRXDPW4ZTR_7HQmrxs",
            "name": "Shape and Size",
            "sms_keyword": "amBo4gEipk4cMRXDPW4ZTR",
            "default_language": "default",
            "version": "4826",
            "id_string": "amBo4gEipk4cMRXDPW4ZTR",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "geopoint",
                    "name": "location",
                    "label": "Location"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What is the type of building ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM (Stone Mud Mortar)"
                        },
                        {
                            "name": "smc",
                            "label": "SMC (Stone Masonry Cement)"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM (Brick Mud Masonry)"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC (Brick Masonry Cement)"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC (Reinforced Concrete Cement)"
                        },
                        {
                            "name": "rcc_a_and_rcc_b",
                            "label": "RCC A &B (Reinforced Concrete Cement)"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        }
                    ],
                    "name": "What_is_the_type_of_building_"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_mf24f05",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} != 'rcc' and ${What_is_the_type_of_building_} != 'rcc_a_and_rcc_b' and ${What_is_the_type_of_building_} != 'confined_masonry'"
                    },
                    "label": "SMM/SMC/BMM/BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the clear span of wall more than 4.5 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_clear_span_of_wall_more_than_4_5_m_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the building simple and regular shaped?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_building_simple_and_regular_shaped_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the length of the building more than 3 times of its width ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_of_the_building_more_than_3_times_of_its_width_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the size of the room more than 13.5 sq.m.?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_room_more_than_13_5_sq_m_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_hm7wx57",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the house limited up to 3 floor ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_house_limited_up_to_3_floor_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the number of bay two to six ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_number_of_bay_two_to_six_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the area less than 1000 sq. ft and area in between 4 pillars 13.5 sq m only ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_area_less_than_1000_sq_ft_and_area_in_between_4_pillars_13_5_sq_m_only_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the Total height of building less than 11m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_total_height_of_building_less_than_11m_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the height of floor from 2.75 m to 3.35 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_floor_from_2_75_m_to_3_35_m_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the shape square or rectangular ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_shape_square_or_rectangular_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the ratio of length less than 3 times the breadth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_ratio_of_length_less_than_3_times_the_breadth_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_wc4ft28",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc_a_and_rcc_b'"
                    },
                    "label": "Pictures of each page of Approved design adopted",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_1",
                            "label": "Photo 1"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_2",
                            "label": "Photo 2"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_3",
                            "label": "Photo 3"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_4",
                            "label": "Photo 4"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_5",
                            "label": "Photo 5"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_fv0sw35",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc_a_and_rcc_b'"
                    },
                    "label": "RCC A and RCC B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the number of bays as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_number_of_bays_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the building area as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_building_area_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the Total height of building less than 11m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_total_height_of_building_less_than_11m__0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the length of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_of_the_building_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the breadth of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_breadth_of_the_building_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the storey height of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_storey_height_of_the_building_as_per_approved_design_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_fp83b97",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'confined_masonry'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the maximum span of the wall more than 3.5 meters ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_maximum_span_of_the_wall_more_than_3_5_meters_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the house either a square or a rectangle ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_house_either_a_square_or_a_rectangle_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the length to breadth ratio of the structure more than 3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_to_breadth_ratio_of_the_structure_more_than_3_"
                        }
                    ]
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4826"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20368,
        "name": "Site Selection",
        "json": {
            "name": "aGBTDXVGZy4c9NVWAiTYVL_epC1RC5",
            "name": "Site Selection",
            "sms_keyword": "aGBTDXVGZy4c9NVWAiTYVL",
            "default_language": "default",
            "version": "4812",
            "id_string": "aGBTDXVGZy4c9NVWAiTYVL",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "geopoint",
                    "name": "location",
                    "label": "Location"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from geological fault or rupture areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_geological_fault_or_rupture_areas_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from landslide susceptible areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_landslide_susceptible_areas_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from liquefaction susceptible areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_liquefaction_susceptible_areas_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from river bank and water logged areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_river_bank_and_water_logged_area_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the site away from rock fall areas ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_site_away_from_rock_fall_area_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the slope of the site more than 20% ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "is_the_slope_of_the_site_more_than_20_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo",
                    "label": "Add photo"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4812"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 297299,
        "name": "New Construction Measurement Final",
        "json": {
            "name": "anN4nbZdNDdBNhDmCfyPsf_7GaUByQ",
            "name": "New Construction Measurement Final",
            "sms_keyword": "anN4nbZdNDdBNhDmCfyPsf",
            "default_language": "default",
            "version": "24631",
            "id_string": "anN4nbZdNDdBNhDmCfyPsf",
            "type": "survey",
            "children": [
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "General Information",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "date",
                            "name": "date",
                            "label": "Date"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "geopoint",
                            "name": "gps",
                            "label": "GPS Coordinate of House"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "data_collector",
                            "label": "Name Of Data Collector"
                        }
                    ],
                    "name": "info"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "How many Grid lines are there in the Horizontal Direction?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "2",
                            "label": "2"
                        },
                        {
                            "name": "3",
                            "label": "3"
                        },
                        {
                            "name": "4",
                            "label": "4"
                        },
                        {
                            "name": "5",
                            "label": "5"
                        },
                        {
                            "name": "6",
                            "label": "6"
                        }
                    ],
                    "name": "no_of_horizontal_grid"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "Horizontal Grids",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${no_of_horizontal_grid} != ''",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_ab",
                            "label": "Distance between grids A-B"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_horizontal_grid} = '6' or ${no_of_horizontal_grid} = '5' or ${no_of_horizontal_grid} = '4' or ${no_of_horizontal_grid} = '3'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_bc",
                            "label": "Distance between grids B-C"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_horizontal_grid} = '6' or ${no_of_horizontal_grid} = '5' or ${no_of_horizontal_grid} = '4'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_cd",
                            "label": "Distance between grids C-D"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_horizontal_grid} = '6' or ${no_of_horizontal_grid} = '5'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_de",
                            "label": "Distance between grids D-E"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_horizontal_grid} = '6'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_ef",
                            "label": "Distance between grids E-F"
                        }
                    ],
                    "name": "horizontal_grid"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "How many Grid lines are there in the Vertical Direction?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "2",
                            "label": "2"
                        },
                        {
                            "name": "3",
                            "label": "3"
                        },
                        {
                            "name": "4",
                            "label": "4"
                        },
                        {
                            "name": "5",
                            "label": "5"
                        },
                        {
                            "name": "6",
                            "label": "6"
                        }
                    ],
                    "name": "no_of_vertical_grid"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "Verticals Grid",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${no_of_vertical_grid} != ''",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_12",
                            "label": "Distance between grids 1-2"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_vertical_grid} = '3' or ${no_of_vertical_grid} = '4' or ${no_of_vertical_grid} = '5' or ${no_of_vertical_grid} = '6'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_23",
                            "label": "Distance between grids 2-3"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_vertical_grid} = '4' or ${no_of_vertical_grid} = '5' or ${no_of_vertical_grid} = '6'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_34",
                            "label": "Distance between grids 3-4"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_vertical_grid} = '5' or ${no_of_vertical_grid} = '6'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_45",
                            "label": "Distance between grids 4-5"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_vertical_grid} = '6'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "distance_56",
                            "label": "Distance between grids 5-6"
                        }
                    ],
                    "name": "vertical_grid"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "How many levels are there? (excluding Roof)",
                    "type": "select one",
                    "children": [
                        {
                            "name": "1",
                            "label": "0"
                        },
                        {
                            "name": "2",
                            "label": "1"
                        },
                        {
                            "name": "3",
                            "label": "2"
                        }
                    ],
                    "name": "level"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "Levels",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "level1_height",
                            "label": "Height from ground floor to level 1?"
                        },
                        {
                            "bind": {
                                "relevant": "${level} = '3'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "level_1to2_height",
                            "label": "Height from level 1 to level 2?"
                        },
                        {
                            "bind": {
                                "relevant": "${level} = '2' or ${level} = '3'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "upper_wall_height",
                            "label": "Wall height on Upper Floor?"
                        }
                    ],
                    "name": "levels"
                },
                {
                    "label": "Roof",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What kind of roof is it?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "gabled",
                                    "label": "Gabled"
                                },
                                {
                                    "name": "pitched",
                                    "label": "Pitched"
                                },
                                {
                                    "name": "flat",
                                    "label": "Flat"
                                }
                            ],
                            "name": "type_of_roof"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_roof} = 'gabled'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "ridge_height",
                            "label": "Ridge Height from Upper level floor"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_roof} = 'pitched'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "upper_roof_height",
                            "label": "Upper Roof height Dimension"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_roof} = 'pitched'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "lower_roof_height",
                            "label": "Lower Roof Height Dimension"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_roof} = 'pitched'",
                                "required": "true"
                            },
                            "type": "text",
                            "name": "high_roof_grid",
                            "label": "Along which grid is the high roof edge?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "roof_overhang",
                            "label": "Roof overhang dimension"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Roof material type",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "concrete",
                                    "label": "Concrete"
                                },
                                {
                                    "name": "wood_with_cgi",
                                    "label": "Wood framing with CGI"
                                },
                                {
                                    "name": "wood_with_clay",
                                    "label": "Wood framing with Clay tile"
                                }
                            ],
                            "name": "roof_material_type"
                        }
                    ],
                    "name": "roof"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "What kind of house is it?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_ab",
                            "label": "RCC AB"
                        },
                        {
                            "name": "cm",
                            "label": "Confined Masonary"
                        }
                    ],
                    "name": "type_of_house"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "rccolumn_grnd_flr",
                    "bind": {
                        "relevant": "${type_of_house} = 'rcc_ab' or ${type_of_house} = 'rcc'"
                    },
                    "label": "RC Column Details at Ground Floor",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "no_of_column_grnd_floor",
                            "label": "How many RC Columns are there on ground floor?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What are the grid intersection locations?",
                            "type": "select all that apply",
                            "children": [
                                {
                                    "name": "1a",
                                    "label": "1-A"
                                },
                                {
                                    "name": "1b",
                                    "label": "1-B"
                                },
                                {
                                    "name": "1c",
                                    "label": "1-C"
                                },
                                {
                                    "name": "1d",
                                    "label": "1-D"
                                },
                                {
                                    "name": "1e",
                                    "label": "1-E"
                                },
                                {
                                    "name": "1f",
                                    "label": "1-F"
                                },
                                {
                                    "name": "2a",
                                    "label": "2-A"
                                },
                                {
                                    "name": "2b",
                                    "label": "2-B"
                                },
                                {
                                    "name": "2c",
                                    "label": "2-C"
                                },
                                {
                                    "name": "2d",
                                    "label": "2-D"
                                },
                                {
                                    "name": "2e",
                                    "label": "2-E"
                                },
                                {
                                    "name": "2f",
                                    "label": "2-F"
                                },
                                {
                                    "name": "3a",
                                    "label": "3-A"
                                },
                                {
                                    "name": "3b",
                                    "label": "3-B"
                                },
                                {
                                    "name": "3c",
                                    "label": "3-C"
                                },
                                {
                                    "name": "3d",
                                    "label": "3-D"
                                },
                                {
                                    "name": "3e",
                                    "label": "3-E"
                                },
                                {
                                    "name": "3f",
                                    "label": "3-F"
                                },
                                {
                                    "name": "4a",
                                    "label": "4-A"
                                },
                                {
                                    "name": "4b",
                                    "label": "4-B"
                                },
                                {
                                    "name": "4c",
                                    "label": "4-C"
                                },
                                {
                                    "name": "4d",
                                    "label": "4-D"
                                },
                                {
                                    "name": "4e",
                                    "label": "4-E"
                                },
                                {
                                    "name": "4f",
                                    "label": "4-F"
                                },
                                {
                                    "name": "5a",
                                    "label": "5-A"
                                },
                                {
                                    "name": "5b",
                                    "label": "5-B"
                                },
                                {
                                    "name": "5c",
                                    "label": "5-C"
                                },
                                {
                                    "name": "5d",
                                    "label": "5-D"
                                },
                                {
                                    "name": "5e",
                                    "label": "5-E"
                                },
                                {
                                    "name": "5f",
                                    "label": "5-F"
                                },
                                {
                                    "name": "6a",
                                    "label": "6-A"
                                },
                                {
                                    "name": "6b",
                                    "label": "6-B"
                                },
                                {
                                    "name": "6c",
                                    "label": "6-C"
                                },
                                {
                                    "name": "6d",
                                    "label": "6-D"
                                },
                                {
                                    "name": "6e",
                                    "label": "6-E"
                                },
                                {
                                    "name": "6f",
                                    "label": "6-F"
                                }
                            ],
                            "name": "grid_locations_grndflr"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "ground_floor_column_width",
                            "label": "Typical Width of Columns on Ground floor (choose 1 column that is most like the others)?"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "rccolumn_1stflr",
                    "bind": {
                        "relevant": "(${type_of_house} = 'rcc' or ${type_of_house} = 'rcc_ab')and(${level}='3')"
                    },
                    "label": "RC Column Details at First Floor",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "no_of_column_1st_floor",
                            "label": "How many columns are there on the First floor (between level 1 to 2)?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What are the grid intersection locations?",
                            "type": "select all that apply",
                            "children": [
                                {
                                    "name": "1a",
                                    "label": "1-A"
                                },
                                {
                                    "name": "1b",
                                    "label": "1-B"
                                },
                                {
                                    "name": "1c",
                                    "label": "1-C"
                                },
                                {
                                    "name": "1d",
                                    "label": "1-D"
                                },
                                {
                                    "name": "1e",
                                    "label": "1-E"
                                },
                                {
                                    "name": "1f",
                                    "label": "1-F"
                                },
                                {
                                    "name": "2a",
                                    "label": "2-A"
                                },
                                {
                                    "name": "2b",
                                    "label": "2-B"
                                },
                                {
                                    "name": "2c",
                                    "label": "2-C"
                                },
                                {
                                    "name": "2d",
                                    "label": "2-D"
                                },
                                {
                                    "name": "2e",
                                    "label": "2-E"
                                },
                                {
                                    "name": "2f",
                                    "label": "2-F"
                                },
                                {
                                    "name": "3a",
                                    "label": "3-A"
                                },
                                {
                                    "name": "3b",
                                    "label": "3-B"
                                },
                                {
                                    "name": "3c",
                                    "label": "3-C"
                                },
                                {
                                    "name": "3d",
                                    "label": "3-D"
                                },
                                {
                                    "name": "3e",
                                    "label": "3-E"
                                },
                                {
                                    "name": "3f",
                                    "label": "3-F"
                                },
                                {
                                    "name": "4a",
                                    "label": "4-A"
                                },
                                {
                                    "name": "4b",
                                    "label": "4-B"
                                },
                                {
                                    "name": "4c",
                                    "label": "4-C"
                                },
                                {
                                    "name": "4d",
                                    "label": "4-D"
                                },
                                {
                                    "name": "4e",
                                    "label": "4-E"
                                },
                                {
                                    "name": "4f",
                                    "label": "4-F"
                                },
                                {
                                    "name": "5a",
                                    "label": "5-A"
                                },
                                {
                                    "name": "5b",
                                    "label": "5-B"
                                },
                                {
                                    "name": "5c",
                                    "label": "5-C"
                                },
                                {
                                    "name": "5d",
                                    "label": "5-D"
                                },
                                {
                                    "name": "5e",
                                    "label": "5-E"
                                },
                                {
                                    "name": "5f",
                                    "label": "5-F"
                                },
                                {
                                    "name": "6a",
                                    "label": "6-A"
                                },
                                {
                                    "name": "6b",
                                    "label": "6-B"
                                },
                                {
                                    "name": "6c",
                                    "label": "6-C"
                                },
                                {
                                    "name": "6d",
                                    "label": "6-D"
                                },
                                {
                                    "name": "6e",
                                    "label": "6-E"
                                },
                                {
                                    "name": "6f",
                                    "label": "6-F"
                                }
                            ],
                            "name": "grid_locations_1stflr"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "frst_floor_column_width",
                            "label": "Typical Width of Columns on First floor (choose 1 column that is most like the others)?"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "rccolumn_uprflr",
                    "bind": {
                        "relevant": "(${type_of_house} = 'rcc' or ${type_of_house} = 'rcc_ab')and(${level}='3' or ${level}='2')"
                    },
                    "label": "RC Column Details at Upper Floor",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "no_of_column_upr_floor",
                            "label": "How many columns are there on the Upper floor ?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What are the grid intersection locations?",
                            "type": "select all that apply",
                            "children": [
                                {
                                    "name": "1a",
                                    "label": "1-A"
                                },
                                {
                                    "name": "1b",
                                    "label": "1-B"
                                },
                                {
                                    "name": "1c",
                                    "label": "1-C"
                                },
                                {
                                    "name": "1d",
                                    "label": "1-D"
                                },
                                {
                                    "name": "1e",
                                    "label": "1-E"
                                },
                                {
                                    "name": "1f",
                                    "label": "1-F"
                                },
                                {
                                    "name": "2a",
                                    "label": "2-A"
                                },
                                {
                                    "name": "2b",
                                    "label": "2-B"
                                },
                                {
                                    "name": "2c",
                                    "label": "2-C"
                                },
                                {
                                    "name": "2d",
                                    "label": "2-D"
                                },
                                {
                                    "name": "2e",
                                    "label": "2-E"
                                },
                                {
                                    "name": "2f",
                                    "label": "2-F"
                                },
                                {
                                    "name": "3a",
                                    "label": "3-A"
                                },
                                {
                                    "name": "3b",
                                    "label": "3-B"
                                },
                                {
                                    "name": "3c",
                                    "label": "3-C"
                                },
                                {
                                    "name": "3d",
                                    "label": "3-D"
                                },
                                {
                                    "name": "3e",
                                    "label": "3-E"
                                },
                                {
                                    "name": "3f",
                                    "label": "3-F"
                                },
                                {
                                    "name": "4a",
                                    "label": "4-A"
                                },
                                {
                                    "name": "4b",
                                    "label": "4-B"
                                },
                                {
                                    "name": "4c",
                                    "label": "4-C"
                                },
                                {
                                    "name": "4d",
                                    "label": "4-D"
                                },
                                {
                                    "name": "4e",
                                    "label": "4-E"
                                },
                                {
                                    "name": "4f",
                                    "label": "4-F"
                                },
                                {
                                    "name": "5a",
                                    "label": "5-A"
                                },
                                {
                                    "name": "5b",
                                    "label": "5-B"
                                },
                                {
                                    "name": "5c",
                                    "label": "5-C"
                                },
                                {
                                    "name": "5d",
                                    "label": "5-D"
                                },
                                {
                                    "name": "5e",
                                    "label": "5-E"
                                },
                                {
                                    "name": "5f",
                                    "label": "5-F"
                                },
                                {
                                    "name": "6a",
                                    "label": "6-A"
                                },
                                {
                                    "name": "6b",
                                    "label": "6-B"
                                },
                                {
                                    "name": "6c",
                                    "label": "6-C"
                                },
                                {
                                    "name": "6d",
                                    "label": "6-D"
                                },
                                {
                                    "name": "6e",
                                    "label": "6-E"
                                },
                                {
                                    "name": "6f",
                                    "label": "6-F"
                                }
                            ],
                            "name": "grid_locations_uprflr"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "upr_floor_column_width",
                            "label": "Typical Width of Columns on Upper floor (choose 1 column that is most like the others)?"
                        }
                    ]
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "integer",
                    "name": "no_of_ground_walls",
                    "label": "How many total walls are there on ground floor?"
                },
                {
                    "bind": {
                        "readonly": "true()",
                        "calculate": "${no_of_ground_walls}"
                    },
                    "type": "calculate",
                    "name": "ground_wall_count"
                },
                {
                    "control": {
                        "jr:count": "${ground_wall_count}"
                    },
                    "name": "ground_wall",
                    "bind": {
                        "relevant": "${no_of_ground_walls} > 0"
                    },
                    "label": "Ground Floor Walls",
                    "type": "repeat",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "On which Grid line does the wall lie?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "3",
                                    "label": "3"
                                },
                                {
                                    "name": "4",
                                    "label": "4"
                                },
                                {
                                    "name": "5",
                                    "label": "5"
                                },
                                {
                                    "name": "6",
                                    "label": "6"
                                },
                                {
                                    "name": "a",
                                    "label": "A"
                                },
                                {
                                    "name": "b",
                                    "label": "B"
                                },
                                {
                                    "name": "c",
                                    "label": "C"
                                },
                                {
                                    "name": "d",
                                    "label": "D"
                                },
                                {
                                    "name": "e",
                                    "label": "E"
                                },
                                {
                                    "name": "f",
                                    "label": "F"
                                }
                            ],
                            "name": "grndwall_on_grid"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "grndwall_grid_intersection",
                            "label": "On which Grid intersection does the wall start?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there an Offset from that intersection?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "y",
                                    "label": "Yes"
                                },
                                {
                                    "name": "n",
                                    "label": "No"
                                }
                            ],
                            "name": "grnd_offset"
                        },
                        {
                            "bind": {
                                "relevant": "${grnd_offset} = 'y'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "grndoffset_dimension",
                            "label": "What is the offset dimension?"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "text",
                            "name": "grndwall_end_intersection",
                            "label": "On which intersection does the wall end?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "length_of_grndwall",
                            "label": "What is the overall length of the wall?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "grndwall_thickness",
                            "label": "What is the wall’s thickness?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What is the orientation of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "interior",
                                    "label": "Interior"
                                },
                                {
                                    "name": "exterior",
                                    "label": "Exterior"
                                }
                            ],
                            "name": "orientation_of_grndwall"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the wall extend up to the Level above?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "y",
                                    "label": "Yes"
                                },
                                {
                                    "name": "n",
                                    "label": "No"
                                }
                            ],
                            "name": "grndwall_extend_level"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "height_of_grndwall",
                            "label": "What is the height of the wall?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "no_of_grndwall_openings",
                            "label": "How many openings are there in the wall?"
                        },
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "${no_of_grndwall_openings}"
                            },
                            "type": "calculate",
                            "name": "grnd_opening_count"
                        },
                        {
                            "control": {
                                "jr:count": "${grnd_opening_count}"
                            },
                            "name": "grnd_opening",
                            "bind": {
                                "relevant": "${no_of_grndwall_openings} > 0"
                            },
                            "label": "Opening (Ground Floor)",
                            "type": "repeat",
                            "children": [
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "What kind of opening is it?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "door",
                                            "label": "Door"
                                        },
                                        {
                                            "name": "window",
                                            "label": "Window"
                                        }
                                    ],
                                    "name": "grnd_kind_of_opening"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "distance_from_grndwall",
                                    "label": "What is the distance from the Start of the wall?"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "grndopening_width",
                                    "label": "Opening Width"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "grndopening_height",
                                    "label": "Opening Height"
                                },
                                {
                                    "bind": {
                                        "relevant": "${grnd_kind_of_opening} = 'window'",
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "grndopening_sill_height",
                                    "label": "Opening Sill Height"
                                }
                            ]
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${level} = '3'",
                        "required": "true"
                    },
                    "type": "integer",
                    "name": "no_of_1stfloor_wall",
                    "label": "How many total walls are there on first floor?"
                },
                {
                    "bind": {
                        "readonly": "true()",
                        "calculate": "${no_of_1stfloor_wall}"
                    },
                    "type": "calculate",
                    "name": "frstflr_wall_count"
                },
                {
                    "control": {
                        "jr:count": "${frstflr_wall_count}"
                    },
                    "name": "frstflr_wall",
                    "bind": {
                        "relevant": "${no_of_1stfloor_wall} > 0"
                    },
                    "label": "First Floor Walls",
                    "type": "repeat",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "On which Grid line does the wall lie?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "3",
                                    "label": "3"
                                },
                                {
                                    "name": "4",
                                    "label": "4"
                                },
                                {
                                    "name": "5",
                                    "label": "5"
                                },
                                {
                                    "name": "6",
                                    "label": "6"
                                },
                                {
                                    "name": "a",
                                    "label": "A"
                                },
                                {
                                    "name": "b",
                                    "label": "B"
                                },
                                {
                                    "name": "c",
                                    "label": "C"
                                },
                                {
                                    "name": "d",
                                    "label": "D"
                                },
                                {
                                    "name": "e",
                                    "label": "E"
                                },
                                {
                                    "name": "f",
                                    "label": "F"
                                }
                            ],
                            "name": "frstwall_on_grid"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "frstwall_grid_intersection",
                            "label": "On which Grid intersection does the wall start?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there an Offset from that intersection?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "y",
                                    "label": "Yes"
                                },
                                {
                                    "name": "n",
                                    "label": "No"
                                }
                            ],
                            "name": "frst_offset"
                        },
                        {
                            "bind": {
                                "relevant": "${frst_offset} = 'y'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "frst_offset_dimension",
                            "label": "What is the offset dimension?"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "text",
                            "name": "frstwall_end_intersection",
                            "label": "On which intersection does the wall end?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "length_of_frstwall",
                            "label": "What is the overall length of the wall?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "frstwall_thickness",
                            "label": "What is the wall’s thickness?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What is the orientation of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "interior",
                                    "label": "Interior"
                                },
                                {
                                    "name": "exterior",
                                    "label": "Exterior"
                                }
                            ],
                            "name": "orientation_of_frstwall"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the wall extend up to the Level above?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "y",
                                    "label": "Yes"
                                },
                                {
                                    "name": "n",
                                    "label": "No"
                                }
                            ],
                            "name": "frstwall_extend_level"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "height_of_frstwall",
                            "label": "What is the height of the wall?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "no_of_frstwall_openings",
                            "label": "How many openings are there in the wall?"
                        },
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "${no_of_frstwall_openings}"
                            },
                            "type": "calculate",
                            "name": "frst_opening_count"
                        },
                        {
                            "control": {
                                "jr:count": "${frst_opening_count}"
                            },
                            "name": "frst_opening",
                            "bind": {
                                "relevant": "${no_of_frstwall_openings} > 0"
                            },
                            "label": "Opening (First Floor)",
                            "type": "repeat",
                            "children": [
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "What kind of opening is it?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "door",
                                            "label": "Door"
                                        },
                                        {
                                            "name": "window",
                                            "label": "Window"
                                        }
                                    ],
                                    "name": "frst_kind_of_opening"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "distance_from_frstwall",
                                    "label": "What is the distance from the Start of the wall?"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "frstopening_width",
                                    "label": "Opening Width"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "frstopening_height",
                                    "label": "Opening Height"
                                },
                                {
                                    "bind": {
                                        "relevant": "${frst_kind_of_opening} = 'window'",
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "frstopening_sill_height",
                                    "label": "Opening Sill Height"
                                }
                            ]
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${level} = '3' or ${level} = '2'",
                        "required": "true"
                    },
                    "type": "integer",
                    "name": "no_of_uprfloor_wall",
                    "label": "How many total walls are there on Upper floor?"
                },
                {
                    "bind": {
                        "readonly": "true()",
                        "calculate": "${no_of_uprfloor_wall}"
                    },
                    "type": "calculate",
                    "name": "uprflr_wall_count"
                },
                {
                    "control": {
                        "jr:count": "${uprflr_wall_count}"
                    },
                    "name": "uprflr_wall",
                    "bind": {
                        "relevant": "${no_of_uprfloor_wall} > 0"
                    },
                    "label": "Upper Floor Walls",
                    "type": "repeat",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "On which Grid line does the wall lie?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "3",
                                    "label": "3"
                                },
                                {
                                    "name": "4",
                                    "label": "4"
                                },
                                {
                                    "name": "5",
                                    "label": "5"
                                },
                                {
                                    "name": "6",
                                    "label": "6"
                                },
                                {
                                    "name": "a",
                                    "label": "A"
                                },
                                {
                                    "name": "b",
                                    "label": "B"
                                },
                                {
                                    "name": "c",
                                    "label": "C"
                                },
                                {
                                    "name": "d",
                                    "label": "D"
                                },
                                {
                                    "name": "e",
                                    "label": "E"
                                },
                                {
                                    "name": "f",
                                    "label": "F"
                                }
                            ],
                            "name": "uprwall_on_grid"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "uprwall_grid_intersection",
                            "label": "On which Grid intersection does the wall start?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there an Offset from that intersection?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "y",
                                    "label": "Yes"
                                },
                                {
                                    "name": "n",
                                    "label": "No"
                                }
                            ],
                            "name": "upr_offset"
                        },
                        {
                            "bind": {
                                "relevant": "${upr_offset} = 'y'",
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "upr_offset_dimension",
                            "label": "What is the offset dimension?"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "text",
                            "name": "uprwall_end_intersection",
                            "label": "On which intersection does the wall end?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "length_of_uprwall",
                            "label": "What is the overall length of the wall?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "uprwall_thickness",
                            "label": "What is the wall’s thickness?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What is the orientation of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "interior",
                                    "label": "Interior"
                                },
                                {
                                    "name": "exterior",
                                    "label": "Exterior"
                                }
                            ],
                            "name": "orientation_of_uprwall"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the wall extend up to the Level above?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "y",
                                    "label": "Yes"
                                },
                                {
                                    "name": "n",
                                    "label": "No"
                                }
                            ],
                            "name": "uprwall_extend_level"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "decimal",
                            "name": "height_of_uprwall",
                            "label": "What is the height of the wall?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "no_of_uprwall_openings",
                            "label": "How many openings are there in the wall?"
                        },
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "${no_of_uprwall_openings}"
                            },
                            "type": "calculate",
                            "name": "upr_opening_count"
                        },
                        {
                            "control": {
                                "jr:count": "${upr_opening_count}"
                            },
                            "name": "upr_opening",
                            "bind": {
                                "relevant": "${no_of_uprwall_openings} > 0"
                            },
                            "label": "Opening (Upper Floor)",
                            "type": "repeat",
                            "children": [
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "What kind of opening is it?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "door",
                                            "label": "Door"
                                        },
                                        {
                                            "name": "window",
                                            "label": "Window"
                                        }
                                    ],
                                    "name": "upr_kind_of_opening"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "distance_from_uprwall",
                                    "label": "What is the distance from the Start of the wall?"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "upropening_width",
                                    "label": "Opening Width"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "upropening_height",
                                    "label": "Opening Height"
                                },
                                {
                                    "bind": {
                                        "relevant": "${upr_kind_of_opening} = 'window'",
                                        "required": "true"
                                    },
                                    "type": "decimal",
                                    "name": "frstopening_sill_height",
                                    "label": "Opening Sill Height"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "type": "today",
                    "name": "today"
                },
                {
                    "bind": {
                        "calculate": "24631"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 26823,
        "name": "Design Specification Form",
        "json": {
            "name": "a9gZerCUK7AzH4R7QWVvBc_UDgirah",
            "name": "Design Specification Form",
            "sms_keyword": "a9gZerCUK7AzH4R7QWVvBc",
            "default_language": "default",
            "version": "18381",
            "id_string": "a9gZerCUK7AzH4R7QWVvBc",
            "type": "survey",
            "children": [
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "General Questions",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "date",
                            "name": "date",
                            "label": "Date"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "data_collecdtor",
                            "label": "Data Collector"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Name Of TSC",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "sangachowk",
                                    "label": "Sangachowk"
                                },
                                {
                                    "name": "dhunkharka",
                                    "label": "Dhunkharka"
                                },
                                {
                                    "name": "kahule",
                                    "label": "Kahule"
                                },
                                {
                                    "name": "bhalche",
                                    "label": "Bhalche"
                                },
                                {
                                    "name": "gogane",
                                    "label": "Gogane"
                                },
                                {
                                    "name": "thulogaun",
                                    "label": "Thulogaun"
                                },
                                {
                                    "name": "dadagaun",
                                    "label": "Dadagaun"
                                },
                                {
                                    "name": "panchkhal",
                                    "label": "Panchkhal"
                                },
                                {
                                    "name": "banepa",
                                    "label": "Banepa"
                                },
                                {
                                    "name": "thaha",
                                    "label": "Thaha"
                                }
                            ],
                            "name": "name"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Design from DUDBC catalog?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_Design_from_DUDBC_catalog"
                        }
                    ],
                    "name": "tsc"
                },
                {
                    "bind": {
                        "relevant": "${Is_Design_from_DUDBC_catalog} = 'yes'",
                        "required": "true"
                    },
                    "type": "text",
                    "name": "name_of_dudbc_design",
                    "label": "Name of DUDBC design"
                },
                {
                    "bind": {
                        "relevant": "${Is_Design_from_DUDBC_catalog} = 'no'"
                    },
                    "label": "Template",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Did you find the drawing in the Library?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "drawing_in_library"
                        }
                    ],
                    "name": "template"
                },
                {
                    "bind": {
                        "relevant": "${drawing_in_library} = 'yes'",
                        "required": "true"
                    },
                    "type": "text",
                    "name": "name_of_template",
                    "label": "What is the name of Template?"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "technology",
                    "bind": {
                        "relevant": "${drawing_in_library} = 'no'"
                    },
                    "label": "Type Of House",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What Type of House is it ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "smm",
                                    "label": "SMM"
                                },
                                {
                                    "name": "smc",
                                    "label": "SMC"
                                },
                                {
                                    "name": "bmc",
                                    "label": "BMC"
                                },
                                {
                                    "name": "bmm",
                                    "label": "BMM"
                                },
                                {
                                    "name": "rcc",
                                    "label": "RCC"
                                },
                                {
                                    "name": "cm",
                                    "label": "CM"
                                }
                            ],
                            "name": "type_of_house"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${type_of_house} = 'smm' or ${type_of_house} = 'bmm'",
                        "required": "true"
                    },
                    "label": "What type of band is it ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "rcc",
                            "label": "RCC Band"
                        },
                        {
                            "name": "timber",
                            "label": "Timber band"
                        }
                    ],
                    "name": "type_of_band"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "new_design",
                    "bind": {
                        "relevant": "${drawing_in_library} = 'no' and ${Is_Design_from_DUDBC_catalog} = 'no'"
                    },
                    "label": "New Design Requirement",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${type_of_house} = 'rcc'",
                                "required": "true"
                            },
                            "label": "No of Pillars",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "6",
                                    "label": "6"
                                },
                                {
                                    "name": "8",
                                    "label": "8"
                                },
                                {
                                    "name": "9",
                                    "label": "9"
                                },
                                {
                                    "name": "12",
                                    "label": "12"
                                },
                                {
                                    "name": "14",
                                    "label": "14"
                                },
                                {
                                    "name": "15",
                                    "label": "15"
                                },
                                {
                                    "name": "16",
                                    "label": "16"
                                }
                            ],
                            "name": "no_of_pillars"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "No of rooms",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "3",
                                    "label": "3"
                                },
                                {
                                    "name": "4",
                                    "label": "4"
                                }
                            ],
                            "name": "no_of_rooms"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_house} = 'smm' or ${type_of_house} = 'bmm'",
                                "required": "true"
                            },
                            "label": "No of Storey SMM/ BMM",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                }
                            ],
                            "name": "no_of_storey_smm_bmm"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_house} = 'smc' or ${type_of_house} = 'bmc'",
                                "required": "true"
                            },
                            "label": "No of Storey SMC/BMC",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "no_of_storey_smc_bmc"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_house} = 'rcc'",
                                "required": "true"
                            },
                            "label": "No of Storey RCC",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "3",
                                    "label": "3"
                                }
                            ],
                            "name": "no_of_storey_rcc"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_house} = 'cm'",
                                "required": "true"
                            },
                            "label": "No of Storey CM",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "no_of_storey_cm"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_band} != 'timber'",
                                "required": "true"
                            },
                            "label": "Do you want an attic?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "attic_available"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Do you want a porch ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Porch"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Do you want a corridor?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "corridor"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "room",
                    "bind": {
                        "relevant": "${drawing_in_library} = 'no'"
                    },
                    "label": "Room Size (Feet)",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true",
                                "constraint": ". <= 14"
                            },
                            "type": "decimal",
                            "name": "length",
                            "label": "Length"
                        },
                        {
                            "bind": {
                                "required": "true",
                                "constraint": ". <= 14"
                            },
                            "type": "decimal",
                            "name": "width",
                            "label": "Width"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "door",
                    "bind": {
                        "relevant": "${drawing_in_library} = 'no'"
                    },
                    "label": "No of Doors",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Front",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "front"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Back",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "back"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Left",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "left"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Right",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "right"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "window",
                    "bind": {
                        "relevant": "${Is_Design_from_DUDBC_catalog} = 'no' and ${drawing_in_library} = 'no'"
                    },
                    "label": "No of Windows",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Front",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "option_4",
                                    "label": "3"
                                }
                            ],
                            "name": "front_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Back",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "option_4",
                                    "label": "3"
                                }
                            ],
                            "name": "back_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Left",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "option_4",
                                    "label": "3"
                                }
                            ],
                            "name": "left_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Right",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "option_4",
                                    "label": "3"
                                }
                            ],
                            "name": "right_0"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "roof_type",
                    "bind": {
                        "relevant": "${Is_Design_from_DUDBC_catalog} = 'no' and ${drawing_in_library} = 'no'"
                    },
                    "label": "Roof Type",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${type_of_house} = 'smm' or ${type_of_house} = 'bmm'",
                                "required": "true"
                            },
                            "label": "Roof Type SMM / BMM",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber_truss",
                                    "label": "Timber Truss"
                                },
                                {
                                    "name": "metal_truss",
                                    "label": "Metal Truss"
                                }
                            ],
                            "name": "roof_type_smm_bmm"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_house} = 'smc' or ${type_of_house} = 'bmc' or ${type_of_house} = 'cm'",
                                "required": "true"
                            },
                            "label": "Roof Type SMC/ BMC/CM",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber_truss",
                                    "label": "Timber Truss"
                                },
                                {
                                    "name": "metal_truss",
                                    "label": "Metal Truss"
                                },
                                {
                                    "name": "slab",
                                    "label": "Slab"
                                }
                            ],
                            "name": "roof_type_smc_bmc_cm"
                        },
                        {
                            "bind": {
                                "relevant": "${type_of_house} = 'rcc'",
                                "required": "true"
                            },
                            "label": "Roof Type RCC",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "terrace",
                                    "label": "Terrace"
                                },
                                {
                                    "name": "slab",
                                    "label": "Slab"
                                }
                            ],
                            "name": "roof_type_rcc"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "Comment and Photos",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "comments",
                            "label": "Comments"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_Design_from_DUDBC_catalog} = 'no' and ${drawing_in_library} = 'no'",
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo_of_the_sketch1",
                            "label": "Photo of the sketch"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_Design_from_DUDBC_catalog} = 'no' and ${drawing_in_library} = 'no'",
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo_of_sketch_1",
                            "label": "Photo of the sketch"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photos_of_site_if_required_",
                            "label": "Photos of site (if required)"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photos_of_site_if_required__0",
                            "label": "Photos of site (if required)"
                        }
                    ],
                    "name": "cmnt_photo"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "18381"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 25910,
        "name": "First Tranche Final Inspection",
        "json": {
            "name": "a2bc3p3qUsADD2MDedAdSF_75QBKgG",
            "name": "First Tranche Final Inspection",
            "sms_keyword": "a2bc3p3qUsADD2MDedAdSF",
            "default_language": "default",
            "version": "7878",
            "id_string": "a2bc3p3qUsADD2MDedAdSF",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "What type of building is it ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_b",
                            "label": "RCC A&B"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        }
                    ],
                    "name": "What_type_of_building_is_it_"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} != 'rcc' and ${What_type_of_building_is_it_} != 'rcc_a_b' and ${What_type_of_building_is_it_} != 'confined_masonry'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the clear span of wall more than 4.5m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_clear_span_of_wall_more_than_4_5m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the building simple and regular shaped ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_building_simple_and_regular_shaped_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the length of the building more than 3 times of its width?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_of_the_building_more_than_3_times_of_its_width_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of the room more than 13.5 sq.m. ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_room_more_than_13_5_sq_m_"
                        }
                    ],
                    "name": "group_ln8fx86"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'smm' and ${What_type_of_building_is_it_} = 'bmm' and ${What_type_of_building_is_it_} = 'smc' and ${What_type_of_building_is_it_} = 'bmc'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the foundation new or old ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "old",
                                    "label": "Old"
                                },
                                {
                                    "name": "new",
                                    "label": "New"
                                }
                            ],
                            "name": "Is_the_foundation_new_or_old_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_foundation_new_or_old_} = 'old'",
                                "required": "true"
                            },
                            "label": "Is the existing foundation damaged or settled ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_existing_foundation_dam"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_existing_foundation_dam} = 'no'",
                                "required": "true"
                            },
                            "label": "Is there a good connection between the old foundation and new masonry work ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_a_good_connection_between_the_old_foundation_and_new_masonry_work_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the foundation continuous and at the same level throughout the foundation in flat area ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_foundation_continuous_and_at_the_same_level_throughout_the_foundation_in_flat_area_"
                        }
                    ],
                    "name": "group_ta4nb78"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'smm'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the stones rounded, not-dressed, easily breakable soft stone and boulder stones in its natural shape ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_stones_rounded_not_dressed_easily_breakable_soft_stone_and_boulder_stones_in_its_natural_shape_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the stones smaller than 50 mm in thickness and 150 mm in length or breadth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_stones_smaller_than_50_mm_in_thickness_and_150_mm_in_length_or_breadth_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Mud mortar free from organic materials, pebbles, hard materials ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mud_mortar_free_from_organic_materials_pebbles_hard_materials_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 750 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_750_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the base of foundation greater than 800 mm in soft soil/ greater than 750 mm in medium to hard soil ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_800_mm_in_soft_soil_greater_than_750_mm_in_medium_to_hard_soil_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the wall at the plinth beam 350 mm or more ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_350_mm_or_more_"
                        }
                    ],
                    "name": "group_gn67i69"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'smm' and ${What_type_of_building_is_it_} = 'bmm'"
                    },
                    "label": "SMM/BMM Vertical Member",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member placed at all corners and junctions of walls and starting from the foundation and continuing upwards ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_and_junctions_of_walls_and_starting_from_the_foundation_and_continuing_upwards_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member placed adjacent to all doors and window openings ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_adjacent_to_all_doors_and_window_openings_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member Timber or Concrete ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "concrete",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_Timber_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber_} = 'timber'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner of size 75 mm x 100 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member of timber and house more than one storey ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_of_timber_and_house_more_than_one_storey_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber_} = 'timber'",
                                "required": "true"
                            },
                            "label": "Is the vertical member adjacent to all doors and window openings two members of size 75 mm x 100 mm each ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_adjacen"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_adjacen} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber_} = 'concrete'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner and intersections one bar of at least 12 mm diameter and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M15 grade or mix ratio 1:2:4 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m15_grade_or_mix_ratio_1_2_4_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_"
                        }
                    ],
                    "name": "group_cn85n62"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'smm' and ${What_type_of_building_is_it_} = 'bmm'"
                    },
                    "label": "SMM/BMM Plinth",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the plinth of Timber or RC ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "rc",
                                    "label": "RC"
                                }
                            ],
                            "name": "Is_the_plinth_of_Timber_or_RC_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "How many storeys is the building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "one",
                                    "label": "One"
                                },
                                {
                                    "name": "one_plus_attic",
                                    "label": "One plus attic"
                                },
                                {
                                    "name": "two",
                                    "label": "Two"
                                }
                            ],
                            "name": "How_many_storeys_is_the_buildi"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'timber'",
                                "required": "true"
                            },
                            "label": "Is the plinth of timber or house more than one storey ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_plinth_of_timber_or_house_more_than_one_storey_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'timber' and ${How_many_storeys_is_the_buildi} = 'one'",
                                "required": "true"
                            },
                            "label": "Is the level of the plinth less than 300 mm from ground level ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_plinth_less_than_300_mm_from_ground_level_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'timber' and ${How_many_storeys_is_the_buildi} = 'one'",
                                "required": "true"
                            },
                            "label": "Are two 75 mm x 38 mm members used and connected with batten of the same size at a spacing of 500 mm center to center or less ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Are_two_75_mm_x_38_mm_members_"
                        },
                        {
                            "bind": {
                                "relevant": "${Are_two_75_mm_x_38_mm_members_} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc' and ${How_many_storeys_is_the_buildi} != 'two'",
                                "required": "true"
                            },
                            "label": "Is the level of the plinth less than 300 mm from ground level ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_plinth_less_than_300_mm_from_ground_level__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc'",
                                "required": "true"
                            },
                            "label": "Is the thickness of the band 150 mm for medium and soft soil or 75 mm for hard soil ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_thickness_of_the_band_1"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thickness_of_the_band_1} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M15 grade or mix ratio 1:2:4 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m15_grade_or_mix_ratio_1_2_4__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc' and ${How_many_storeys_is_the_buildi} != 'two'",
                                "required": "true"
                            },
                            "label": "Is the main reinforcement 4 nos of 12mm dia rebars in case of 150mm thick plinth or 2 nos of 12 mm diameter rebar in case of 75 mm plinth with 6 mm diameter stirrups at 150 mm center to center and have a clear cover of 25 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_main_reinforcement_4_no"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_main_reinforcement_4_no} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc'",
                                "required": "true"
                            },
                            "label": "Is the width of the band at least equal to the width of the wall ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_band_at_least_equal_to_the_width_of_the_wall_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC_} = 'rc' and ${How_many_storeys_is_the_buildi} != 'two'",
                                "required": "true"
                            },
                            "label": "Is the level of the plinth less than 300 mm from ground level ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_plinth_less_than_300_mm_from_ground_level__0_0"
                        }
                    ],
                    "name": "group_cl7sv00"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'smc'"
                    },
                    "label": "SMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "How many storeys is the building ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "one",
                                    "label": "One"
                                },
                                {
                                    "name": "more_than_one",
                                    "label": "More than one"
                                },
                                {
                                    "name": "more_than_two_plus_attic",
                                    "label": "More than two plus attic"
                                }
                            ],
                            "name": "How_many_storeys_is_the_buildi_002"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_002} = 'one'",
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 800 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_depth_of_the_foundation"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_depth_of_the_foundation} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the width of the base of foundation greater than 800 mm in soft soil/ greater than 600 mm in medium to hard soil ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_800_mm_in_soft_soil_greater_than_600_mm_in_medium_to_hard_soil_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_002} = 'one'",
                                "required": "true"
                            },
                            "label": "Is the width of the wall at the plinth beam level 350 mm or more ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_level_350_mm_or_more_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_002} = 'more_than_one'",
                                "required": "true"
                            },
                            "label": "Is the type of soil soft ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_type_of_soil_soft_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_type_of_soil_soft_} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the width of the base of foundation greater than 800 mm in medium soil/ greater than 600 mm in hard soil ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_800_mm_in_medium_soil_greater_than_600_mm_in_hard_soil_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the wall at the plinth beam level 450 mm or more ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_level_450_mm_or_more_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_002} != 'one'",
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 900 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_900_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member placed at all corners, junctions of walls, and adjacent to all openings and starting from the foundation and continuing upwards ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_junctions_of_walls_and_adjacent_to_all_openings_and_starting_from_the_foundation_and_continuing_upwards_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member Timber or Concrete ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "concrete",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_Timber__001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber__001} = 'concrete'",
                                "required": "true"
                            },
                            "label": "Is the house one storey ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_house_one_storey_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_house_one_storey_} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner,intersections and adjacent to openings one bar of at least 12 mm diameter and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_002"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_002} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_002} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_house_one_storey_} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of at least 16 mm diameter and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_003"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_003} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_003} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_"
                        }
                    ],
                    "name": "group_nh6qm09"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} != 'smm' and ${What_type_of_building_is_it_} != 'bmm' and ${What_type_of_building_is_it_} != 'rcc' and ${What_type_of_building_is_it_} != 'rcc_a_b' and ${What_type_of_building_is_it_} != 'confined_masonry'"
                    },
                    "label": "Plinth SMC/BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the level of the plinth less than 300 mm from ground level ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_plinth_less_than_300_mm_from_ground_level_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the thickness of the band at least 150 mm for medium and soft soil or at least 75 mm for hard soil ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                },
                                {
                                    "name": "option_3",
                                    "label": "Option 3"
                                }
                            ],
                            "name": "is_the_thickness_of_the_band_at_least_150_mm_for_medium_and_soft_soil_or_at_least_75_mm_for_hard_soil_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the band at least equal to the width of the wall ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_band_at_least_equal_to_the_width_of_the_wall_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the plinth of Timber or RC ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "rc",
                                    "label": "RC"
                                }
                            ],
                            "name": "Is_the_plinth_of_Timber_or_RC__001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_plinth_of_Timber_or_RC__001} = 'rc'",
                                "required": "true"
                            },
                            "label": "Is the main reinforcement 4 nos of 12 mm diameter rebars in case of 150 mm thick plinth or 2 nos of 12 mm diameter rebars in case of 75 mm plinth with 6 mm diameter stirrups at 150 mm center to center and have a clear cover of 25 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_main_reinforcement_4_no_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_main_reinforcement_4_no_001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_main_reinforcement_4_no_001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0"
                        }
                    ],
                    "name": "group_oa7uk55"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'bmm'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Has Overburnt, underburnt, deformed bricks used ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "has_overburnt_underburnt_deformed_bricks_used_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Mud mortar free from organic materials, pebbles, hard materials ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mud_mortar_free_from_organic_materials_pebbles_hard_materials_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 750 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_750_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the base of foundation greater than 750 mm in soft soil/ greater than 650 mm in medium soil and greater than 550 mm in hard soil ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_750_mm_in_soft_soil_greater_than_650_mm_in_medium_soil_and_greater_than_550_mm_in_hard_soil_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the wall at the plinth beam 350 mm or more ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_350_mm_or_more_"
                        }
                    ],
                    "name": "group_rx3bc84"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'bmc'"
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "How many storeys is the building ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "one",
                                    "label": "One"
                                },
                                {
                                    "name": "more_than_one",
                                    "label": "More than one"
                                },
                                {
                                    "name": "more_than_two_plus_attic",
                                    "label": "More than two plus attic"
                                }
                            ],
                            "name": "How_many_storeys_is_the_buildi_001"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'one'",
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 800 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_800_mm_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'one'",
                                "required": "true"
                            },
                            "label": "Is the width of the wall at the plinth beam 230 mm or more ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_at_the_plinth_beam_230_mm_or_more_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'more_than_one'",
                                "required": "true"
                            },
                            "label": "Is the width of the base of foundation greater than 900 mm in soft soil/greater than 650 in medium soil/ greater than 550 mm in hard soil?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_base_of_foundation_greater_than_900_mm_in_soft_soil_greater_than_650_in_medium_soil_greater_than_550_mm_in_hard_soil_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'more_than_one'",
                                "required": "true"
                            },
                            "label": "Is the width of the wall below the plinth beam 350 mm or more ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_below_the_plinth_beam_350_mm_or_more_"
                        },
                        {
                            "bind": {
                                "relevant": "${How_many_storeys_is_the_buildi_001} = 'more_than_one'",
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation from the ground level greater than 900 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_from_the_ground_level_greater_than_900_mm__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Has Overburnt, underburnt, deformed bricks used ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "has_overburnt_underburnt_deformed_bricks_used__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member placed at all corners, junctions of walls, and adjacent to all openings and starting from the foundation and continuing upwards ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_junctions_of_walls_and_adjacent_to_all_openings_and_starting_from_the_foundation_and_continuing_upwards__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member Timber or Concrete ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "concrete",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_Timber__002"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_Timber__002} = 'concrete'",
                                "required": "true"
                            },
                            "label": "Is the house one storey ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_house_one_storey__001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_house_one_storey__001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of at least 12 mm diameter and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_004"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_004} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_004} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_house_one_storey__001} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of at least 16 mm diameter and covered with concrete or 1:4 mortar in cavities made around them during masonry construction ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_005"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_005} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_005} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0"
                        }
                    ],
                    "name": "group_jd5ul78"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the house limited up to 3 floor ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_house_limited_up_to_3_floor_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the number of bay two to six ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_number_of_bay_two_to_six_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the area less than 1000 sq. ft and area in between 4 pillars 13.5 sq m only ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_area_less_than_1000_sq_ft_and_area_in_between_4_pillars_13_5_sq_m_only_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Total height of building less than 11 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_total_height_of_building_less_than_11_m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the height of floor from 2.75 m to 3.35 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_floor_from_2_75_m_to_3_35_m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the shape square or rectangular ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_shape_square_or_rectangular_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the ratio of length less than 3 times the breadth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_ratio_of_length_less_than_3_times_the_breadth_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the mortar ratio at least 1:4 for 4\" wall and 1:6 for thicker wall ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_at_least_1_4_for_4_wall_and_1_6_for_thicker_wall_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth at least 5 ft ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_at_least_5_ft_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Choose the type of soil from the options below.",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "loose_soil",
                                    "label": "Loose Soil"
                                },
                                {
                                    "name": "soft_soil",
                                    "label": "Soft Soil"
                                },
                                {
                                    "name": "medium_soil",
                                    "label": "Medium Soil"
                                },
                                {
                                    "name": "hard_soil",
                                    "label": "Hard Soil"
                                }
                            ],
                            "name": "Choose_the_type_of_soil_from_t"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'loose_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at corner loose soil >2.2 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_corner_loose_soil_2_2_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'loose_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at front loose soil >2.4 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_front_loose_soil_2_4_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'loose_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at mid loose soil >3 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_mid_loose_soil_3_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'soft_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at corner soft soil >1.5 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_corner_soft_soil_1_5_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'soft_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at front soft soil >1.65 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_front_soft_soil_1_65_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'soft_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at mid soft soil >2.1 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_mid_soft_soil_2_1_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'medium_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at corner medium soil >1.25m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_corner_medium_soil_1_25m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'medium_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at front medium soil >1.4 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_front_medium_soil_1_4_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'medium_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at mid medium soil >1.7 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_mid_medium_soil_1_7_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'hard_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at corner hard soil >1.2 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_corner_hard_soil_1_2_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'hard_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at front hard soil >1.1 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_front_hard_soil_1_1_m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Choose_the_type_of_soil_from_t} = 'hard_soil'",
                                "required": "true"
                            },
                            "label": "Is the width of the foundation at mid hard soil >1.5 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_at_mid_hard_soil_1_5_m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar at base of the foundation at least 12 mm diameter ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_at_base_of_the_foundation_at_least_12_mm_diameter_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the footing 400 mm in middle and 300 mm in other sides ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_footing_400_mm_in_middle_and_300_mm_in_other_sides_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the beam of the foundation at least 9 inch X 9 inch with 4 numbers of 12 mm diameter rebar ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_beam_of_the_foundation_at_least_9_inch_x_9_inch_with_4_numbers_of_12_mm_diameter_rebar_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the height at least 450 mm from Ground Level ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_at_least_450_mm_from_ground_level_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size at least 9 inches X 9 inches ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_at_least_9_inches_x_9_inches_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Main rebar 4 numbers of 12 mm and 8 mm stirrups placed at 6 inches center to center ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_main_rebar_4_numbers_of_12_mm_and_8_mm_stirrups_placed_at_6_inches_center_to_center_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the splicing of bar equal to or less than 50% at one section and Splice/overlap length at least 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_splicing_of_bar_equal_to_or_less_than_50_at_one_section_and_splice_overlap_length_at_least_60_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the pillar aligned in one line ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_pillar_aligned_in_one_line_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the pillar size at least 12 inches X 12 inches ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_pillar_size_at_least_12_inches_x_12_inches_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar at ground and first floor 4 numbers of 16 mm + 4 numbers of 12 mm and third floor 8 numbers of 12 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_at_ground_and_first_floor_4_numbers_of_16_mm_4_numbers_of_12_mm_and_third_floor_8_numbers_of_12_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the stirrups at least 8 mm diameter and at 4 inch c/c at ends and joints and 6 inch at middle?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_stirrups_at_least_8_mm_diameter_and_at_4_inch_c_c_at_ends_and_joints_and_6_inch_at_middle_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Lapping in the middle leaving 2 ft from edge and not more than 50% at one section and overlap of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_lapping_in_the_middle_leaving_2_ft_from_edge_and_not_more_than_50_at_one_section_and_overlap_of_60_"
                        }
                    ],
                    "name": "group_qn8mc36"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'rcc_a_b'"
                    },
                    "label": "RCC A&B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "pictures_of_each_page_of_approved_design_adopted",
                            "label": "Pictures of each page of Approved design adopted"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "pictures_of_each_page_of_approved_design_adopted_0",
                            "label": "Pictures of each page of Approved design adopted"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "pictures_of_each_page_of_approved_design_adopted_0_0",
                            "label": "Pictures of each page of Approved design adopted"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "pictures_of_each_page_of_approved_design_adopted_0_0_0",
                            "label": "Pictures of each page of Approved design adopted"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the number of bays as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_number_of_bays_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the building area as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_building_area_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the total height of building less than 11 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_total_height_of_building_less_than_11_m__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the length of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_of_the_building_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the breadth of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_breadth_of_the_building_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the storey height of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_storey_height_of_the_building_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the mortar ratio at least 1:4 for 4\" wall and 1:6 for thicker wall ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_at_least_1_4_for_4_wall_and_1_6_for_thicker_wall__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete mix and quality as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_mix_and_quality_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0_0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the type of foundation as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_type_of_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of foundation as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar provided in the foundation as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_provided_in_the_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the foundation as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_foundation_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the bottom tie beam required as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_bottom_tie_beam_require"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_bottom_tie_beam_require} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the size of the beam section as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_beam_section_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_bottom_tie_beam_require} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar size and detailing provided as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_size_and_detailing_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of the plinth beam section as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_plinth_beam_section_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar size and detailing provided as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_size_and_detailing_provided_as_per_approved_design__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the connections provided adequate as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_connections_provided_adequate_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of the pillar section as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_pillar_section_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar size and detailing provided as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_size_and_detailing_provided_as_per_approved_design__0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design__0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the ring provided as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_ring_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the connections provided adequate as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_connections_provided_adequate_as_per_approved_design__0"
                        }
                    ],
                    "name": "group_mv6pc20"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it_} = 'confined_masonry'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the site lie in a geographical fault area ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "does_the_site_lie_in_a_geographical_fault_area_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the site susceptible to landslides ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_site_susceptible_to_landslides_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the slope of the site more than 20% ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_slope_of_the_site_more_than_20_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the site placed on a riverbanks and water logged areas ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_site_placed_on_a_riverbanks_and_water_logged_areas_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the maximum span of the wall more than 3.5 meters ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_maximum_span_of_the_wall_more_than_3_5_meters_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the house either a square or a rectangle ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_house_either_a_square_or_a_rectangle_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the length to breadth ratio of the structure more than 3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_to_breadth_ratio_of_the_structure_more_than_3_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the mortar ratio 1:5 or richer ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_1_5_or_richer_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy 415Mpa or Fy 500 Mpa with overlap length of 60 times the diameter of the bar ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_or_fy_500_mpa_with_overlap_length_of_60_times_the_diameter_of_the_bar_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the foundation continuous and at the same level throughout the foundation in flat area ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_foundation_continuous_and_at_the_same_level_throughout_the_foundation_in_flat_area_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the foundation less than 900 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_foundation_less_than_900_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of footing 900 mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_footing_900_mm_or_more_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there a Tie column provided at each corners, wall intersections and on either side of the doors, which is starting from the foundation and continuing upwards ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_a_tie_column_provided_at_each_corners_wall_intersections_and_on_either_side_of_the_doors_which_is_starting_from_the_foundation_and_continuing_upwards_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical reinforcement in tie column at least 4 bars of 12 mm diameter and 7 mm diameter bar stirrups placed at 150 mm center to center ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_reinforcement_in_tie_column_at_least_4_bars_of_12_mm_diameter_and_7_mm_diameter_bar_stirrups_placed_at_150_mm_center_to_center_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement used of high strength deformed bars of Fe 415 MPa ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_used_of_high_strength_deformed_bars_of_fe_415_mpa_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3__0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is plinth band provided ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_plinth_band_provided_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the plinth height more than 300 mm from the existing ground level ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_plinth_height_more_than_300_mm_from_the_existing_ground_level_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the plinth beam greater than or equal to 150 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_plinth_beam_greater_than_or_equal_to_150_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the plinth beam greater or equal to 200 mm ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_plinth_beam_greater_or_equal_to_200_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the main reinforcement in the plinth, 4 bars of 10 mm diameter and 7 mm diameter rings provided at 150 mm center to center with 50 mm hook length and clear cover of 25 mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_main_reinforcement_in_the_plinth_4_bars_of_10_mm_diameter_and_7_mm_diameter_rings_provided_at_150_mm_center_to_center_with_50_mm_hook_length_and_clear_cover_of_25_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement used of high strength deformed bars of Fe 415 MPa ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_used_of_high_strength_deformed_bars_of_fe_415_mpa__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3__0_0_0"
                        }
                    ],
                    "name": "group_ic0hf00"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "7878"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 25754,
        "name": "Design Library Template",
        "json": {
            "name": "aNC3Cv7JU6rK8tsUURPCMU_3s7iT5O",
            "name": "Design Library Template",
            "sms_keyword": "aNC3Cv7JU6rK8tsUURPCMU",
            "default_language": "default",
            "version": "18385",
            "id_string": "aNC3Cv7JU6rK8tsUURPCMU",
            "type": "survey",
            "children": [
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "General Questions",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What type of house is it?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "SMM",
                                    "label": "Stone Masonry in Mud Mortar (SMM)"
                                },
                                {
                                    "name": "SMC",
                                    "label": "Stone Masonry in Cement Mortar (SMC)"
                                },
                                {
                                    "name": "BMC",
                                    "label": "Brick Masonry in Cement Mortar (BMC)"
                                },
                                {
                                    "name": "BMM",
                                    "label": "Brick Masonry in Mud Mortar (BMM)"
                                },
                                {
                                    "name": "RCC",
                                    "label": "Reinforced Concrete Cement (RCC)"
                                },
                                {
                                    "name": "confined_mason",
                                    "label": "Confined Masonry"
                                },
                                {
                                    "name": "Others",
                                    "label": "Others"
                                }
                            ],
                            "name": "what_type_of_house_is_it_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "No of rooms",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "3",
                                    "label": "3"
                                },
                                {
                                    "name": "4",
                                    "label": "4"
                                }
                            ],
                            "name": "no_of_rooms"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Do you want an Attic ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Do_you_want_an_Attic_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Do you want a porch ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "do_you_want_a_porch_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Do you want a corridor?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "do_you_want_a_corridor_"
                        }
                    ],
                    "name": "group_general"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'RCC'",
                        "required": "true"
                    },
                    "label": "No of Pillars",
                    "type": "select one",
                    "children": [
                        {
                            "name": "9",
                            "label": "9"
                        },
                        {
                            "name": "10",
                            "label": "10"
                        },
                        {
                            "name": "11",
                            "label": "11"
                        },
                        {
                            "name": "12",
                            "label": "12"
                        }
                    ],
                    "name": "no_of_pillars"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'RCC'",
                        "required": "true"
                    },
                    "label": "No of Storey RCC",
                    "type": "select one",
                    "children": [
                        {
                            "name": "1",
                            "label": "1"
                        },
                        {
                            "name": "2",
                            "label": "2"
                        },
                        {
                            "name": "3",
                            "label": "3"
                        }
                    ],
                    "name": "no_of_storey_rcc"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'BMC'",
                        "required": "true"
                    },
                    "label": "No of Storey BMC",
                    "type": "select one",
                    "children": [
                        {
                            "name": "1",
                            "label": "1"
                        },
                        {
                            "name": "2",
                            "label": "2"
                        }
                    ],
                    "name": "no_of_storey_bmc"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'SMC'",
                        "required": "true"
                    },
                    "label": "No of Storey SMC",
                    "type": "select one",
                    "children": [
                        {
                            "name": "1",
                            "label": "1"
                        },
                        {
                            "name": "2",
                            "label": "2"
                        }
                    ],
                    "name": "no_of_storey_smc"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'SMM'",
                        "required": "true"
                    },
                    "label": "No of storey SMM",
                    "type": "select one",
                    "children": [
                        {
                            "name": "1",
                            "label": "1"
                        }
                    ],
                    "name": "No_of_storey_SMM"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'SMM'",
                        "required": "true"
                    },
                    "label": "Which type of band ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "RCC_band",
                            "label": "RCC band"
                        },
                        {
                            "name": "timber_band",
                            "label": "Timber Band"
                        }
                    ],
                    "name": "Which_type_of_band_"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "Room Size (Feet)",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true",
                                "constraint": ". <= 14"
                            },
                            "type": "decimal",
                            "name": "length",
                            "label": "Length"
                        },
                        {
                            "bind": {
                                "required": "true",
                                "constraint": ". <= 14"
                            },
                            "type": "decimal",
                            "name": "width",
                            "label": "Width"
                        }
                    ],
                    "name": "group_room"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "No of Doors",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Front",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "front"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Back",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "back"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Left",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "left"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Right",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                }
                            ],
                            "name": "right"
                        }
                    ],
                    "name": "group_door"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "No of Windows",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Front",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "option_4",
                                    "label": "3"
                                }
                            ],
                            "name": "front_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Back",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "option_4",
                                    "label": "3"
                                }
                            ],
                            "name": "back_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Left",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "option_4",
                                    "label": "3"
                                }
                            ],
                            "name": "left_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Right",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "0",
                                    "label": "0"
                                },
                                {
                                    "name": "1",
                                    "label": "1"
                                },
                                {
                                    "name": "2",
                                    "label": "2"
                                },
                                {
                                    "name": "option_4",
                                    "label": "3"
                                }
                            ],
                            "name": "right_0"
                        }
                    ],
                    "name": "group_window"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'SMM'",
                        "required": "true"
                    },
                    "label": "Roof type SMM",
                    "type": "select one",
                    "children": [
                        {
                            "name": "AUTOMATIC",
                            "label": "Timber Truss"
                        },
                        {
                            "name": "metal_truss",
                            "label": "Metal Truss"
                        }
                    ],
                    "name": "Roof_type_smm"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'SMC'",
                        "required": "true"
                    },
                    "label": "Roof type SMC",
                    "type": "select one",
                    "children": [
                        {
                            "name": "AUTOMATIC",
                            "label": "Timber Truss"
                        },
                        {
                            "name": "metal_truss",
                            "label": "Metal Truss"
                        },
                        {
                            "name": "slab",
                            "label": "Slab"
                        }
                    ],
                    "name": "Roof_type_smc"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'BMC'",
                        "required": "true"
                    },
                    "label": "Roof type BMC",
                    "type": "select one",
                    "children": [
                        {
                            "name": "AUTOMATIC",
                            "label": "Timber Truss"
                        },
                        {
                            "name": "metal_truss",
                            "label": "Metal Truss"
                        },
                        {
                            "name": "slab",
                            "label": "Slab"
                        }
                    ],
                    "name": "Roof_type_bmc"
                },
                {
                    "bind": {
                        "relevant": "${what_type_of_house_is_it_} = 'RCC'",
                        "required": "true"
                    },
                    "label": "Roof type RCC",
                    "type": "select one",
                    "children": [
                        {
                            "name": "AUTOMATIC",
                            "label": "Terrace"
                        },
                        {
                            "name": "metal_truss",
                            "label": "Metal Truss"
                        },
                        {
                            "name": "slab",
                            "label": "Slab"
                        }
                    ],
                    "name": "Roof_type_rcc"
                },
                {
                    "label": "Your Design Is",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "relevant": "${no_of_rooms} = '2' and ${No_of_storey_SMM} = '1' and ${Do_you_want_an_Attic_} = 'yes' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 11 and ${width} = 10 and ${front} = '2' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '1' and ${Roof_type_smm} = 'AUTOMATIC' and ${Which_type_of_band_} = 'RCC_band'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_1",
                            "label": "SMM 12"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${Which_type_of_band_} = 'RCC_band' and ${no_of_rooms} = '2' and ${No_of_storey_SMM} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 11 and ${width} = 10 and ${front} = '2' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '1' and ${Roof_type_smm} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_18",
                            "label": "SMM 18"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${No_of_storey_SMM} = '1' and ${no_of_rooms} = '2' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 10 and ${width} = 10 and ${front} = '2' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '1' and ${Roof_type_smm} = 'AUTOMATIC' and ${Which_type_of_band_} = 'RCC_band'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_smm_21",
                            "label": "SMM 21"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${Which_type_of_band_} = 'RCC_band' and ${no_of_rooms} = '1' and ${No_of_storey_SMM} = '1' and ${Do_you_want_an_Attic_} = 'yes' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${width} = 10 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '0' and ${right_0} = '1' and ${Roof_type_smm} = 'AUTOMATIC' and ${length} = 10",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_30",
                            "label": "SMM 30"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${No_of_storey_SMM} = '1' and ${no_of_rooms} = '2' and ${Do_you_want_an_Attic_} = 'yes' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 12 and ${width} = 11 and ${front} = '2' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '1' and ${Roof_type_smm} = 'AUTOMATIC' and ${Which_type_of_band_} = 'RCC_band'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_smm_39",
                            "label": "SMM 39"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${No_of_storey_SMM} = '1' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 12 and ${width} = 11 and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${Roof_type_smm} = 'AUTOMATIC' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${front} = '1' and ${right_0} = '0' and ${Which_type_of_band_} = 'timber_band'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_smm_t_1",
                            "label": "SMM-T-1"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${No_of_storey_SMM} = '1' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 12 and ${width} = 11 and ${Roof_type_smm} = 'AUTOMATIC' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${Which_type_of_band_} = 'timber_band' and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '0' and ${right_0} = '1'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_smm_t_3",
                            "label": "SMM-T-3"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${No_of_storey_SMM} = '1' and ${Which_type_of_band_} = 'timber_band' and ${length} = 10 and ${width} = 10 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '1' and ${left_0} = '0' and ${right_0} = '0' and ${Roof_type_smm} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_t_9",
                            "label": "SMM - T- 9"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${No_of_storey_SMM} = '1' and ${Which_type_of_band_} = 'timber_band' and ${length} = 11 and ${width} = 10 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '0' and ${Roof_type_smm} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_t_10",
                            "label": "SMM - T- 10"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${No_of_storey_SMM} = '1' and ${Which_type_of_band_} = 'timber_band' and ${length} = 13 and ${width} = 10 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '0' and ${Roof_type_smm} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_t_11",
                            "label": "SMM - T- 11"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${No_of_storey_SMM} = '1' and ${Which_type_of_band_} = 'timber_band' and ${length} = 10 and ${width} = 12 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '0' and ${Roof_type_smm} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_t_12",
                            "label": "SMM - T- 12"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${No_of_storey_SMM} = '1' and ${Which_type_of_band_} = 'timber_band' and ${length} = 10 and ${width} = 12 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${Roof_type_smm} = 'AUTOMATIC' and ${left_0} = '0' and ${right_0} = '1'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_t_13",
                            "label": "SMM - T- 13"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${No_of_storey_SMM} = '1' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 10 and ${width} = 10 and ${Roof_type_smm} = 'AUTOMATIC' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${Which_type_of_band_} = 'timber_band' and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '0' and ${right_0} = '1'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_smm_t_16",
                            "label": "SMM-T-16"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${No_of_storey_SMM} = '1' and ${Which_type_of_band_} = 'timber_band' and ${length} = 12 and ${width} = 12 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '0' and ${Roof_type_smm} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_t_18",
                            "label": "SMM - T- 18"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'SMM' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${No_of_storey_SMM} = '1' and ${Which_type_of_band_} = 'timber_band' and ${length} = 11 and ${width} = 10 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${Roof_type_smm} = 'AUTOMATIC' and ${left_0} = '0' and ${right_0} = '1'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "smm_t_19",
                            "label": "SMM - T- 19"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'BMC' and ${no_of_storey_bmc} = '1' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 12 and ${width} = 12 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '1' and ${back_0} = '0' and ${left_0} = '0' and ${right_0} = '0' and ${Roof_type_bmc} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_bmc_2",
                            "label": "BMC 2"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'BMC' and ${no_of_storey_bmc} = '1' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 12 and ${width} = 11 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '1' and ${back_0} = '0' and ${left_0} = '0' and ${right_0} = '0' and ${Roof_type_bmc} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_bmc_4",
                            "label": "BMC 4"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'BMC' and ${no_of_storey_bmc} = '1' and ${no_of_rooms} = '2' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'yes' and ${length} = 12 and ${width} = 12 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '2' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '1' and ${Roof_type_bmc} = 'metal_truss'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_bmc_34",
                            "label": "BMC 34"
                        },
                        {
                            "bind": {
                                "relevant": "${what_type_of_house_is_it_} = 'BMC' and ${no_of_storey_bmc} = '1' and ${no_of_rooms} = '1' and ${Do_you_want_an_Attic_} = 'no' and ${do_you_want_a_porch_} = 'yes' and ${do_you_want_a_corridor_} = 'no' and ${length} = 11 and ${width} = 12 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '0' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '0' and ${Roof_type_bmc} = 'AUTOMATIC'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_bmc_62",
                            "label": "BMC 62"
                        },
                        {
                            "bind": {
                                "relevant": "${no_of_pillars} = '12' and ${what_type_of_house_is_it_} = 'RCC' and ${no_of_storey_rcc} = '1' and ${no_of_rooms} = '4' and ${do_you_want_a_porch_} = 'no' and ${do_you_want_a_corridor_} = 'yes' and ${length} = 11 and ${width} = 11 and ${front} = '1' and ${back} = '0' and ${left} = '0' and ${right} = '0' and ${front_0} = '2' and ${back_0} = '0' and ${left_0} = '1' and ${right_0} = '1' and ${Roof_type_rcc} = 'slab'",
                                "required": "false"
                            },
                            "type": "note",
                            "name": "your_design_is_rcc_26",
                            "label": "RCC 26"
                        }
                    ],
                    "name": "group_bw9cq35"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "Comment and Photos",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "comments",
                            "label": "Comments"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo_of_the_sketch",
                            "label": "Photo of the sketch"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo_of_the_sketch_0",
                            "label": "Photo of the sketch"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photos_of_site_if_required_",
                            "label": "Photos of site (if required)"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photos_of_site_if_required__0",
                            "label": "Photos of site (if required)"
                        }
                    ],
                    "name": "group_cmnt_phot"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "18385"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 24742,
        "name": "Pre-Construction Survey",
        "json": {
            "name": "aV2Bztu5b7BDfz4qFFKcib_BG9ylTf",
            "name": "Pre-Construction Survey",
            "sms_keyword": "aV2Bztu5b7BDfz4qFFKcib",
            "default_language": "default",
            "version": "18391",
            "id_string": "aV2Bztu5b7BDfz4qFFKcib",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "text",
                    "name": "data_recorder",
                    "label": "Name of the recorder"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "date",
                    "name": "date",
                    "label": "Date"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "Baseline Data",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "cbs_slip_",
                            "label": "CBS Slip#"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "cbs_slip_homeowner_serial_",
                            "label": "CBS Slip Homeowner Serial #"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "house_ward",
                            "label": "House Ward"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "village_name",
                            "label": "Village Name"
                        }
                    ],
                    "name": "baseline_data"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "label": "Homeowner Information",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "homeowner_name",
                            "label": "Homeowner Name"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Homeowner Gender",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "female",
                                    "label": "Female"
                                },
                                {
                                    "name": "male",
                                    "label": "Male"
                                },
                                {
                                    "name": "others",
                                    "label": "Others"
                                }
                            ],
                            "name": "homeowner_gender"
                        },
                        {
                            "bind": {
                                "jr:constraintMsg": "Invalid age",
                                "required": "true",
                                "constraint": ". > 1965 and . < 2055"
                            },
                            "type": "integer",
                            "name": "birth_year",
                            "label": "Homeowner Birth Year in Nepali"
                        },
                        {
                            "control": {
                                "appearance": "numbers"
                            },
                            "bind": {
                                "required": "true",
                                "constraint": ". = ''"
                            },
                            "type": "text",
                            "name": "Homwowner_Telephone",
                            "label": "Homwowner Telephone"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Homeowner Ethnicity",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "brahmin_chhetr",
                                    "label": "Brahmin/Chhetri"
                                },
                                {
                                    "name": "janjati",
                                    "label": "Janjati"
                                },
                                {
                                    "name": "dalit",
                                    "label": "Dalit"
                                },
                                {
                                    "name": "others",
                                    "label": "Others"
                                }
                            ],
                            "name": "homeowner_ethnicity"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are you married?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_you_married_"
                        },
                        {
                            "bind": {
                                "required": "true",
                                "constraint": ". < 99"
                            },
                            "type": "integer",
                            "name": "how_many_household_members_are_there_",
                            "label": "How many household members are there?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "male_members",
                            "label": "How many household members are male?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "female_members",
                            "label": "How many household members are female?"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Homeowner Identification Card",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "citizenship_certificate",
                                    "label": "Citizenship Certificate"
                                },
                                {
                                    "name": "voter_s_card",
                                    "label": "Voter's Card"
                                },
                                {
                                    "name": "driver_s_license",
                                    "label": "Driver's License"
                                }
                            ],
                            "name": "Homeowner_Identification_Card"
                        },
                        {
                            "bind": {
                                "relevant": "${Homeowner_Identification_Card} = 'citizenship_certificate'",
                                "required": "true"
                            },
                            "type": "text",
                            "name": "homeowner_citizenship_certificate",
                            "label": "Homeowner Citizenship Certificate"
                        },
                        {
                            "bind": {
                                "relevant": "${Homeowner_Identification_Card} = 'voter_s_card'",
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "homeowner_voter_s_card_",
                            "label": "Homeowner Voter's Card #"
                        },
                        {
                            "bind": {
                                "relevant": "${Homeowner_Identification_Card} = 'driver_s_license'",
                                "required": "true"
                            },
                            "type": "text",
                            "name": "homeowner_s_driving_license",
                            "label": "Homeowner's Driving License"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "homeowner_identification_card_photo",
                            "label": "Homeowner Identification Card Photo side 1"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "homeowner_identification_card_photo_side_2",
                            "label": "Homeowner Identification Card Photo side 2"
                        }
                    ],
                    "name": "homeowner_info"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "Are you planning to build one of the Government house model?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "Are_you_planning_to_build_one_"
                },
                {
                    "bind": {
                        "relevant": "${Are_you_planning_to_build_one_} = 'yes'"
                    },
                    "label": "Government Model",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Which government house model do you prefer to build?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "option_1",
                                    "label": "SMC 1.1"
                                },
                                {
                                    "name": "option_2",
                                    "label": "SMC 1.2"
                                },
                                {
                                    "name": "smc_2_1",
                                    "label": "SMC 2.1"
                                },
                                {
                                    "name": "smc_2_2",
                                    "label": "SMC 2.2"
                                },
                                {
                                    "name": "smc_2_3",
                                    "label": "SMC 2.3"
                                },
                                {
                                    "name": "smc_2_4",
                                    "label": "SMC 2.4"
                                },
                                {
                                    "name": "smc_2_5",
                                    "label": "SMC 2.5"
                                },
                                {
                                    "name": "smc_2_6",
                                    "label": "SMC 2.6"
                                },
                                {
                                    "name": "bmc_1_1",
                                    "label": "BMC 1.1"
                                },
                                {
                                    "name": "bmc_1_2",
                                    "label": "BMC 1.2"
                                },
                                {
                                    "name": "bmc_2_1",
                                    "label": "BMC 2.1"
                                },
                                {
                                    "name": "bmc_2_2",
                                    "label": "BMC 2.2"
                                },
                                {
                                    "name": "bmc_2_3",
                                    "label": "BMC 2.3"
                                },
                                {
                                    "name": "bmc_2_4",
                                    "label": "BMC 2.4"
                                },
                                {
                                    "name": "bmc_2_5",
                                    "label": "BMC 2.5"
                                },
                                {
                                    "name": "smm_1_1",
                                    "label": "SMM 1.1"
                                },
                                {
                                    "name": "bmm_1_1",
                                    "label": "BMM 1.1"
                                },
                                {
                                    "name": "other",
                                    "label": "Other"
                                },
                                {
                                    "name": "undecided",
                                    "label": "Undecided"
                                }
                            ],
                            "name": "which_government_house_model_do_you_prefer_to_build_"
                        }
                    ],
                    "name": "govt_model"
                },
                {
                    "bind": {
                        "relevant": "${Are_you_planning_to_build_one_} = 'no'",
                        "required": "true"
                    },
                    "label": "What type of house are you planning to build?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "stone_masonry_in_mud_mortar__s",
                            "label": "Stone Masonry in Mud Mortar (SMM)"
                        },
                        {
                            "name": "stone_masonry_in_cement_mortar",
                            "label": "Stone Masonry in Cement Mortar (SMC)"
                        },
                        {
                            "name": "brick_masonry_in_cement_mortar",
                            "label": "Brick Masonry in Cement Mortar (BMC)"
                        },
                        {
                            "name": "brick_masonry_in_mud_mortar__b",
                            "label": "Brick Masonry in Mud Mortar (BMM)"
                        },
                        {
                            "name": "reinforced_concrete_cement__rc",
                            "label": "Reinforced Concrete Cement (RCC)"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        },
                        {
                            "name": "rcc_category_a___b",
                            "label": "RCC Category A & B"
                        },
                        {
                            "name": "other",
                            "label": "Other"
                        }
                    ],
                    "name": "What_type_of_house_are_you_pla"
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_house_are_you_pla} = 'other'",
                        "required": "true"
                    },
                    "type": "text",
                    "name": "specify_the_type",
                    "label": "Specify the type"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "Do you have a bank account in any of the following banks",
                    "type": "select one",
                    "children": [
                        {
                            "name": "option_1",
                            "label": "Agriculture Development Bnak"
                        },
                        {
                            "name": "option_2",
                            "label": "Prabhu Bank"
                        }
                    ],
                    "name": "do_you_have_a_bank_account_in_any_of_the_following_banks"
                },
                {
                    "label": "Technical Evaluation",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "plot_",
                            "label": "Plot#"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "Ward",
                            "label": "Ward #"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "land_owner",
                            "label": "Land Owner"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Relationship of Beneficiary with Land Owner",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "self",
                                    "label": "Self"
                                },
                                {
                                    "name": "father_or_moth",
                                    "label": "Father or Mother"
                                },
                                {
                                    "name": "father_in_law_",
                                    "label": "Father-in-Law or Mother-in-Law"
                                },
                                {
                                    "name": "husband_or_wif",
                                    "label": "Husband or Wife"
                                },
                                {
                                    "name": "son_or_daughte",
                                    "label": "Son or Daughter"
                                },
                                {
                                    "name": "brother_or_sis",
                                    "label": "Brother or SIster"
                                },
                                {
                                    "name": "uncle_or_aunt",
                                    "label": "Uncle or Aunt"
                                },
                                {
                                    "name": "cousin",
                                    "label": "Cousin"
                                }
                            ],
                            "name": "relationship_of_beneficiary_with_land_owner"
                        }
                    ],
                    "name": "tech_evaluation"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "18391"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 24636,
        "name": "On-Site Survey",
        "json": {
            "name": "a7SwD4HmUoxMX7stGoSCc8_dfbPiSg",
            "name": "On-Site Survey",
            "sms_keyword": "a7SwD4HmUoxMX7stGoSCc8",
            "default_language": "default",
            "version": "18394",
            "id_string": "a7SwD4HmUoxMX7stGoSCc8",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "text",
                    "name": "data_collector",
                    "label": "Name of Data collector"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "date",
                    "name": "date",
                    "label": "Date"
                },
                {
                    "label": "Homeowner Information",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "house_ward",
                            "label": "House Ward"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "village_tole",
                            "label": "Village/Tole"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "cbs_slip_no",
                            "label": "CBS Slip #"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "integer",
                            "name": "cbs_slip",
                            "label": "CBS Slip Homeowner Serial #"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Status of the house",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "not_started_ye",
                                    "label": "Not-started yet"
                                },
                                {
                                    "name": "under_construc",
                                    "label": "Under-construction"
                                },
                                {
                                    "name": "construction_c",
                                    "label": "Construction completed"
                                },
                                {
                                    "name": "partially_dama",
                                    "label": "Partially damaged - possible retrofit"
                                }
                            ],
                            "name": "status_of_the_house"
                        }
                    ],
                    "name": "homeowner_info"
                },
                {
                    "label": "Site Evaluation",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the site need to have a retaining wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "does_the_site_need_to_have_a_retaining_wall_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the area Swampy, Marshy, or Waterlogged?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_area_swampy_marshy_or_waterlogged_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there any local drainage in the area?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_any_local_drainage_in_the_area_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is There Sufficient Space to Leave a 1.5 Meter Setback for a Road?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_sufficient_space_to_leave_a_1_5_meter_setback_for_a_road_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are there any trees in or Nearby the construction site?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_there_any_trees_in_or_nearby_the_construction_site_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What is the Soil Type of the Site According to the Nepal National Building Code, NBC 105 (1994)?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "type_i__rock_o",
                                    "label": "Type I, Rock or Stiff Soil Sites"
                                },
                                {
                                    "name": "type_ii__mediu",
                                    "label": "Type II: Medium Soil Sites"
                                },
                                {
                                    "name": "type_iiii__sof",
                                    "label": "Type IIII: Soft Soil Sites"
                                }
                            ],
                            "name": "what_is_the_soil_type_of_the_site_according_to_the_nepal_national_building_code_nbc_105_1994_"
                        }
                    ],
                    "name": "site_evaluation"
                },
                {
                    "label": "On-Site Information",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "geopoint",
                            "name": "house_location",
                            "label": "House Location"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo_of_current_destroyed_structure_site",
                            "label": "Photo of Current/Destroyed Structure/Site"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "What is the main source of water (post earthquake)?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "piped_water",
                                    "label": "Piped water"
                                },
                                {
                                    "name": "spring",
                                    "label": "Spring"
                                },
                                {
                                    "name": "pond",
                                    "label": "Pond"
                                },
                                {
                                    "name": "stream_river",
                                    "label": "Stream/river"
                                }
                            ],
                            "name": "what_is_the_main_source_of_water_post_earthquake_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "How far is the water (including both ways commuting time?)",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "less_than_30_m",
                                    "label": "Less than 30 min"
                                },
                                {
                                    "name": "30_min_to_60_m",
                                    "label": "30 min to 60 min"
                                },
                                {
                                    "name": "more_than_60_m",
                                    "label": "More than 60 min"
                                }
                            ],
                            "name": "how_far_is_the_water_including_both_ways_commuting_time_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the household has improved toilet (water-sealed toilet NOT pit latrine)?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Does_the_household_has_improve"
                        },
                        {
                            "bind": {
                                "relevant": "${Does_the_household_has_improve} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the toilet in full use and maintained?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_toilet_in_full_use_and_maintained_"
                        }
                    ],
                    "name": "on_site_info"
                },
                {
                    "label": "Construction Information",
                    "type": "group",
                    "children": [
                        {
                            "label": "Construction Requirement",
                            "type": "group",
                            "children": [
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "Are you planning to build the same house model that you chose during Personal Aggrement?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Are_you_planning_to_build_the_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Are_you_planning_to_build_the_} = 'no'",
                                        "required": "true"
                                    },
                                    "type": "text",
                                    "name": "house_model",
                                    "label": "Which House Model are you planning to build ?"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "Do you want to build an attic?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "do_you_want_to_build_an_attic_"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "Do you want to build a porch?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "do_you_want_to_build_a_porch_"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "What is the current status of your house?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "fully_demolish",
                                            "label": "Fully demolished, ground cleared ready for new construction"
                                        },
                                        {
                                            "name": "fully_destroye",
                                            "label": "Fully destroyed, ground needs to be cleared ready for new construction"
                                        },
                                        {
                                            "name": "partially_dest",
                                            "label": "Partially destroyed, building needs to be demolished and ground cleared ready for new construction"
                                        },
                                        {
                                            "name": "partially_dest_1",
                                            "label": "Partially destroyed, would be interested in retrofitting and keeping original house"
                                        },
                                        {
                                            "name": "destroyed_hous",
                                            "label": "Destroyed house has already been demolished and rebuilt"
                                        }
                                    ],
                                    "name": "what_is_the_current_status_of_your_house_"
                                }
                            ],
                            "name": "const_req"
                        },
                        {
                            "label": "Construction Methodology",
                            "type": "group",
                            "children": [
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "What labor do you plan to use to rebuild your house?",
                                    "type": "select all that apply",
                                    "children": [
                                        {
                                            "name": "i_will_build_i",
                                            "label": "I will build it myself"
                                        },
                                        {
                                            "name": "i_will_hire_ma",
                                            "label": "I will hire masons and builders to build it"
                                        },
                                        {
                                            "name": "my_neighbors_o",
                                            "label": "My neighbors or broader community will build it"
                                        },
                                        {
                                            "name": "i_don_t_know",
                                            "label": "I don't know"
                                        }
                                    ],
                                    "name": "what_labor_do_you_plan_to_use_to_rebuild_your_house_"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "Do you have salvage material which you plan to use to rebuild your house?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "do_you_have_salvage_material_which_you_plan_to_use_to_rebuild_your_house_"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "Have you identified / chosen a DUDBC certified mason for rebuilding your house ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "have_you_identified_chosen_a_dudbc_certified_mason_for_rebuilding_your_house_"
                                },
                                {
                                    "bind": {
                                        "required": "true"
                                    },
                                    "label": "When do you plan to start construction on your house?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "1st_quarter__j",
                                            "label": "1st Quarter (Jan-March)"
                                        },
                                        {
                                            "name": "2nd_quarter__a",
                                            "label": "2nd Quarter (April-June)"
                                        },
                                        {
                                            "name": "3rd_quarter__j",
                                            "label": "3rd Quarter (July-Sept)"
                                        },
                                        {
                                            "name": "4th_quarter__o",
                                            "label": "4th Quarter (Oct-Dec)"
                                        }
                                    ],
                                    "name": "when_do_you_plan_to_start_construction_on_your_house_"
                                }
                            ],
                            "name": "const_method"
                        },
                        {
                            "label": "Finance",
                            "type": "group",
                            "children": [
                                {
                                    "label": "First",
                                    "type": "group",
                                    "children": [
                                        {
                                            "bind": {
                                                "required": "true"
                                            },
                                            "label": "Have you received your first tranche?",
                                            "type": "select one",
                                            "children": [
                                                {
                                                    "name": "yes",
                                                    "label": "Yes"
                                                },
                                                {
                                                    "name": "no",
                                                    "label": "No"
                                                }
                                            ],
                                            "name": "have_you_received_your_first_tranche_"
                                        }
                                    ],
                                    "name": "first_inst"
                                },
                                {
                                    "bind": {
                                        "relevant": "${have_you_received_your_first_tranche_} = 'yes' and ${status_of_the_house} = 'partially_dama'"
                                    },
                                    "label": "Second",
                                    "type": "group",
                                    "children": [
                                        {
                                            "bind": {
                                                "required": "true"
                                            },
                                            "label": "Have you received your second tranche?",
                                            "type": "select one",
                                            "children": [
                                                {
                                                    "name": "yes",
                                                    "label": "Yes"
                                                },
                                                {
                                                    "name": "no",
                                                    "label": "No"
                                                }
                                            ],
                                            "name": "have_you_received_your_second_tranche_"
                                        }
                                    ],
                                    "name": "second_inst"
                                },
                                {
                                    "bind": {
                                        "relevant": "${have_you_received_your_second_tranche_} = 'yes'"
                                    },
                                    "label": "Third",
                                    "type": "group",
                                    "children": [
                                        {
                                            "bind": {
                                                "required": "true"
                                            },
                                            "label": "Have you received your third tranche?",
                                            "type": "select one",
                                            "children": [
                                                {
                                                    "name": "yes",
                                                    "label": "Yes"
                                                },
                                                {
                                                    "name": "no",
                                                    "label": "No"
                                                }
                                            ],
                                            "name": "have_you_received_your_third_tranche_"
                                        }
                                    ],
                                    "name": "third_inst"
                                }
                            ],
                            "name": "finance"
                        }
                    ],
                    "name": "const_info"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "18394"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20396,
        "name": "Corrective Action",
        "json": {
            "name": "aCcSDJ2CwgsUZsF9Xa6ED2_ARHzMiS",
            "name": "Corrective Action",
            "sms_keyword": "aCcSDJ2CwgsUZsF9Xa6ED2",
            "default_language": "default",
            "version": "4666",
            "id_string": "aCcSDJ2CwgsUZsF9Xa6ED2",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "text",
                    "name": "name_of_homeowner",
                    "label": "Name of Homeowner"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "District/ VDC",
                    "type": "select one",
                    "children": [
                        {
                            "name": "nuwakot___kaul",
                            "label": "Nuwakot , Kaule"
                        },
                        {
                            "name": "nuwakot___bhal",
                            "label": "Nuwakot , Bhalche"
                        },
                        {
                            "name": "rasuwa___thulo",
                            "label": "Rasuwa , Thulogaun"
                        },
                        {
                            "name": "makwanpur__gog",
                            "label": "Makwanpur, Gogane"
                        }
                    ],
                    "name": "district_vdc"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "integer",
                    "name": "ward_no_",
                    "label": "Ward No."
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "geopoint",
                    "name": "location",
                    "label": "Location"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "text",
                    "name": "name_of_data_collector",
                    "label": "Name of data collector"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "date",
                    "name": "date",
                    "label": "Date"
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "What kind of House is it?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "SMM",
                            "label": "Stone Masonry in Mud Mortar (SMM)"
                        },
                        {
                            "name": "SMC",
                            "label": "Stone Masonry in Cement Mortar (SMC)"
                        },
                        {
                            "name": "BMC",
                            "label": "Brick Masonry in Cement Mortar (BMC)"
                        },
                        {
                            "name": "BMM",
                            "label": "Brick Masonry in Mud Mortar (BMM)"
                        },
                        {
                            "name": "RCC",
                            "label": "Reinforced Concrete Cement (RCC)"
                        },
                        {
                            "name": "CM",
                            "label": "Confined Masonry"
                        },
                        {
                            "name": "RCCAB",
                            "label": "RCC Category A & B"
                        },
                        {
                            "name": "other",
                            "label": "Other"
                        }
                    ],
                    "name": "what_kind_of_house_is_it_"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Select Type of Correction : Final Inspection Stage",
                    "type": "select one",
                    "children": [
                        {
                            "name": "first_tranche",
                            "label": "First Tranche"
                        },
                        {
                            "name": "second_tranche",
                            "label": "Second Tranche"
                        },
                        {
                            "name": "third_tranche",
                            "label": "Third Tranche"
                        }
                    ],
                    "name": "select_type_of_correction_final_inspection_stage"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Select Type of correction - error",
                    "type": "select one",
                    "children": [
                        {
                            "name": "report_error_f",
                            "label": "Report error-for an engineer to update an incorrectly filled form"
                        },
                        {
                            "name": "corrective_mea",
                            "label": "Corrective measure-for homeowners who update to compliance at a later date"
                        }
                    ],
                    "name": "select_type_of_correction_error"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "text",
                    "name": "what_was_the_report_error_",
                    "label": "What was the report error?"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "text",
                    "name": "what_is_the_corrective_measure_",
                    "label": "What is the corrective measure?"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "text",
                    "name": "please_mention_the_reference_to_the_correction_manual_which_you_have_recommended_as_the_corrective_measure_",
                    "label": "Please mention the reference to the correction manual which you have recommended as the corrective measure."
                },
                {
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photos_of_correction",
                            "label": "Photos of correction"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photos_of_correction_0",
                            "label": "Photos of correction"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photos_of_correction_0_0",
                            "label": "Photos of correction"
                        }
                    ],
                    "name": "group_gc2hd82"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "signature_of_data_collector",
                    "label": "Signature of data collector"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Is the house compliant according to the inspection guidelines?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "Is_the_house_compliant_accordi"
                },
                {
                    "bind": {
                        "relevant": "${Is_the_house_compliant_accordi} = 'no'",
                        "required": "false"
                    },
                    "type": "text",
                    "name": "if_the_house_is_non_compliant_",
                    "label": "If the house is non compliant, Explain why?"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4666"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20381,
        "name": "Third Tranche",
        "json": {
            "name": "apLqPUhXmW7Vnn577aeB4a_pJEDglj",
            "name": "Third Tranche",
            "sms_keyword": "apLqPUhXmW7Vnn577aeB4a",
            "default_language": "default",
            "version": "4781",
            "id_string": "apLqPUhXmW7Vnn577aeB4a",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "Which type of building is it ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_b",
                            "label": "RCC A&B"
                        }
                    ],
                    "name": "Which_type_of_building_is_it_"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_xj4qa82",
                    "bind": {
                        "relevant": "${Which_type_of_building_is_it_} != 'rcc' and ${Which_type_of_building_is_it_} != 'rcc_a_b'"
                    },
                    "label": "All Typology",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "datetime",
                            "name": "date",
                            "label": "Date"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "name_of_data_collector",
                            "label": "Name of Data Collector"
                        },
                        {
                            "bind": {
                                "relevant": "${Which_type_of_building_is_it_} = 'smc' or ${Which_type_of_building_is_it_} = 'bmc'",
                                "required": "true"
                            },
                            "label": "Does the building have RCC slab or Roof ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Does_the_building_have_RCC_sla"
                        },
                        {
                            "bind": {
                                "relevant": "${Does_the_building_have_RCC_sla} = 'no' or ${Which_type_of_building_is_it_} = 'bmm' or ${Which_type_of_building_is_it_} = 'smm'",
                                "required": "true"
                            },
                            "label": "Is the wood material light comprising wooden or steel truss and covered with CGI sheets?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_wood_material_light_comprising_wooden_or_steel_truss_and_covered_with_cgi_sheets_"
                        },
                        {
                            "bind": {
                                "relevant": "${Does_the_building_have_RCC_sla} = 'no' or ${Which_type_of_building_is_it_} = 'smm' or ${Which_type_of_building_is_it_} = 'bmm'",
                                "required": "true"
                            },
                            "label": "Are all members of the timber truss or joints properly connected?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_all_members_of_the_timber_truss_or_joints_properly_connected_"
                        },
                        {
                            "bind": {
                                "relevant": "${Does_the_building_have_RCC_sla} = 'no' or ${Which_type_of_building_is_it_} = 'smm' or ${Which_type_of_building_is_it_} = 'bmm'",
                                "required": "true"
                            },
                            "label": "Is the roof properly connected to the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_roof_properly_connected_to_the_wall_"
                        },
                        {
                            "bind": {
                                "relevant": "${Does_the_building_have_RCC_sla} = 'no' or ${Which_type_of_building_is_it_} = 'smm' or ${Which_type_of_building_is_it_} = 'bmm'",
                                "required": "true"
                            },
                            "label": "Is diagonal bracings provided for flexible roofs like timber or steel?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_diagonal_bracings_provided_for_flexible_roofs_like_timber_or_steel_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "recommendation_monitor_all",
                            "label": "Recommnedation"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "Photos_monitor_all",
                            "label": "Photos"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_if_required_",
                            "label": "Photo (If required)"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_if_required__0",
                            "label": "Photo (If required)"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "comments",
                            "label": "Comments"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_nh5ti89",
                    "bind": {
                        "relevant": "${Which_type_of_building_is_it_} = 'confined_masonry'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "date",
                            "name": "date",
                            "label": "Date"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "name_of_the_recorder",
                            "label": "Name of the Recorder"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the gable made of light materials?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_gable_made_of_light_materials_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Area all members of the timber truss or joints properly connected?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "area_all_members_of_the_timber_truss_or_joints_properly_connected_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the roof properly connected to the walls?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_roof_properly_connected_to_the_walls_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the roof of timber, steel or concrete?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_roof_of_timber_steel_or_concrete_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is diagonal bracing provided to connect the trusses in the direction opposite to the span of the truss?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_diagonal_bracing_provided_to_connect_the_trusses_in_the_direction_opposite_to_the_span_of_the_truss_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is diagonal bracing provided to connect the trusses in the direction opposite to the span of the truss?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_diagonal_bracing_provided_to_connect_the_trusses_in_the_direction_opposite_to_the_span_of_the_truss__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "Recommendation_confined_masona",
                            "label": "Recommendation"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "Photos_confined_masonary",
                            "label": "Photos"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_if_required_",
                            "label": "Photo (If Required)"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo_if_required__0",
                            "label": "Photo (If Required)"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "comments",
                            "label": "Comments"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ed97y30",
                    "bind": {
                        "relevant": "${Which_type_of_building_is_it_} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "date",
                            "name": "date_0",
                            "label": "Date"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "name_of_the_recorder_0",
                            "label": "Name of the recorder"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the thickness of slab at least 125 mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_thickness_of_slab_at_least_125_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the bottom slab rebar at least 8 mm dia in both direction (Fe 415 or Fe 500) and at 6” C/C ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_bottom_slab_rebar_at_least_8_mm_dia_in_both_direction_fe_415_or_fe_500_and_at_6_c_c_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the top Reinforcement for slab at continuous section at least 8mm dia, a maximum of 0.3 L or Ld in length and at 6” C/C ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_top_reinforcement_for_slab_at_continuous_section_at_least_8mm_dia_a_maximum_of_0_3_l_or_ld_in_length_and_at_6_c_c_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the top reinforcement for slab at discontinuous section at least 8mm dia, a maximum of 0.15 L or Ld in length and at 6” C/C ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_top_reinforcement_for_slab_at_discontinuous_section_at_least_8mm_dia_a_maximum_of_0_15_l_or_ld_in_length_and_at_6_c_c_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the top reinforcement for slab at cantilever section at least 8mm dia and throughout?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_top_reinforcement_for_slab_at_cantilever_section_at_least_8mm_dia_and_throughout_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "Recommendation_RCC",
                            "label": "Recommendation"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo",
                            "label": "Photo"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo_if_required_",
                            "label": "Photo (If Required)"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "photo",
                            "name": "photo_if_required__0",
                            "label": "Photo (If Required)"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "type": "text",
                            "name": "comments",
                            "label": "Comments"
                        }
                    ]
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "label": "Is the house Compliant according to inspection Guideline?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "yes",
                            "label": "Yes"
                        },
                        {
                            "name": "no",
                            "label": "No"
                        }
                    ],
                    "name": "Is_the_house_Compliant_accordi"
                },
                {
                    "bind": {
                        "relevant": "${Is_the_house_Compliant_accordi} = 'no'",
                        "required": "false"
                    },
                    "type": "text",
                    "name": "if_the_house_is_non_compliant_explain_why_",
                    "label": "If the house is Non-Compliant, explain why?"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4781"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20380,
        "name": "Second Tranche- Joint",
        "json": {
            "name": "a8JEVJzKHoC3ArQrkY2tTU_o40joPY",
            "name": "Second Tranche- Joint",
            "sms_keyword": "a8JEVJzKHoC3ArQrkY2tTU",
            "default_language": "default",
            "version": "4723",
            "id_string": "a8JEVJzKHoC3ArQrkY2tTU",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What type of building is it?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_b",
                            "label": "RCC A&B"
                        },
                        {
                            "name": "option_3",
                            "label": "Others"
                        }
                    ],
                    "name": "What_type_of_building_is_it"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ms7ge64",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Are the rebar of beam at junction bent into columns for a length of at least 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_rebar_of_beam_at_junction_bent_into_columns_for_a_length_of_at_least_60_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there at least two Stirrups in the joints?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_at_least_two_stirrups_in_the_joints_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_fc3dx81",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc_a_b'"
                    },
                    "label": "RCC A&B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of beam less than pillar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_beam_less_than_pillar_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the joint detailing provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_joint_detailing_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there at least two rings provided in the joints?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_at_least_two_rings_provided_in_the_joints_"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc' or ${What_type_of_building_is_it} = 'rcc_a_b'",
                        "required": "true"
                    },
                    "type": "photo",
                    "name": "add_photo_",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc' or ${What_type_of_building_is_it} = 'rcc_a_b'",
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "note",
                    "name": "there_are_no_joints_in_other_type_houses_other_than_rcc_and_rcca_b",
                    "label": "There are no joints in other type houses other than RCC and RCCA&B"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4723"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20379,
        "name": "Second Tranche- Floor",
        "json": {
            "name": "aqxC6UV8ykvcFgZnSw35Lo_rM2E2fV",
            "name": "Second Tranche- Floor",
            "sms_keyword": "aqxC6UV8ykvcFgZnSw35Lo",
            "default_language": "default",
            "version": "4721",
            "id_string": "aqxC6UV8ykvcFgZnSw35Lo",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What type of building is it?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_b",
                            "label": "RCC A&B"
                        },
                        {
                            "name": "AUTOMATIC",
                            "label": "Others"
                        }
                    ],
                    "name": "What_type_of_building_is_it"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_hr2no27",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the level of the floor same?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_floor_same_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the openings of the floor equal to or less than 25%?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_openings_of_the_floor_equal_to_or_less_than_25_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the floor at least 125 mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_floor_at_least_125_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar minimum 8 mm rod at 6 inch c/c in both directions?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_minimum_8_mm_rod_at_6_inch_c_c_in_both_directions_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Concrete cover at least 15 mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_cover_at_least_15_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the overhang equal to or less than 1m from center of pillar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_overhang_equal_to_or_less_than_1m_from_center_of_pillar_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_wg4zf12",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc_a_b'"
                    },
                    "label": "RCC A&B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the level of the floor as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_level_of_the_floor_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the openings of the floor maximum 25%?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_openings_of_the_floor_maximum_25_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the depth of the floor as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_depth_of_the_floor_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar size and detailing provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_size_and_detailing_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is a minimum cover of 15mm provided throughout the floor?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_a_minimum_cover_of_15mm_provided_throughout_the_floor_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the overhang provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_overhang_provided_as_per_approved_design_"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc' or ${What_type_of_building_is_it} = 'rcc_a_b'",
                        "required": "true"
                    },
                    "type": "photo",
                    "name": "add_photo_",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc' or ${What_type_of_building_is_it} = 'rcc_a_b'",
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc' or ${What_type_of_building_is_it} = 'rcc_a_b'",
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'AUTOMATIC'",
                        "required": "false"
                    },
                    "type": "note",
                    "name": "no_question_available_for_houses_other_than_rcc_and_rcca_b",
                    "label": "No question available for houses other than RCC and RCCA&B"
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4721"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20378,
        "name": "Second Tranche- Doors and Windows",
        "json": {
            "name": "auE2PEpDYngrGBdyBoobUF_an9amPg",
            "name": "Second Tranche- Doors and Windows",
            "sms_keyword": "auE2PEpDYngrGBdyBoobUF",
            "default_language": "default",
            "version": "4720",
            "id_string": "auE2PEpDYngrGBdyBoobUF",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What type of building is it?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_b",
                            "label": "RCC A&B"
                        }
                    ],
                    "name": "What_type_of_building_is_it"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ts8hm18",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smm' or ${What_type_of_building_is_it} = 'bmm'"
                    },
                    "label": "SMM/BMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Are openings located away from the inside corners by a clear distance equal to at least 1/4th of the height of the opening but not less than 600mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_openings_located_away_from_the_inside_corners_by_a_clear_distance_equal_to_at_least_1_4th_of_the_height_of_the_opening_but_not_less_than_600mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the total length of openings in walls less than 30% of the length of the wall between consecutive cross-walls?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_total_length_of_openings_in_walls_less_than_30_of_the_length_of_the_wall_between_consecutive_cross_walls_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the distance between two openings not less than 600mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_distance_between_two_openings_not_less_than_600mm_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ya0ei32",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smc' or ${What_type_of_building_is_it} = 'bmc'"
                    },
                    "label": "SMC/BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are openings located away from the inside corners by a clear distance not less than 600mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_openings_located_away_from_the_inside_corners_by_a_clear_distance_not_less_than_600mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the total length of openings in walls less than 50% of the length of the wall between consecutive cross-walls in single storey construction and 42% in two storey construction?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_total_length_of_openings_in_walls_less_than_50_of_the_length_of_the_wall_between_consecutive_cross_walls_in_single_storey_construction_and_42_in_two_storey_construction_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the distance between two openings not less than 600mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_distance_between_two_openings_not_less_than_600mm__0"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smc' or ${What_type_of_building_is_it} = 'bmm' or ${What_type_of_building_is_it} = 'smm' or ${What_type_of_building_is_it} = 'bmc'",
                        "required": "true"
                    },
                    "type": "photo",
                    "name": "add_photo_",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0",
                    "label": "Add photo."
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4720"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20377,
        "name": "Second Tranche- Horizontal Band/Beam",
        "json": {
            "name": "a86rwnQP5QHCSUjgosnkx5_lRUXi52",
            "name": "Second Tranche- Horizontal Band/Beam",
            "sms_keyword": "a86rwnQP5QHCSUjgosnkx5",
            "default_language": "default",
            "version": "4719",
            "id_string": "a86rwnQP5QHCSUjgosnkx5",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What type of building is it?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_b",
                            "label": "RCC A&B"
                        }
                    ],
                    "name": "What_type_of_building_is_it"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_da14h82",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc_a_b'"
                    },
                    "label": "RCC A&B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the position of the beams as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_position_of_the_beams_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of the beams as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_beams_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the rebar size and detailing provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_size_and_detailing_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the ring provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_ring_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the connections provided adequate as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_connections_provided_adequate_as_per_approved_design_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_dc2zs02",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the junctions of the Beams positioned in the Pillar and Does the beam connects all Pillars?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_junctions_of_the_beams_positioned_in_the_pillar_and_does_the_beam_connects_all_pillars_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size beam at least 9 inches X 14 inches and less than size of pillar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_beam_at_least_9_inches_x_14_inches_and_less_than_size_of_pillar_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the stirrups at least 8mm diameter and at 4 inch c/c at ends and joints and 6 inch at middle?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_stirrups_at_least_8mm_diameter_and_at_4_inch_c_c_at_ends_and_joints_and_6_inch_at_middle_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Splicing of Top rebar placed in middle and for bottom rebar placed at 2 feet away from Pillars and Overlap of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_splicing_of_top_rebar_placed_in_middle_and_for_bottom_rebar_placed_at_2_feet_away_from_pillars_and_overlap_of_60_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_vs3ig23",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'confined_masonry'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is a continuous sill band of at least 75 mm depth and width equal to the width of the wall provided throughout the entire level at the bottom level of the window?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_a_continuous_sill_band_of_at_least_75_mm_depth_and_width_equal_to_the_width_of_the_wall_provided_throughout_the_entire_level_at_the_bottom_level_of_the_window_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement provided of at least 2 bars of 10mm diameter and hooks provided of 7mm diameter bars at the spacing of 150mm center to center?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_provided_of_at_least_2_bars_of_10mm_diameter_and_hooks_provided_of_7mm_diameter_bars_at_the_spacing_of_150mm_center_to_center_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement used of high strength deformed bars of Fe 415MPa?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_used_of_high_strength_deformed_bars_of_fe_415mpa_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is a continuous Lintel band of at least 75 mm depth and width equal to the width of the wall provided throughout the entire the entire level at the bottom level of the window?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_a_continuous_lintel_band_of_at_least_75_mm_depth_and_width_equal_to_the_width_of_the_wall_provided_throughout_the_entire_the_entire_level_at_the_bottom_level_of_the_window_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement provided of at least 2 bars of 10mm diameter and hooks provided of 7mm diameter bars at the spacing of 150mm center to center?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_provided_of_at_least_2_bars_of_10mm_diameter_and_hooks_provided_of_7mm_diameter_bars_at_the_spacing_of_150mm_center_to_center__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement used of high strength deformed bars of Fe 415MPa?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_used_of_high_strength_deformed_bars_of_fe_415mpa__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is a continuous floor/roof band provided throughout the entire wall at the top of the walls at the floor level?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_a_continuous_floor_roof_band_provided_throughout_the_entire_wall_at_the_top_of_the_walls_at_the_floor_level_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the minimum width and depth of the ring/floor beam less than 200mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_minimum_width_and_depth_of_the_ring_floor_beam_less_than_200mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the main reinforcement bars at the roof/floor band, 4-10mm diameter and are 7mm diameter rings provided at a spacing of 150mm center to center with minimum hooks of 50mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_main_reinforcement_bars_at_the_roof_floor_band_4_10mm_diameter_and_are_7mm_diameter_rings_provided_at_a_spacing_of_150mm_center_to_center_with_minimum_hooks_of_50mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement used of high strength deformed bars of Fe 415?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_used_of_high_strength_deformed_bars_of_fe_415_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3__0_0"
                        }
                    ]
                },
                {
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smc' or ${What_type_of_building_is_it} = 'bmc'"
                    },
                    "label": "SMC/BMC",
                    "type": "group",
                    "children": [
                        {
                            "control": {
                                "appearance": "field-list"
                            },
                            "label": "SMC/BMC",
                            "type": "group",
                            "children": [
                                {
                                    "bind": {
                                        "required": "false"
                                    },
                                    "label": "Is a horizontal sill band provided throughout the entire wall at the bottom level of the windows and it's width equal to width of wall?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_a_horizontal_sill_band_prov"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_a_horizontal_sill_band_prov} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the sill band of timber or RC ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "timber",
                                            "label": "Timber"
                                        },
                                        {
                                            "name": "rc",
                                            "label": "RC"
                                        }
                                    ],
                                    "name": "Is_the_sill_band_of_timber_or_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_sill_band_of_timber_or_} = 'rc'",
                                        "required": "false"
                                    },
                                    "label": "Is the thickness of the band 75mm or more?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_thickness_of_the_band_7"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_thickness_of_the_band_7} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_sill_band_of_timber_or_} = 'rc'",
                                        "required": "false"
                                    },
                                    "label": "Is the main reinforcement 2 no of 12mm dia rebars in case of 75mm plinth with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_main_reinforcement_2_no"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_main_reinforcement_2_no} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                                },
                                {
                                    "bind": {
                                        "required": "false"
                                    },
                                    "label": "Is a horizontal lintel band provided throughout the entire wall at the top level of the windows and it's width equal to width of wall?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_a_horizontal_lintel_band_pr"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_a_horizontal_lintel_band_pr} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the lintel band of timber or RC ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "timber",
                                            "label": "Timber"
                                        },
                                        {
                                            "name": "rc",
                                            "label": "RC"
                                        }
                                    ],
                                    "name": "Is_the_lintel_band_of_timber_o"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_lintel_band_of_timber_o} = 'rc'",
                                        "required": "false"
                                    },
                                    "label": "Is the width of the opening less than 1.25m and masonry height above the lintel less than 0.9m?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_width_of_the_opening_le"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_width_of_the_opening_le} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the thick ness of the lintel band at least 75mm and the main reinforcement 2 nos of 12mm dia rebars with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_thick_ness_of_the_linte"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_thick_ness_of_the_linte} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_thick_ness_of_the_linte} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_width_of_the_opening_le} = 'no'",
                                        "required": "false"
                                    },
                                    "label": "Is the thickness of the lintel band at least 150mm and the main reinforcement 4 nos of 12mm dia rebars with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_thick_ness_of_the_linte_001"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_thick_ness_of_the_linte_001} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_thick_ness_of_the_linte_001} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0"
                                },
                                {
                                    "bind": {
                                        "required": "false"
                                    },
                                    "label": "Is a horizontal Roof band provided throughout the entire wall at the top level of the wall and it's width equal to width of wall?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_a_horizontal_Roof_band_prov"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_a_horizontal_Roof_band_prov} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the roof band of timber or RC ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "timber",
                                            "label": "Timber"
                                        },
                                        {
                                            "name": "rc",
                                            "label": "RC"
                                        }
                                    ],
                                    "name": "Is_the_roof_band_of_timber_or_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_roof_band_of_timber_or_} = 'rc'",
                                        "required": "false"
                                    },
                                    "label": "Is the thick ness of the roof band at least 75mm and the main reinforcement 2 nos of 12mm dia rebars with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_thick_ness_of_the_roof_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_thick_ness_of_the_roof_} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0_0"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_thick_ness_of_the_roof_} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0"
                                },
                                {
                                    "bind": {
                                        "required": "false"
                                    },
                                    "label": "Are stitches provided at corners and junctions of length upto the adjacent openings or 1.2m or more?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Are_stitches_provided_at_corne"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Are_stitches_provided_at_corne} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the minimum thickness of the stitch 75mm with at least two 12mm dia rebars?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_minimum_thickness_of_th"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_minimum_thickness_of_th} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0_0_0"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_minimum_thickness_of_th} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0_0"
                                }
                            ],
                            "name": "group_xr5eg95"
                        },
                        {
                            "control": {
                                "appearance": "field-list"
                            },
                            "name": "group_gz8kl86",
                            "bind": {
                                "relevant": "${What_type_of_building_is_it} = 'bmc'"
                            },
                            "label": "BMC",
                            "type": "group",
                            "children": [
                                {
                                    "bind": {
                                        "required": "false"
                                    },
                                    "label": "Is the gable present?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_gable_present"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_gable_present} = 'yes'",
                                        "required": "false"
                                    },
                                    "label": "Is the gable wall provided light like wood, CGI sheet, etc.?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_the_gable_wall_provided_lig"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_gable_wall_provided_lig} = 'no'",
                                        "required": "false"
                                    },
                                    "label": "Is confining beamof 75mm depth and main reinforcement 2 nos of 12mm dia rebars with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm provided around the top of gable wall?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "Is_confining_beamof_75mm_depth"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_the_gable_present} = 'no'",
                                        "required": "false"
                                    },
                                    "label": "Is RCC slab floor/roof provided?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_rcc_slab_floor_roof_provided_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_confining_beamof_75mm_depth} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Is the thickness of slab at least 125 mm?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_thickness_of_slab_at_least_125_mm_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_confining_beamof_75mm_depth} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Are the bottom slab rebar at least 8 mm dia in both direction (Fe 415 or Fe 500) and at 6” C/C ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "are_the_bottom_slab_rebar_at_least_8_mm_dia_in_both_direction_fe_415_or_fe_500_and_at_6_c_c_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_confining_beamof_75mm_depth} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Are the top Reinforcement for slab at continuous section at least 8mm dia, a maximum of 0.3 L or Ld in length and at 6” C/C ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "are_the_top_reinforcement_for_slab_at_continuous_section_at_least_8mm_dia_a_maximum_of_0_3_l_or_ld_in_length_and_at_6_c_c_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_confining_beamof_75mm_depth} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Are the top reinforcement for slab at discontinuous section at least 8mm dia, a maximum of 0.15 L or Ld in length and at 6” C/C ?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "are_the_top_reinforcement_for_slab_at_discontinuous_section_at_least_8mm_dia_a_maximum_of_0_15_l_or_ld_in_length_and_at_6_c_c_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_confining_beamof_75mm_depth} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Are the top reinforcement for slab at cantilever section at least 8mm diameter and throughout?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "are_the_top_reinforcement_for_slab_at_cantilever_section_at_least_8mm_diameter_and_throughout_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_confining_beamof_75mm_depth} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Is the concrete of mix ratio 1:1.5:3?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_concrete_of_mix_ratio_1_1_5_3_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_confining_beamof_75mm_depth} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Is the rebar high strength deformed bars with at least Fy=415MPa?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "is_the_rebar_high_strength_deformed_bars_with_at_least_fy_415mpa_"
                                },
                                {
                                    "bind": {
                                        "relevant": "${Is_confining_beamof_75mm_depth} = 'yes'",
                                        "required": "true"
                                    },
                                    "label": "Are rebars of slab inserted into the floor beam with at least 60 times diameter of bar embedded into the beam?",
                                    "type": "select one",
                                    "children": [
                                        {
                                            "name": "yes",
                                            "label": "Yes"
                                        },
                                        {
                                            "name": "no",
                                            "label": "No"
                                        }
                                    ],
                                    "name": "are_rebars_of_slab_inserted_into_the_floor_beam_with_at_least_60_times_diameter_of_bar_embedded_into_the_beam_"
                                }
                            ]
                        }
                    ],
                    "name": "group_xs9ua61"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_wi3ni82",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smm' or ${What_type_of_building_is_it} = 'bmm'"
                    },
                    "label": "SMM/BMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is a horizontal sill band provided throughout the entire wall at the bottom level of the windows and it's width equal to width of wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_a_horizontal_sill_band_provided_throughout_the_entire_wall_at_the_bottom_level_of_the_windows_and_it_s_width_equal_to_width_of_wall_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the sill band of timber or RC ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "rc",
                                    "label": "RC"
                                }
                            ],
                            "name": "Is_the_sill_band_of_timber_or__001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_sill_band_of_timber_or__001} = 'timber'",
                                "required": "false"
                            },
                            "label": "Is the sill band of timber and house more than one storey?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_sill_band_of_timber_and"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_sill_band_of_timber_and} = 'no'",
                                "required": "false"
                            },
                            "label": "Are two 75mm x 38mm members used and connected with batten of 50mm x 30mm size at a spacing of 500mm c/c or less?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_two_75mm_x_38mm_members_used_and_connected_with_batten_of_50mm_x_30mm_size_at_a_spacing_of_500mm_c_c_or_less_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_sill_band_of_timber_and} = 'no'",
                                "required": "false"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_sill_band_of_timber_or__001} = 'rc'",
                                "required": "false"
                            },
                            "label": "Is the thickness of the band 75mm or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_thickness_of_the_band_7_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thickness_of_the_band_7_001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the concrete at least M15 grade or mix ratio 1:2;4, without surface cracks, no rebars exposed and with clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m15_grade_or_mix_ratio_1_2_4_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_sill_band_of_timber_or__001} = 'rc'",
                                "required": "false"
                            },
                            "label": "Is the main reinforcement 2 no of 12mm dia rebars in case of 75mm plinth with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_main_reinforcement_2_no_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_main_reinforcement_2_no_001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0_0_0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is a horizontal lintel band provided throughout the entire wall at the top level of the windows and it's width equal to width of wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_a_horizontal_lintel_band_pr_001"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the width of the opening less than 1.25m and masonry height above the lintel less than 0.9m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_opening_less_than_1_25m_and_masonry_height_above_the_lintel_less_than_0_9m_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_a_horizontal_lintel_band_pr_001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the lintel band of timber or RC ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "rc",
                                    "label": "RC"
                                }
                            ],
                            "name": "Is_the_lintel_band_of_timber_o_001"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the lintel band of timber and house more than one storey?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_lintel_band_of_timber_a"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_lintel_band_of_timber_a} = 'no'",
                                "required": "false"
                            },
                            "label": "Are two 75mm x 38mm members used and connected with batten of 50mm x 30mm size at a spacing of 500mm c/c or less?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_two_75mm_x_38mm_members_used_and_connected_with_batten_of_50mm_x_30mm_size_at_a_spacing_of_500mm_c_c_or_less__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_lintel_band_of_timber_a} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_lintel_band_of_timber_o_001} = 'rc'",
                                "required": "false"
                            },
                            "label": "Is the width of the opening less than 1.25m and masonry height above the lintel less than 0.9m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_width_of_the_opening_le_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_width_of_the_opening_le_001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the thickness of the lintel band at least 75mm and the main reinforcement 2 nos of 12mm dia rebars with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_thick_ness_of_the_linte_002"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thick_ness_of_the_linte_002} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the concrete atleast M15 grade or mix ratio 1:2;4, without surface cracks, no rebars exposed and with clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_atleast_m15_grade_or_mix_ratio_1_2_4_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thick_ness_of_the_linte_002} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0_0_0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_lintel_band_of_timber_o_001} = 'rc' and ${Is_the_width_of_the_opening_le_001} = 'no'",
                                "required": "false"
                            },
                            "label": "Is the thickness of the lintel band atleast 150mm and the main reinforcement 4 nos of 12mm dia rebars with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_thickness_of_the_lintel"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thickness_of_the_lintel} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the concrete atleast M15 grade or mix ratio 1:2;4, without surface cracks, no rebars exposed and with clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_atleast_m15_grade_or_mix_ratio_1_2_4_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thickness_of_the_lintel} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0_0_0_0_0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is a horizontal Floor/Roof band provided throughout the entire wall at the top level of the wall and it's width equal to width of wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_a_horizontal_Floor_Roof_ban"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_a_horizontal_Floor_Roof_ban} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the roof band of timber or RC ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "rc",
                                    "label": "RC"
                                }
                            ],
                            "name": "Is_the_roof_band_of_timber_or__001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_roof_band_of_timber_or__001} = 'timber'",
                                "required": "true"
                            },
                            "label": "Is the roof band of timber and house more than one storey?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_roof_band_of_timber_and"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_roof_band_of_timber_and} = 'no'",
                                "required": "false"
                            },
                            "label": "Are two 75mm x 38mm members used and connected with batten of 50mm x 30mm size at a spacing of 500mm c/c or less?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_two_75mm_x_38mm_members_used_and_connected_with_batten_of_50mm_x_30mm_size_at_a_spacing_of_500mm_c_c_or_less__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_roof_band_of_timber_and} = 'no'",
                                "required": "true"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_roof_band_of_timber_or__001} = 'rc'",
                                "required": "false"
                            },
                            "label": "Is the thick ness of the roof band atleast 75mm and the main reinforcement 2 nos of 12mm dia rebars with 6mm dia stirrups at 150mm c/c and have a clear cover of 25mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_thick_ness_of_the_roof__001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thick_ness_of_the_roof__001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the concrete atleast M15 grade or mix ratio 1:2;4, without surface cracks, no rebars exposed and with clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_atleast_m15_grade_or_mix_ratio_1_2_4_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_thick_ness_of_the_roof__001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0_0_0_0_0_0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Are stitches provided at corners and junctions of length upto the adjacent openings or 1.2m or more?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Are_stitches_provided_at_corne_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Are_stitches_provided_at_corne_001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the Stitch of Timber or RCC?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "rcc",
                                    "label": "RCC"
                                }
                            ],
                            "name": "Is_the_Stitch_of_Timber_or_RCC"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_Stitch_of_Timber_or_RCC} = 'timber'",
                                "required": "false"
                            },
                            "label": "Are two 75mm x 38mm members used and connected with batten of 50mm x 30mm size at a spacing of 500mm c/c or less ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_two_75mm_x_38mm_members_used_and_connected_with_batten_of_50mm_x_30mm_size_at_a_spacing_of_500mm_c_c_or_less__0_0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_Stitch_of_Timber_or_RCC} = 'timber'",
                                "required": "true"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives__0_0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_Stitch_of_Timber_or_RCC} = 'rcc'",
                                "required": "false"
                            },
                            "label": "Is the minimum thickness of the stitch 75mm with atleast two 8mm dia rebars?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_minimum_thickness_of_the_stitch_75mm_with_atleast_two_8mm_dia_rebars_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_Stitch_of_Timber_or_RCC} = 'rcc'",
                                "required": "true"
                            },
                            "label": "Is the concrete atleast M15 grade or mix ratio 1:2;4, without surface cracks, no rebars exposed and with clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_atleast_m15_grade_or_mix_ratio_1_2_4_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth__0_0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_Stitch_of_Timber_or_RCC} = 'rcc'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0_0_0_0_0_0_0_0_0"
                        }
                    ]
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "photo",
                    "name": "add_photo_",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0_0",
                    "label": "Add photo."
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4719"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20376,
        "name": "Second Tranche- Vertical Members Pillars",
        "json": {
            "name": "apkVnQgCGkNBvWXQeAprbR_iz7Yvzw",
            "name": "Second Tranche- Vertical Members Pillars",
            "sms_keyword": "apkVnQgCGkNBvWXQeAprbR",
            "default_language": "default",
            "version": "8097",
            "id_string": "apkVnQgCGkNBvWXQeAprbR",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What type of building is it?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_b",
                            "label": "RCC A&B"
                        }
                    ],
                    "name": "What_type_of_building_is_it"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ha8qn95",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc_a_b'"
                    },
                    "label": "RCC A&B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Are the pillars in the same line in each direction?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_pillars_in_the_same_line_in_each_direction_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there presence of short column in the building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_presence_of_short_column_in_the_building_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of the pillar section as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_pillar_section_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the re bar size and detailing provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_re_bar_size_and_detailing_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the concrete quality and mix ratio as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_quality_and_mix_ratio_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the ring provided as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_ring_provided_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the connections provided adequate as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_connections_provided_adequate_as_per_approved_design_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_bp2lh70",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the pillar aligned in one line?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_pillar_aligned_in_one_line_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is short column avoided in the structure?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_short_column_avoided_in_the_structure_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the pillar size at least 12 inches X 12 inches?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_pillar_size_at_least_12_inches_x_12_inches_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the re bar at ground and first floor 4 numbers of 16 mm + 4 numbers of 12 mm and third floor 8 numbers of 12 mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_re_bar_at_ground_and_first_floor_4_numbers_of_16_mm_4_numbers_of_12_mm_and_third_floor_8_numbers_of_12_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the stirrups at least 8 mm diameter and at 4 inch c/c at ends and joints and 6 inch at middle?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_stirrups_at_least_8_mm_diameter_and_at_4_inch_c_c_at_ends_and_joints_and_6_inch_at_middle_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Lapping in the middle leaving 2 ft from edge and not more than 50% at one section and overlap of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_lapping_in_the_middle_leaving_2_ft_from_edge_and_not_more_than_50_at_one_section_and_overlap_of_60_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_kb9zr06",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'confined_masonry'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is there a Tie column provided at each corners, wall intersections and on either side of the doors?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_a_tie_column_provided_at_each_corners_wall_intersections_and_on_either_side_of_the_doors_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the size of all Tie columns at least equal to the width of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_all_tie_columns_at_least_equal_to_the_width_of_the_wall_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical reinforcement in Tie column at least 4 bars of 12 mm diameter and 7 mm diameter bar stirrups placed at 150 mm center to center?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_reinforcement_in_tie_column_at_least_4_bars_of_12_mm_diameter_and_7_mm_diameter_bar_stirrups_placed_at_150_mm_center_to_center_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the reinforcement used of high strength deformed bars of Fe 415 MPa?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_reinforcement_used_of_high_strength_deformed_bars_of_fe_415_mpa_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is a single vertical reinforcement bar of at least 12mm dia provided on either side of the windows, starting from the plinth beam and continuous to the roof beam? (The bar should be centered in the adjacent hollow block cell and grouted with cement mortar of at least 1:5 ratio)",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_a_single_vertical_reinforcement_bar_of_at_least_12mm_dia_provided_on_either_side_of_the_windows_starting_from_the_plinth_beam_and_continuous_to_the_roof_beam_the_bar_should_be_centered_in_the_adjacent_hollow_block_cell_and_grouted_with_cement_mortar_of_at_least_1_5_ratio_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ed4bt04",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'bmc'"
                    },
                    "label": "BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the height of wall from floor level to floor level more than 3m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_wall_from_floor_level_to_floor_level_more_than_3m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the height of attic wall from floor level to eaves level more than 1m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_attic_wall_from_floor_level_to_eaves_level_more_than_1m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the height from the attic floor to the ridge level more than 1.8m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_from_the_attic_floor_to_the_ridge_level_more_than_1_8m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member placed at all corners, junctions of walls, and adjacent to all openings and starting from the foundation and continuing upwards?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_junctions_of_walls_and_adjacent_to_all_openings_and_starting_from_the_foundation_and_continuing_upwards_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member timber or concrete?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "concrete",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_timber_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber_} = 'concrete'",
                                "required": "false"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of at least 12 mm diameter and covered with concrete or 1:4 mortar in cavities made around them during masonry construction?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the re bar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_re_bar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_kw4fc80",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'bmm'"
                    },
                    "label": "BMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "What is the number of stories you are building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "one",
                                    "label": "One"
                                },
                                {
                                    "name": "one_plus_attic",
                                    "label": "One plus attic"
                                },
                                {
                                    "name": "two_or_more",
                                    "label": "Two or more"
                                }
                            ],
                            "name": "What_is_the_number_of_stories_"
                        },
                        {
                            "bind": {
                                "relevant": "${What_is_the_number_of_stories_} = 'one_plus_attic'",
                                "required": "false"
                            },
                            "label": "Is the height of attic wall from floor level to eaves level more than 1m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_attic_wall_from_floor_level_to_eaves_level_more_than_1m__0"
                        },
                        {
                            "bind": {
                                "relevant": "${What_is_the_number_of_stories_} = 'one_plus_attic'",
                                "required": "true"
                            },
                            "label": "Is the height from the attic floor to the ridge level more than 1.8m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_from_the_attic_floor_to_the_ridge_level_more_than_1_8m__0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member placed at all corners and junctions continuous to the ring beam?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_and_junctions_continuous_to_the_ring_beam_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member placed adjacent to all doors and window openings continuous throughout its height?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_adjacent_to_all_doors_and_window_openings_continuous_throughout_its_height_"
                        },
                        {
                            "bind": {
                                "relevant": "${What_is_the_number_of_stories_} = 'one_plus_attic'",
                                "required": "false"
                            },
                            "label": "Is the vertical member timber or concrete?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "concrete",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_timber__001"
                        },
                        {
                            "bind": {
                                "relevant": "${What_is_the_number_of_stories_} = 'one' and ${Is_the_vertical_member_timber__001} = 'timber'",
                                "required": "false"
                            },
                            "label": "Is the vertical member at corner one member of size 75mm x 100mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_002"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_002} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives_"
                        },
                        {
                            "bind": {
                                "relevant": "${What_is_the_number_of_stories_} = 'one' and ${Is_the_vertical_member_timber__001} = 'timber'",
                                "required": "false"
                            },
                            "label": "Is the vertical member adjacent to all doors and window openings two members of size 75mm x 100mm each?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_adjacent_to_all_doors_and_window_openings_two_members_of_size_75mm_x_100mm_each_"
                        },
                        {
                            "bind": {
                                "relevant": "${What_is_the_number_of_stories_} = 'one' and ${Is_the_vertical_member_timber__001} = 'concrete'",
                                "required": "false"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of atleast 12mm dia and covered with concrete or 1:4 mortar in cavities made around them during masonry construction?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_001} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the concrete at least M15 grade or mix ratio 1:2;4, without surface cracks, no rebars exposed and with clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m15_grade_or_mix_ratio_1_2_4_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_001} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_cu04b04",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smm'"
                    },
                    "label": "SMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member timber or concrete?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "concrete",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_timber__002"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "What is the number of stories you are building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "one",
                                    "label": "One"
                                },
                                {
                                    "name": "one_plus_attic",
                                    "label": "One plus attic"
                                },
                                {
                                    "name": "two_or_more",
                                    "label": "Two or more"
                                }
                            ],
                            "name": "What_is_the_number_of_stories__001"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber__002} = 'concrete' and ${What_is_the_number_of_stories__001} = 'one_plus_attic'",
                                "required": "false"
                            },
                            "label": "Is the height of attic wall from floor level to eaves level more than 1m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_attic_wall_from_floor_level_to_eaves_level_more_than_1m__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber__002} = 'concrete' and ${What_is_the_number_of_stories__001} = 'one_plus_attic'",
                                "required": "true"
                            },
                            "label": "Is the height from the attic floor to the ridge level more than 1.8m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_from_the_attic_floor_to_the_ridge_level_more_than_1_8m__0_0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member placed at all corners and junctions continuous to the ring beam?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_and_junctions_continuous_to_the_ring_beam__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member placed adjacent to all doors and window openings continuous throughout its height?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_adjacent_to_all_doors_and_window_openings_continuous_throughout_its_height__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber__002} = 'timber' and ${What_is_the_number_of_stories__001} = 'one'",
                                "required": "false"
                            },
                            "label": "Is the vertical member at corner one member of size 75mm x 100mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_003"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_003} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives__0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber__002} = 'timber' and ${What_is_the_number_of_stories__001} = 'one'",
                                "required": "false"
                            },
                            "label": "Is the vertical member adjacent to all doors and window openings two members of size 75mm x 100mm each?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_adjacent_to_all_doors_and_window_openings_two_members_of_size_75mm_x_100mm_each__0"
                        },
                        {
                            "bind": {
                                "relevant": "${What_is_the_number_of_stories_} = 'one' and ${Is_the_vertical_member_timber__002} = 'timber' and ${Is_the_vertical_member_at_corn_003} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the timber used for structural purpose well-seasoned hard wood without knots and treated with coal tar or any other preservatives?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_timber_used_for_structural_purpose_well_seasoned_hard_wood_without_knots_and_treated_with_coal_tar_or_any_other_preservatives__0_0"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber__002} = 'concrete'",
                                "required": "false"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of atleast 12mm dia and covered with concrete or 1:4 mortar in cavities made around them during masonry construction?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_at_corner_intersections_and_adjacent_to_openings_bar_of_atleast_12mm_dia_and_covered_with_concrete_or_1_4_mortar_in_cavities_made_around_them_during_masonry_construction_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber__002} = 'concrete'",
                                "required": "true"
                            },
                            "label": "Is the concrete atleast M15 grade or mix ratio 1:2;4, without surface cracks, no rebars exposed and with clean and smooth surface?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_atleast_m15_grade_or_mix_ratio_1_2_4_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_surface_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber__002} = 'concrete'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60__0"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_ao65k14",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smc'"
                    },
                    "label": "SMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the height of wall from floor level to floor level more than 3m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_wall_from_floor_level_to_floor_level_more_than_3m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the height of attic wall from floor level to eaves level more than 1m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_attic_wall_from_floor_level_to_eaves_level_more_than_1m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the height from the attic floor to the ridge level more than 1.8m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_from_the_attic_floor_to_the_ridge_level_more_than_1_8m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the vertical member placed at all corners, junctions of walls, and adjacent to all openings and starting from the foundation and continuing upwards?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_vertical_member_placed_at_all_corners_junctions_of_walls_and_adjacent_to_all_openings_and_starting_from_the_foundation_and_continuing_upwards_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the vertical member timber or concrete?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "timber",
                                    "label": "Timber"
                                },
                                {
                                    "name": "concrete",
                                    "label": "Concrete"
                                }
                            ],
                            "name": "Is_the_vertical_member_timber__003"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_timber__003} = 'concrete'",
                                "required": "false"
                            },
                            "label": "Is the vertical member at corner, intersections and adjacent to openings bar of atleast 12mm dia and covered with concrete or 1:4 mortar in cavities made around them during masonry construction?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_vertical_member_at_corn_004"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_004} = 'yes'",
                                "required": "false"
                            },
                            "label": "Is the concrete at least M20 grade or mix ratio 1:1.5:3, without surface cracks, no rebars exposed and with clean and smooth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_concrete_at_least_m20_grade_or_mix_ratio_1_1_5_3_without_surface_cracks_no_rebars_exposed_and_with_clean_and_smooth_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_vertical_member_at_corn_004} = 'yes'",
                                "required": "true"
                            },
                            "label": "Is the rebar high strength deformed bars with Fy=415Mpa/500Mpa with overlap length of 60Ǿ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_rebar_high_strength_deformed_bars_with_fy_415mpa_500mpa_with_overlap_length_of_60_"
                        }
                    ]
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "photo",
                    "name": "add_photo_",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0_0",
                    "label": "Add photo."
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "8097"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20375,
        "name": "Second Tranche- Walls",
        "json": {
            "name": "azuBLfrQ6w4moNtXqpAR6Y_GxcIYSu",
            "name": "Second Tranche- Walls",
            "sms_keyword": "azuBLfrQ6w4moNtXqpAR6Y",
            "default_language": "default",
            "version": "4709",
            "id_string": "azuBLfrQ6w4moNtXqpAR6Y",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What type of building is it?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM"
                        },
                        {
                            "name": "smc",
                            "label": "SMC"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC"
                        },
                        {
                            "name": "rcc_a_b",
                            "label": "RCC A&B"
                        }
                    ],
                    "name": "What_type_of_building_is_it"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_oz3my92",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smm'"
                    },
                    "label": "SMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the clear span of wall less than 12 times the thickness of wall or less than or equal to 4.5m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_clear_span_of_wall_less"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_clear_span_of_wall_less} = 'no'",
                                "required": "false"
                            },
                            "label": "Are there buttresses provided in the wall at less than 3m apart with minimum base width equal to one sixth of the wall height and top with equal to thickness of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_there_buttresses_provided_in_the_wall_at_less_than_3m_apart_with_minimum_base_width_equal_to_one_sixth_of_the_wall_height_and_top_with_equal_to_thickness_of_the_wall_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the wall in plumb and of the thickness at least 350 mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_wall_in_plumb_and_of_the_thickness_at_least_350_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the through stones placed 1.2 m apart horizontally and 600 mm vertically?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_through_stones_placed_1_2_m_apart_horizontally_and_600_mm_vertically_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are corner stones placed 600 mm apart vertically at all corners and intersections?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_corner_stones_placed_600_mm_apart_vertically_at_all_corners_and_intersections_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the mortar joints less than 20mm and more than 10mm thick?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_mortar_joints_less_than_20mm_and_more_than_10mm_thick_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Gable wall of light materials like wood, CGI sheet, etc?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_gable_wall_of_light_materials_like_wood_cgi_sheet_etc_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the stones rounded, not-dressed, easily breakable soft stone and boulder stones in its natural shape?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_stones_rounded_not_dressed_easily_breakable_soft_stone_and_boulder_stones_in_its_natural_shape_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the stones smaller than 50mm in thickness and 150 mm in length or breadth?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_stones_smaller_than_50mm_in_thickness_and_150_mm_in_length_or_breadth_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Mud mortar free from organic materials, pebbles, hard materials?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mud_mortar_free_from_organic_materials_pebbles_hard_materials_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_xk2bo56",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'bmm'"
                    },
                    "label": "BMM",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the clear span of wall less than 12 times the thickness of wall or less than or equal to 4.5m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_clear_span_of_wall_less_than_12_times_the_thickness_of_wall_or_less_than_or_equal_to_4_5m_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are there buttresses provided in the wall at less than 3m apart with minimum base width equal to one sixth of the wall height and top with equal to thickness of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_there_buttresses_provided_in_the_wall_at_less_than_3m_apart_with_minimum_base_width_equal_to_one_sixth_of_the_wall_height_and_top_with_equal_to_thickness_of_the_wall__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the wall in plumb and of the thickness at least 350mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_wall_in_plumb_and_of_the_thickness_at_least_350mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the through stones placed 1.2 m apart horizontally and 600mm vertically?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_through_stones_placed_1_2_m_apart_horizontally_and_600mm_vertically_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are corner stones placed 600mm apart vertically at all corners and intersections?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_corner_stones_placed_600mm_apart_vertically_at_all_corners_and_intersections_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the mortar joints less than 20mm and more than 10mm thick?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_mortar_joints_less_than_20mm_and_more_than_10mm_thick__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Gable wall of light materials like wood, CGI sheet, etc?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_gable_wall_of_light_materials_like_wood_cgi_sheet_etc__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Has Overburnt, underburnt and deformed bricks with minimum crushing strength of 3.5 MPa used?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "has_overburnt_underburnt_and_deformed_bricks_with_minimum_crushing_strength_of_3_5_mpa_used_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Mud mortar free from organic materials, pebbles, hard materials?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mud_mortar_free_from_organic_materials_pebbles_hard_materials__0"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_et15g98",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'smc'"
                    },
                    "label": "SMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the clear span of wall equal to or less than 4.5m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "Is_the_clear_span_of_wall_equa"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_clear_span_of_wall_equa} = 'no'",
                                "required": "true"
                            },
                            "label": "Are there buttresses provided in the wall at less than 3m apart with minimum base width equal to one sixth of the wall height and top with equal to thickness of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_there_buttresses_provided_in_the_wall_at_less_than_3m_apart_with_minimum_base_width_equal_to_one_sixth_of_the_wall_height_and_top_with_equal_to_thickness_of_the_wall__0_0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the wall in plumb and of thickness 350mm for one storey or 450mm for two storey building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_wall_in_plumb_and_of_thickness_350mm_for_one_storey_or_450mm_for_two_storey_building_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the mortar joints 10mm to 20 mm thick?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_mortar_joints_10mm_to_20_mm_thick_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Gable wall of light materials like wood, CGI sheet, etc?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_gable_wall_of_light_materials_like_wood_cgi_sheet_etc__0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the stones rounded, not-dressed, easily breakable soft stone and boulder stones in its natural shape?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_stones_rounded_not_dressed_easily_breakable_soft_stone_and_boulder_stones_in_its_natural_shape__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the mortar ratio atleast 1:6(1 parts cement and 6 sand)?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_atleast_1_6_1_parts_cement_and_6_sand_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the through stones placed 1.2 m apart horizontally and 600mm vertically?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_through_stones_placed_1_2_m_apart_horizontally_and_600mm_vertically__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are corner stones placed 600mm apart vertically at all corners and intersections?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_corner_stones_placed_600mm_apart_vertically_at_all_corners_and_intersections__0"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_cx7hj85",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'bmc'"
                    },
                    "label": "BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the clear span of wall equal to or less than 4.5m?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_clear_span_of_wall_equal_to_or_less_than_4_5m_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the wall in plumb and of thickness 230mm for one storey or 350mm for more than one storey building?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_wall_in_plumb_and_of_thickness_230mm_for_one_storey_or_350mm_for_more_than_one_storey_building_"
                        },
                        {
                            "bind": {
                                "relevant": "${Is_the_clear_span_of_wall_equa} = 'no'",
                                "required": "false"
                            },
                            "label": "Are there buttresses provided in the wall at less than 3m apart with minimum base width equal to one sixth of the wall height and top with equal to thickness of the wall?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_there_buttresses_provided_in_the_wall_at_less_than_3m_apart_with_minimum_base_width_equal_to_one_sixth_of_the_wall_height_and_top_with_equal_to_thickness_of_the_wall__0_0_0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the mortar joints 10mm to 20 mm thick and joints vertically staggered?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_mortar_joints_10mm_to_20_mm_thick_and_joints_vertically_staggered_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Has Overburnt, underburnt, deformed bricks used?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "has_overburnt_underburnt_deformed_bricks_used_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the mortar ratio at least 1:6(1 parts cement and 6 sand)?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_at_least_1_6_1_parts_cement_and_6_sand_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_an6gn49",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'confined_masonry'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Are the hollow blocks used of regular shape/size and does not shatter when dropped from shoulder height on a hard ground?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_hollow_blocks_used_of_regular_shape_size_and_does_not_shatter_when_dropped_from_shoulder_height_on_a_hard_ground_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the masonry units laid staggered in order to avoid continuous vertical joints?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_masonry_units_laid_staggered_in_order_to_avoid_continuous_vertical_joints_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are toothing provided at the wall-column interface?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_toothing_provided_at_the_wall_column_interface_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the mortar ratio 1:5 (cement: sand) or richer and the mortar thickness between 20mm to 10mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_ratio_1_5_cement_sand_or_richer_and_the_mortar_thickness_between_20mm_to_10mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the wall equal at least 150mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_wall_equal_at_least_150mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is there only one opening per wall span?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_there_only_one_opening_per_wall_span_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the area of opening less than or equal to 10% of the area of the confined wall panel (area of wall panel calculated including the tie columns but not including the tie beams)?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_area_of_opening_less_than_or_equal_to_10_of_the_area_of_the_confined_wall_panel_area_of_wall_panel_calculated_including_the_tie_columns_but_not_including_the_tie_beams_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_zn6df99",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the non structural wall constructed equally from two sides?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_non_structural_wall_constructed_equally_from_two_sides_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the wall straight and in Plumb?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_wall_straight_and_in_plumb_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the Mortar joints staggered vertically?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_mortar_joints_staggered_vertically_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width at least 110mm or 230mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_at_least_110mm_or_230mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the Mortar joints 10 mm to 20 mm?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_mortar_joints_10_mm_to_20_mm_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the sill band has minimum depth 75 mm and 2 numbers of 8mm dia rebars connected to pillar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "does_the_sill_band_has_minimum_depth_75_mm_and_2_numbers_of_8mm_dia_rebars_connected_to_pillar_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the lintel band has minimum depth 75 mm and 2 numbers of 8mm dia rebars connected to pillar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "does_the_lintel_band_has_minimum_depth_75_mm_and_2_numbers_of_8mm_dia_rebars_connected_to_pillar_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_fu4pn51",
                    "bind": {
                        "relevant": "${What_type_of_building_is_it} = 'rcc_a_b'"
                    },
                    "label": "RCC A&B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the position of walls as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_position_of_walls_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the wall straight?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_wall_straight_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Are the mortar joints staggered vertically?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "are_the_mortar_joints_staggered_vertically__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the width of the wall as per approved design?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_width_of_the_wall_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Is the joints 10 mm to 20 mm thick?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_joints_10_mm_to_20_mm_thick_"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the sill band has minimum depth 75 mm and 2 numbers of 8mm dia rebars connected to pillar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "does_the_sill_band_has_minimum_depth_75_mm_and_2_numbers_of_8mm_dia_rebars_connected_to_pillar__0"
                        },
                        {
                            "bind": {
                                "required": "true"
                            },
                            "label": "Does the lintel band has minimum depth 75 mm and 2 numbers of 8mm dia rebars connected to pillar?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "does_the_lintel_band_has_minimum_depth_75_mm_and_2_numbers_of_8mm_dia_rebars_connected_to_pillar__0"
                        }
                    ]
                },
                {
                    "bind": {
                        "required": "true"
                    },
                    "type": "photo",
                    "name": "add_photo_",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0",
                    "label": "Add photo."
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "photo",
                    "name": "add_photo__0_0",
                    "label": "Add photo."
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4709"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    },
    {
        "id": 20374,
        "name": "Shape and Size",
        "json": {
            "name": "amBo4gEipk4cMRXDPW4ZTR_7HQmrxs",
            "name": "Shape and Size",
            "sms_keyword": "amBo4gEipk4cMRXDPW4ZTR",
            "default_language": "default",
            "version": "4826",
            "id_string": "amBo4gEipk4cMRXDPW4ZTR",
            "type": "survey",
            "children": [
                {
                    "bind": {
                        "required": "false"
                    },
                    "type": "geopoint",
                    "name": "location",
                    "label": "Location"
                },
                {
                    "bind": {
                        "required": "false"
                    },
                    "label": "What is the type of building ?",
                    "type": "select one",
                    "children": [
                        {
                            "name": "smm",
                            "label": "SMM (Stone Mud Mortar)"
                        },
                        {
                            "name": "smc",
                            "label": "SMC (Stone Masonry Cement)"
                        },
                        {
                            "name": "bmm",
                            "label": "BMM (Brick Mud Masonry)"
                        },
                        {
                            "name": "bmc",
                            "label": "BMC (Brick Masonry Cement)"
                        },
                        {
                            "name": "rcc",
                            "label": "RCC (Reinforced Concrete Cement)"
                        },
                        {
                            "name": "rcc_a_and_rcc_b",
                            "label": "RCC A &B (Reinforced Concrete Cement)"
                        },
                        {
                            "name": "confined_masonry",
                            "label": "Confined Masonry"
                        }
                    ],
                    "name": "What_is_the_type_of_building_"
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_mf24f05",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} != 'rcc' and ${What_is_the_type_of_building_} != 'rcc_a_and_rcc_b' and ${What_is_the_type_of_building_} != 'confined_masonry'"
                    },
                    "label": "SMM/SMC/BMM/BMC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the clear span of wall more than 4.5 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_clear_span_of_wall_more_than_4_5_m_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the building simple and regular shaped?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_building_simple_and_regular_shaped_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the length of the building more than 3 times of its width ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_of_the_building_more_than_3_times_of_its_width_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the size of the room more than 13.5 sq.m.?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_size_of_the_room_more_than_13_5_sq_m_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_hm7wx57",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc'"
                    },
                    "label": "RCC",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the house limited up to 3 floor ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_house_limited_up_to_3_floor_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the number of bay two to six ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_number_of_bay_two_to_six_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the area less than 1000 sq. ft and area in between 4 pillars 13.5 sq m only ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_area_less_than_1000_sq_ft_and_area_in_between_4_pillars_13_5_sq_m_only_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the Total height of building less than 11m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_total_height_of_building_less_than_11m_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the height of floor from 2.75 m to 3.35 m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_height_of_floor_from_2_75_m_to_3_35_m_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the shape square or rectangular ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_shape_square_or_rectangular_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the ratio of length less than 3 times the breadth ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_ratio_of_length_less_than_3_times_the_breadth_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_wc4ft28",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc_a_and_rcc_b'"
                    },
                    "label": "Pictures of each page of Approved design adopted",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_1",
                            "label": "Photo 1"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_2",
                            "label": "Photo 2"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_3",
                            "label": "Photo 3"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_4",
                            "label": "Photo 4"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "type": "photo",
                            "name": "photo_5",
                            "label": "Photo 5"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_fv0sw35",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'rcc_a_and_rcc_b'"
                    },
                    "label": "RCC A and RCC B",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the number of bays as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_number_of_bays_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the building area as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_building_area_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the Total height of building less than 11m ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_total_height_of_building_less_than_11m__0"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the length of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_of_the_building_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the breadth of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_breadth_of_the_building_as_per_approved_design_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the storey height of the building as per approved design ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_storey_height_of_the_building_as_per_approved_design_"
                        }
                    ]
                },
                {
                    "control": {
                        "appearance": "field-list"
                    },
                    "name": "group_fp83b97",
                    "bind": {
                        "relevant": "${What_is_the_type_of_building_} = 'confined_masonry'"
                    },
                    "label": "Confined Masonry",
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the maximum span of the wall more than 3.5 meters ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_maximum_span_of_the_wall_more_than_3_5_meters_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the house either a square or a rectangle ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_house_either_a_square_or_a_rectangle_"
                        },
                        {
                            "bind": {
                                "required": "false"
                            },
                            "label": "Is the length to breadth ratio of the structure more than 3 ?",
                            "type": "select one",
                            "children": [
                                {
                                    "name": "yes",
                                    "label": "Yes"
                                },
                                {
                                    "name": "no",
                                    "label": "No"
                                }
                            ],
                            "name": "is_the_length_to_breadth_ratio_of_the_structure_more_than_3_"
                        }
                    ]
                },
                {
                    "type": "start",
                    "name": "start"
                },
                {
                    "type": "end",
                    "name": "end"
                },
                {
                    "bind": {
                        "calculate": "4826"
                    },
                    "type": "calculate",
                    "name": "__version__"
                },
                {
                    "control": {
                        "bodyless": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "bind": {
                                "readonly": "true()",
                                "calculate": "concat('uuid:', uuid())"
                            },
                            "type": "calculate",
                            "name": "instanceID"
                        }
                    ],
                    "name": "meta"
                }
            ]
        }
    }
]