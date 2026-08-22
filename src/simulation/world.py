from simulation.voters import Voter, GenerateVoterList
from simulation.preferencesweights import Preferences, Weights
from simulation.parties import Party, Candidate, getPartyAffinity
from settings import REGION_VOTERS, DEFAULT_REGIONS, DEFAULT_PARTY_PREFERENCES, DEFAULT_CANDIDATES


class Region:

    def getAvgs(self):
        count = 0

        self.preferences = Preferences(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.weights = Weights(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        for i in range(self.voter_list.__len__()):
            voter = self.voter_list[i]

            self.age += voter.age
            self.turnout_probability += voter.turnout_probability
            self.income += voter.income

            self.preferences.economy += voter.preferences.economy
            self.preferences.tax += voter.preferences.tax
            self.preferences.healthcare += voter.preferences.healthcare
            self.preferences.education += voter.preferences.education
            self.preferences.immigration += voter.preferences.immigration
            self.preferences.environment += voter.preferences.environment
            self.preferences.crime += voter.preferences.crime
            self.preferences.government_size += voter.preferences.government_size
            self.preferences.foreign_policy += voter.preferences.foreign_policy
            self.preferences.infrastructure += voter.preferences.infrastructure

            self.weights.economy += voter.weights.economy
            self.weights.tax += voter.weights.tax
            self.weights.healthcare += voter.weights.healthcare
            self.weights.education += voter.weights.education
            self.weights.immigration += voter.weights.immigration
            self.weights.environment += voter.weights.environment
            self.weights.crime += voter.weights.crime
            self.weights.government_size += voter.weights.government_size
            self.weights.foreign_policy += voter.weights.foreign_policy
            self.weights.infrastructure += voter.weights.infrastructure

            count += 1

        self.age /= count
        self.turnout_probability /= count
        self.income /= count

        self.preferences.economy /= count
        self.preferences.tax /= count
        self.preferences.healthcare /= count
        self.preferences.education /= count
        self.preferences.immigration /= count
        self.preferences.environment /= count
        self.preferences.crime /= count
        self.preferences.government_size /= count
        self.preferences.foreign_policy /= count
        self.preferences.infrastructure /= count

        self.weights.economy /= count
        self.weights.tax /= count
        self.weights.healthcare /= count
        self.weights.education /= count
        self.weights.immigration /= count
        self.weights.environment /= count
        self.weights.crime /= count
        self.weights.government_size /= count
        self.weights.foreign_policy /= count
        self.weights.infrastructure /= count


    def __init__(self, name, num_voters, parties):
        self.name = name
        self.age = 0
        self.income = 0;
        self.turnout_probability = 0
        self.voter_list = GenerateVoterList(region=name, num_voters=num_voters, parties=parties)

        self.getAvgs()

        self.party_affinity = {party.name: getPartyAffinity(self, party) for party in parties}
        self.candidate_popularity = {party.candidate.name: party.candidate.calculate_regional_popularity(self) for party in parties}

    def __repr__(self):
        return f"Region(\nname={self.name},\npreferences={self.preferences},\nweights={self.weights},\nage={self.age}, \nincome={self.income}, \nturnout_probability={self.turnout_probability}, \nparty_affinity={self.party_affinity},\ncandidate_popularity={self.candidate_popularity})"

    def get_candidate_popularity_details(self):
        details = {}
        for candidate_name, popularity_score in self.candidate_popularity.items():
            details[candidate_name] = {
                'popularity_score': popularity_score,
                'popularity_percent': f"{popularity_score * 100:.1f}%"
            }
        return details

    def rank_candidates_by_popularity(self):
        return sorted(self.candidate_popularity.items(), key=lambda x: x[1], reverse=True)

class World:
    def __init__(self, regions):
        self.parties = [Party(name) for name in DEFAULT_PARTY_PREFERENCES.keys()]
        self.regions = [Region(name=region, num_voters=REGION_VOTERS, parties=self.parties) for region in regions]

    def __repr__(self):
        return f"World(regions={self.regions})"

