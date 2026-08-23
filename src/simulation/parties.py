from typing import Dict

from settings import DEFAULT_PARTY_PREFERENCES, DEFAULT_CANDIDATES
from simulation.preferencesweights import Preferences, Weights
from simulation.mathutils import clamp
from simulation import scoring


def getPartyAffinity(target, party) -> float:
    """How closely `target` (a Voter or Region) matches `party`'s platform.

    Returns a value in [0, 1] where 1.0 is a perfect ideological match.
    Kept as a thin wrapper around scoring.calculate_party_affinity so
    existing callers (Region, Voter) don't need to import scoring directly.
    """
    return scoring.calculate_party_affinity(target, party)


class CandidateTraits:
    TRAIT_NAMES = [
        "charisma",
        "debate_skill",
        "media_skill",
        "fundraising",
        "organization",
        "discipline",
        "persuasion",
        "leadership",
        "authenticity",
        "experience",
        "risk_tolerance",
        "coalition_building",
    ]

    def __init__(self, charisma, debate_skill, media_skill, fundraising, organization,
                 discipline, persuasion, leadership, authenticity, experience,
                 risk_tolerance, coalition_building):
        self.charisma = charisma
        self.debate_skill = debate_skill
        self.media_skill = media_skill
        self.fundraising = fundraising
        self.organization = organization
        self.discipline = discipline
        self.persuasion = persuasion
        self.leadership = leadership
        self.authenticity = authenticity
        self.experience = experience
        self.risk_tolerance = risk_tolerance
        self.coalition_building = coalition_building

    def get(self, trait_name: str, default: float = 0.5) -> float:
        return getattr(self, trait_name, default)

    def __repr__(self):
        return (
            f"CandidateTraits(charisma={self.charisma}, debate_skill={self.debate_skill}, "
            f"media_skill={self.media_skill}, fundraising={self.fundraising}, "
            f"organization={self.organization}, discipline={self.discipline}, "
            f"persuasion={self.persuasion}, leadership={self.leadership}, "
            f"authenticity={self.authenticity}, experience={self.experience}, "
            f"risk_tolerance={self.risk_tolerance}, coalition_building={self.coalition_building})"
        )


class Candidate:
    def __init__(self, party):
        data = DEFAULT_CANDIDATES[party]
        self.name = data["name"]
        self.party = party

        prefs = data["preferences"]
        self.preferences = Preferences(
            prefs["economy"], prefs["taxes"], prefs["healthcare"], prefs["education"],
            prefs["immigration"], prefs["environment"], prefs["crime"],
            prefs["government_size"], prefs["foreign_policy"], prefs["infrastructure"],
        )

        weights = data["weights"]
        self.weights = Weights(
            weights["economy"], weights["taxes"], weights["healthcare"], weights["education"],
            weights["immigration"], weights["environment"], weights["crime"],
            weights["government_size"], weights["foreign_policy"], weights["infrastructure"],
        )

        traits = data["traits"]
        self.traits = CandidateTraits(
            traits["charisma"], traits["debate_skill"], traits["media_skill"],
            traits["fundraising"], traits["organization"], traits["discipline"],
            traits["persuasion"], traits["leadership"], traits["authenticity"],
            traits["experience"], traits["risk_tolerance"], traits["coalition_building"],
        )

        self.money = 0
        self.regional_popularity: Dict[str, float] = {}

    def calculate_appeal_score(self) -> float:
        return scoring.calculate_candidate_appeal(self)

    def calculate_voter_affinity(self, voter) -> float:
        return scoring.calculate_candidate_affinity(voter, self)

    def calculate_regional_popularity(self, region) -> float:
        if not region.voter_list:
            return 0.0

        total_affinity = sum(self.calculate_voter_affinity(voter) for voter in region.voter_list)
        regional_popularity = total_affinity / len(region.voter_list)

        self.regional_popularity[region.name] = regional_popularity
        return regional_popularity

    def get_regional_popularity(self, region_name: str) -> float:
        return self.regional_popularity.get(region_name, 0.0)


class Party:
    MIN_POPULARITY = 0.0
    MAX_POPULARITY = 1.0

    def __init__(self, name):
        self.name = name
        self.ideology = "moderate"
        data = DEFAULT_PARTY_PREFERENCES[name]
        self.popularity = clamp(float(data["popularity"]), self.MIN_POPULARITY, self.MAX_POPULARITY)

        prefs = data["preferences"]
        self.preferences = Preferences(
            prefs["economy"], prefs["taxes"], prefs["healthcare"], prefs["education"],
            prefs["immigration"], prefs["environment"], prefs["crime"],
            prefs["government_size"], prefs["foreign_policy"], prefs["infrastructure"],
        )

        weights = data["weights"]
        self.weights = Weights(
            weights["economy"], weights["taxes"], weights["healthcare"], weights["education"],
            weights["immigration"], weights["environment"], weights["crime"],
            weights["government_size"], weights["foreign_policy"], weights["infrastructure"],
        )

        self.candidate = Candidate(name)
        self.candidate.party = self

    def adjust_popularity(self, change: float) -> float:
        self.popularity = clamp(self.popularity + change, self.MIN_POPULARITY, self.MAX_POPULARITY)
        return self.popularity

    def __repr__(self):
        return f"Party(name={self.name}, ideology={self.ideology})"
