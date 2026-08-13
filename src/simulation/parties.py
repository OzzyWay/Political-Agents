from settings import DEFAULT_PARTY_PREFERENCES, DEFAULT_PARTIES, DEFAULT_CANDIDATES
from simulation.preferencesweights import Preferences, Weights


def getPartyAffinity(target, party):
    score = 0
    score += abs(abs(target.preferences.economy)-abs(party.preferences.economy))
    score += abs(abs(target.preferences.tax)-abs(party.preferences.tax))
    score += abs(abs(target.preferences.healthcare)-abs(party.preferences.healthcare))
    score += abs(abs(target.preferences.education)-abs(party.preferences.education))
    score += abs(abs(target.preferences.immigration)-abs(party.preferences.immigration))
    score += abs(abs(target.preferences.environment)-abs(party.preferences.environment))
    score += abs(abs(target.preferences.crime)-abs(party.preferences.crime))
    score += abs(abs(target.preferences.government_size)-abs(party.preferences.government_size))
    score += abs(abs(target.preferences.foreign_policy)-abs(party.preferences.foreign_policy))
    score += abs(abs(target.preferences.infrastructure)-abs(party.preferences.infrastructure))

    score += abs(abs(target.weights.economy)-abs(party.weights.economy))
    score += abs(abs(target.weights.tax)-abs(party.weights.tax))
    score += abs(abs(target.weights.healthcare)-abs(party.weights.healthcare))
    score += abs(abs(target.weights.education)-abs(party.weights.education))
    score += abs(abs(target.weights.immigration)-abs(party.weights.immigration))
    score += abs(abs(target.weights.environment)-abs(party.weights.environment))
    score += abs(abs(target.weights.crime)-abs(party.weights.crime))
    score += abs(abs(target.weights.government_size)-abs(party.weights.government_size))
    score += abs(abs(target.weights.foreign_policy)-abs(party.weights.foreign_policy))
    score += abs(abs(target.weights.infrastructure)-abs(party.weights.infrastructure))

    return score

class CandidateTraits:
    def __init__(self, charisma, debate_skill, media_skill, fundraising, organization, discipline, persuasion, leadership, authenticity, experience, risk_tolerance, coalition_building):
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

    def __repr__(self):
        return f"CandidateTraits(charisma={self.charisma}, debate_skill={self.debate_skill}, media_skill={self.media_skill}, fundraising={self.fundraising}, organization={self.organization}, discipline={self.discipline}, persuasion={self.persuasion}, leadership={self.leadership}, authenticity={self.authenticity}, experience={self.experience}, risk_tolerance={self.risk_tolerance}, coalition_building={self.coalition_building})"


class Candidate:
    def __init__(self, party):
        self.name = DEFAULT_CANDIDATES[party]["name"]
        self.party = party
        self.preferences = Preferences(DEFAULT_CANDIDATES[party]["preferences"]["economy"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["taxes"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["healthcare"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["education"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["immigration"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["environment"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["crime"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["government_size"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["foreign_policy"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["infrastructure"])

        self.weights = Weights(DEFAULT_CANDIDATES[party]["weights"]["economy"],
                               DEFAULT_CANDIDATES[party]["weights"]["taxes"],
                               DEFAULT_CANDIDATES[party]["weights"]["healthcare"],
                               DEFAULT_CANDIDATES[party]["weights"]["education"],
                               DEFAULT_CANDIDATES[party]["weights"]["immigration"],
                               DEFAULT_CANDIDATES[party]["weights"]["environment"],
                               DEFAULT_CANDIDATES[party]["weights"]["crime"],
                               DEFAULT_CANDIDATES[party]["weights"]["government_size"],
                               DEFAULT_CANDIDATES[party]["weights"]["foreign_policy"],
                               DEFAULT_CANDIDATES[party]["weights"]["infrastructure"])

        self.traits = CandidateTraits(DEFAULT_CANDIDATES[party]["traits"]["charisma"],
                                      DEFAULT_CANDIDATES[party]["traits"]["debate_skill"],
                                      DEFAULT_CANDIDATES[party]["traits"]["media_skill"],
                                      DEFAULT_CANDIDATES[party]["traits"]["fundraising"],
                                      DEFAULT_CANDIDATES[party]["traits"]["organization"],
                                      DEFAULT_CANDIDATES[party]["traits"]["discipline"],
                                      DEFAULT_CANDIDATES[party]["traits"]["persuasion"],
                                      DEFAULT_CANDIDATES[party]["traits"]["leadership"],
                                      DEFAULT_CANDIDATES[party]["traits"]["authenticity"],
                                      DEFAULT_CANDIDATES[party]["traits"]["experience"],
                                      DEFAULT_CANDIDATES[party]["traits"]["risk_tolerance"],
                                      DEFAULT_CANDIDATES[party]["traits"]["coalition_building"])
                                    
        self.money = 0

class Party:
    def __init__(self, name):
        self.name = name
        self.preferences = Preferences(DEFAULT_PARTY_PREFERENCES[name]["preferences"]["economy"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["taxes"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["healthcare"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["education"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["immigration"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["environment"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["crime"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["government_size"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["foreign_policy"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["infrastructure"])
        
        self.weights = Weights(DEFAULT_PARTY_PREFERENCES[name]["weights"]["economy"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["taxes"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["healthcare"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["education"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["immigration"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["environment"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["crime"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["government_size"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["foreign_policy"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["infrastructure"])

        self.candidate = Candidate(name)

    def __repr__(self):
        return f"Party(name={self.name}, ideology={self.ideology})"