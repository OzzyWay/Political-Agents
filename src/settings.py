EDUCATION_LEVELS = [
    "No High School",
    "Some High School, No Diploma",
    "High School",
    "Some College, No Degree",
    "Associate's Degree",
    "Bachelor's Degree",
    "Master's Degree",
    "Doctoral/Professional Degree",
]

EDUCATION_WEIGHTS = [0.032, 0.061, 0.289, 0.165, 0.099, 0.222, 0.099, 0.033]

EDUCATION_SCORE = [0.1, 0.2, 0.3, 0.4, 0.5 , 0.6, 0.7 ,0.8]

DEFAULT_REGIONS = ["North", "South", "East", "West"]

REGION_VOTERS =  10000

DEFAULT_REGIONAL_LEAN ={
        "North": {
            "preferences": {
                "economy": 0.10,
                "taxes": 0.05,
                "healthcare": 0.30,
                "education": 0.25,
                "immigration": 0.05,
                "environment": 0.25,
                "crime": 0.05,
                "government_size": 0.15,
                "foreign_policy": 0.10,
                "infrastructure": 0.20
            },
            "weights": {
                "economy": 0.90,
                "taxes": 0.65,
                "healthcare": 0.85,
                "education": 0.75,
                "immigration": 0.65,
                "environment": 0.70,
                "crime": 0.70,
                "government_size": 0.70,
                "foreign_policy": 0.55,
                "infrastructure": 0.75
            },
            "variation": 0.25
    },

    "West": {
      "preferences": {
        "economy": 0.05,
        "taxes": -0.15,
        "healthcare": 0.15,
        "education": 0.20,
        "immigration": -0.05,
        "environment": 0.45,
        "crime": -0.05,
        "government_size": -0.20,
        "foreign_policy": 0.05,
        "infrastructure": 0.15
      },
      "weights": {
        "economy": 0.90,
        "taxes": 0.70,
        "healthcare": 0.75,
        "education": 0.70,
        "immigration": 0.65,
        "environment": 0.85,
        "crime": 0.65,
        "government_size": 0.75,
        "foreign_policy": 0.55,
        "infrastructure": 0.70
      },
      "variation": 0.20
    
    },

    "South": {
      "preferences": {
        "economy": -0.20,
        "taxes": -0.35,
        "healthcare": -0.05,
        "education": 0.05,
        "immigration": -0.30,
        "environment": -0.15,
        "crime": -0.25,
        "government_size": -0.35,
        "foreign_policy": -0.05,
        "infrastructure": 0.10
      },
      "weights": {
        "economy": 0.95,
        "taxes": 0.80,
        "healthcare": 0.70,
        "education": 0.65,
        "immigration": 0.85,
        "environment": 0.50,
        "crime": 0.85,
        "government_size": 0.85,
        "foreign_policy": 0.60,
        "infrastructure": 0.70
      },
      "variation": 0.15
    },

    "East": {
      "preferences": {
        "economy": 0.15,
        "taxes": 0.10,
        "healthcare": 0.35,
        "education": 0.30,
        "immigration": 0.10,
        "environment": 0.30,
        "crime": 0.05,
        "government_size": 0.15,
        "foreign_policy": 0.15,
        "infrastructure": 0.30
      },
      "weights": {
        "economy": 0.90,
        "taxes": 0.65,
        "healthcare": 0.90,
        "education": 0.80,
        "immigration": 0.65,
        "environment": 0.75,
        "crime": 0.70,
        "government_size": 0.70,
        "foreign_policy": 0.65,
        "infrastructure": 0.80
      },
      "variation": 0.25
    }
  }

DEFAULT_PARTIES = [
    {"name": "Democratic Party", "ideology": "Liberal"},
    {"name": "Republican Party", "ideology": "Conservative"},
    {"name": "Libertarian Party", "ideology": "Libertarian"},
    ]

