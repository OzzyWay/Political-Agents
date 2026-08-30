import json
import random
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "app_settings.json"
LOG_PATH = ROOT / "logs" / "political_agents.log"

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

REGION_VOTERS = 10000

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

DEFAULT_SETTINGS = {
    "regions": list(DEFAULT_REGIONS),
    "voters_per_region": int(REGION_VOTERS),
    "campaign_weeks": 8,
    "poll_sample_size": 500,
    "use_ai": True,
    "ai_model": "llama2",
    "log_level": "INFO",
    "party_names": list(DEFAULT_PARTY_PREFERENCES.keys()),
    "candidate_names": [candidate["name"] for candidate in DEFAULT_CANDIDATES.values()],
  "starting_budget_per_candidate": 500000,
  "diminishing_return_decay": 0.35,
  "fundraising_params": {"base": 22000, "intensity_scale": 27000, "bonus": 15000},
  "base_action_costs": {
    "MEDIA_CAMPAIGN": 50000,
    "ISSUE_AD": 35000,
    "PHONE_BANK": 12000,
    "RALLY": 10000,
    "DOOR_TO_DOOR": 5000,
    "POLICY_SPEECH": 15000,
    "TOWN_HALL": 8000,
    "FUNDRAISING": 2000,
    "VOTER_REGISTRATION": 3000,
    "OPPOSITION_RESEARCH": 20000,
    "SOCIAL_MEDIA": 8000,
    "ENDORSEMENT": 30000,
    "SURROGATE_VISIT": 6000,
    "DEBATE_PREP": 18000,
    "MICRO_TARGETING": 15000
  },
  "action_effectiveness": {
    "MEDIA_CAMPAIGN": 0.06,
    "ISSUE_AD": 0.07,
    "PHONE_BANK": 0.08,
    "RALLY": 0.08,
    "DOOR_TO_DOOR": 0.09,
    "POLICY_SPEECH": 0.05,
    "TOWN_HALL": 0.06,
    "FUNDRAISING": 0.05,
    "VOTER_REGISTRATION": 0.0,
    "OPPOSITION_RESEARCH": -0.05,
    "SOCIAL_MEDIA": 0.04,
    "ENDORSEMENT": 0.05,
    "SURROGATE_VISIT": 0.05,
    "DEBATE_PREP": 0.04,
    "MICRO_TARGETING": 0.07
  },
  "action_reach": {
    "MEDIA_CAMPAIGN": 3.0,
    "ISSUE_AD": 2.8,
    "PHONE_BANK": 1.5,
    "RALLY": 1.4,
    "DOOR_TO_DOOR": 1.1,
    "POLICY_SPEECH": 2.0,
    "TOWN_HALL": 1.2,
    "FUNDRAISING": 0.0,
    "VOTER_REGISTRATION": 1.7,
    "OPPOSITION_RESEARCH": 1.8,
    "SOCIAL_MEDIA": 2.5,
    "ENDORSEMENT": 1.6,
    "SURROGATE_VISIT": 1.0,
    "DEBATE_PREP": 1.4,
    "MICRO_TARGETING": 2.1
  },
  "action_efficiency": {
    "MEDIA_CAMPAIGN": 2.8,
    "ISSUE_AD": 2.6,
    "PHONE_BANK": 2.0,
    "RALLY": 1.1,
    "DOOR_TO_DOOR": 0.7,
    "POLICY_SPEECH": 2.1,
    "TOWN_HALL": 1.3,
    "FUNDRAISING": 1.0,
    "VOTER_REGISTRATION": 1.7,
    "OPPOSITION_RESEARCH": 3.3,
    "SOCIAL_MEDIA": 1.6,
    "ENDORSEMENT": 3.8,
    "SURROGATE_VISIT": 1.5,
    "DEBATE_PREP": 1.8,
    "MICRO_TARGETING": 2.3
  },
  "action_popularity_impact": {
    "MEDIA_CAMPAIGN": 0.10,
    "ISSUE_AD": 0.12,
    "PHONE_BANK": 0.08,
    "RALLY": 0.09,
    "DOOR_TO_DOOR": 0.11,
    "POLICY_SPEECH": 0.07,
    "TOWN_HALL": 0.08,
    "FUNDRAISING": 0.04,
    "VOTER_REGISTRATION": 0.06,
    "OPPOSITION_RESEARCH": -0.08,
    "SOCIAL_MEDIA": 0.09,
    "ENDORSEMENT": 0.10,
    "SURROGATE_VISIT": 0.07,
    "DEBATE_PREP": 0.06,
    "MICRO_TARGETING": 0.12
  },
}


def ensure_runtime_files():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_SETTINGS, indent=2), encoding="utf-8")
    if not LOG_PATH.exists():
        LOG_PATH.touch()


def load_settings():
    ensure_runtime_files()
    try:
        raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        raw = {}

    merged = DEFAULT_SETTINGS.copy()
    for key, value in raw.items():
        merged[key] = value
    if "poll_sample_size" not in merged and "polls_per_region" in merged:
        merged["poll_sample_size"] = merged["polls_per_region"]
    merged["regions"] = [str(region).strip() for region in merged.get("regions", DEFAULT_REGIONS) if str(region).strip()]
    if not merged["regions"]:
        merged["regions"] = DEFAULT_REGIONS.copy()
    return merged


def save_settings(settings):
    ensure_runtime_files()
    CONFIG_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")


def set_global_seed(seed: int):
    """Seed every RNG the simulation touches (Section 20).

    The simulation currently draws randomness from Python's `random` module
    and from numpy's global RNG state (np.random.*) throughout voters.py,
    campaigneffects.py, voting.py, etc. Rather than thread an injected RNG
    object through every constructor -- a much larger architectural change
    -- this seeds both global RNGs so `Simulation(seed=42)` run twice
    produces identical output, and different seeds produce different
    outcomes.
    """
    random.seed(seed)
    np.random.seed(seed)