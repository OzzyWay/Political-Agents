from simulation.voters import Voter, VoterList, GenerateVoterList
from simulation.preferencesweights import Preferences, Weights
from settings import REGION_VOTERS


class Region:
    def getAvgs(self):
        current = self.voter_list
        count = 0

        self.preferences = Preferences(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.weights = Weights(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        while current is not None:
            voter = current.voter

            self.age += voter.age
            self.turnout_probability += voter.turnout_probability

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
            current = current.next

        self.age /= count
        self.turnout_probability /= count
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

    def __init__(self, name, num_voters):
        self.name = name
        self.age = 0
        self.turnout_probability = 0
        self.voter_list = GenerateVoterList(region=name, num_voters=num_voters)

        self.getAvgs()

    def __repr__(self):
        return f"Region(name={self.name}, preferences={self.preferences}, weights={self.weights})"

class World:
    def __init__(self, regions):
        self.regions = [Region(name=region, num_voters=REGION_VOTERS) for region in regions]

    def __repr__(self):
        return f"World(regions={self.regions})"

