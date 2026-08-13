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