DEFAULT_PARTY_PREFERENCES = {
    "Democratic Party": {
      "preferences": {
        "economy": 0.35,
        "taxes": 0.30,
        "healthcare": 0.60,
        "education": 0.45,
        "immigration": 0.25,
        "environment": 0.70,
        "crime": 0.15,
        "government_size": 0.35,
        "foreign_policy": 0.20,
        "infrastructure": 0.55
      },
      "weights": {
        "economy": 0.90,
        "taxes": 0.75,
        "healthcare": 0.90,
        "education": 0.85,
        "immigration": 0.70,
        "environment": 0.85,
        "crime": 0.70,
        "government_size": 0.75,
        "foreign_policy": 0.60,
        "infrastructure": 0.80
      },
      "popularity": 0.8
    },

    "Republican Party": {
      "preferences": {
        "economy": -0.25,
        "taxes": -0.40,
        "healthcare": -0.20,
        "education": 0.05,
        "immigration": -0.55,
        "environment": -0.50,
        "crime": -0.45,
        "government_size": -0.35,
        "foreign_policy": -0.15,
        "infrastructure": 0.10
      },
      "weights": {
        "economy": 0.95,
        "taxes": 0.85,
        "healthcare": 0.75,
        "education": 0.75,
        "immigration": 0.90,
        "environment": 0.65,
        "crime": 0.90,
        "government_size": 0.85,
        "foreign_policy": 0.75,
        "infrastructure": 0.75
      },
      "popularity": 0.8
    },

    "Libertarian Party": {
      "preferences": {
        "economy": -0.10,
        "taxes": -0.65,
        "healthcare": -0.45,
        "education": -0.15,
        "immigration": 0.20,
        "environment": 0.10,
        "crime": -0.20,
        "government_size": -0.75,
        "foreign_policy": -0.55,
        "infrastructure": -0.25
      },
      "weights": {
        "economy": 0.90,
        "taxes": 0.95,
        "healthcare": 0.70,
        "education": 0.60,
        "immigration": 0.80,
        "environment": 0.60,
        "crime": 0.75,
        "government_size": 0.95,
        "foreign_policy": 0.80,
        "infrastructure": 0.55
      },
      "popularity": 0.1
    }
}

DEFAULT_CANDIDATES = {
    "Democratic Party": {
        "name": "Maya Rodriguez",

        "preferences": {
            "economy": 0.30,
            "taxes": 0.35,
            "healthcare": 0.75,
            "education": 0.70,
            "immigration": 0.35,
            "environment": 0.80,
            "crime": 0.10,
            "government_size": 0.45,
            "foreign_policy": 0.25,
            "infrastructure": 0.70
        },

        "weights": {
            "economy": 0.80,
            "taxes": 0.65,
            "healthcare": 0.95,
            "education": 0.90,
            "immigration": 0.65,
            "environment": 0.90,
            "crime": 0.55,
            "government_size": 0.70,
            "foreign_policy": 0.60,
            "infrastructure": 0.85
        },

        "traits": {
            "charisma": 0.86,
            "debate_skill": 0.78,
            "media_skill": 0.88,
            "fundraising": 0.82,
            "organization": 0.70,
            "discipline": 0.76,
            "persuasion": 0.84,
            "leadership": 0.79,
            "authenticity": 0.81,
            "experience": 0.74,
            "risk_tolerance": 0.62,
            "coalition_building": 0.78
        }
    },
    "Republican Party": {
        "name": "Daniel Carter",

        "preferences": {
            "economy": -0.40,
            "taxes": -0.55,
            "healthcare": -0.25,
            "education": -0.05,
            "immigration": -0.65,
            "environment": -0.35,
            "crime": -0.60,
            "government_size": -0.50,
            "foreign_policy": -0.20,
            "infrastructure": 0.05
        },

        "weights": {
            "economy": 0.95,
            "taxes": 0.85,
            "healthcare": 0.65,
            "education": 0.70,
            "immigration": 0.95,
            "environment": 0.55,
            "crime": 0.95,
            "government_size": 0.90,
            "foreign_policy": 0.70,
            "infrastructure": 0.75
        },

        "traits": {
            "charisma": 0.74,
            "debate_skill": 0.88,
            "media_skill": 0.70,
            "fundraising": 0.85,
            "organization": 0.91,
            "discipline": 0.82,
            "persuasion": 0.72,
            "leadership": 0.86,
            "authenticity": 0.76,
            "experience": 0.81,
            "risk_tolerance": 0.58,
            "coalition_building": 0.67
        }
    },
    "Libertarian Party": {
        "name": "Ethan Brooks",

        "preferences": {
            "economy": -0.15,
            "taxes": -0.75,
            "healthcare": -0.40,
            "education": -0.20,
            "immigration": 0.35,
            "environment": 0.05,
            "crime": -0.10,
            "government_size": -0.85,
            "foreign_policy": -0.70,
            "infrastructure": -0.25
        },

        "weights": {
            "economy": 0.90,
            "taxes": 0.95,
            "healthcare": 0.70,
            "education": 0.55,
            "immigration": 0.80,
            "environment": 0.50,
            "crime": 0.65,
            "government_size": 0.98,
            "foreign_policy": 0.90,
            "infrastructure": 0.50
        },

        "traits": {
            "charisma": 0.68,
            "debate_skill": 0.92,
            "media_skill": 0.62,
            "fundraising": 0.48,
            "organization": 0.57,
            "discipline": 0.64,
            "persuasion": 0.78,
            "leadership": 0.63,
            "authenticity": 0.91,
            "experience": 0.42,
            "risk_tolerance": 0.88,
            "coalition_building": 0.45
        }
        }
}