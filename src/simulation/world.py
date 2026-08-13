from simulation.voters import Voter, VoterList, GenerateVoterList
from settings import REGION_VOTERS

class Region:
    def __init__(self, name, num_voters):
        self.name = name
        self.AVG_age = 0
        self.voter_list = GenerateVoterList(region=name, num_voters=num_voters)

        self.AVG_economy_preference = 0
        self.AVG_tax_preference = 0
        self.AVG_healthcare_preference = 0
        self.AVG_education_preference = 0
        self.AVG_immigration_preference = 0
        self.AVG_environment_preference = 0
        self.AVG_crime_preference = 0
        self.AVG_government_size_preference = 0
        self.AVG_foreign_policy_preference = 0
        self.AVG_infrastructure_preference = 0

        self.AVG_economy_weight = 0
        self.AVG_tax_weight = 0
        self.AVG_healthcare_weight = 0
        self.AVG_education_weight = 0
        self.AVG_immigration_weight = 0
        self.AVG_environment_weight = 0
        self.AVG_crime_weight = 0
        self.AVG_government_size_weight = 0
        self.AVG_foreign_policy_weight = 0
        self.AVG_infrastructure_weight = 0

    def __repr__(self):
        return f"Region(name='{self.name}', AVG_age={self.AVG_age}, AVG_economy_preference={self.AVG_economy_preference}, AVG_tax_preference={self.AVG_tax_preference}, AVG_healthcare_preference={self.AVG_healthcare_preference}, AVG_education_preference={self.AVG_education_preference}, AVG_immigration_preference={self.AVG_immigration_preference}, AVG_environment_preference={self.AVG_environment_preference}, AVG_crime_preference={self.AVG_crime_preference}, AVG_government_size_preference={self.AVG_government_size_preference}, AVG_foreign_policy_preference={self.AVG_foreign_policy_preference}, AVG_infrastructure_preference={self.AVG_infrastructure_preference}, AVG_economy_weight={self.AVG_economy_weight}, AVG_tax_weight={self.AVG_tax_weight}, AVG_healthcare_weight={self.AVG_healthcare_weight}, AVG_education_weight={self.AVG_education_weight}, AVG_immigration_weight={self.AVG_immigration_weight}, AVG_environment_weight={self.AVG_environment_weight}, AVG_crime_weight={self.AVG_crime_weight}, AVG_government_size_weight={self.AVG_government_size_weight}, AVG_foreign_policy_weight={self.AVG_foreign_policy_weight}, AVG_infrastructure_weight={self.AVG_infrastructure_weight})"

    def getAvgs(self):
        current = self.voter_list
        count = 0

        while current is not None:
            voter = current.voter
            self.AVG_age += voter.age
            self.AVG_economy_preference += voter.economy_preference
            self.AVG_tax_preference += voter.tax_preference
            self.AVG_healthcare_preference += voter.healthcare_preference
            self.AVG_education_preference += voter.education_preference
            self.AVG_immigration_preference += voter.immigration_preference
            self.AVG_environment_preference += voter.environment_preference
            self.AVG_crime_preference += voter.crime_preference
            self.AVG_government_size_preference += voter.government_size_preference
            self.AVG_foreign_policy_preference += voter.foreign_policy_preference
            self.AVG_infrastructure_preference += voter.infrastructure_preference

            self.AVG_economy_weight += voter.economy_weight
            self.AVG_tax_weight += voter.tax_weight
            self.AVG_healthcare_weight += voter.healthcare_weight
            self.AVG_education_weight += voter.education_weight
            self.AVG_immigration_weight += voter.immigration_weight
            self.AVG_environment_weight += voter.environment_weight
            self.AVG_crime_weight += voter.crime_weight
            self.AVG_government_size_weight += voter.government_size_weight
            self.AVG_foreign_policy_weight += voter.foreign_policy_weight
            self.AVG_infrastructure_weight += voter.infrastructure_weight
            
            count += 1
            
            current = current.next

        self.AVG_age /= count
        self.AVG_economy_preference /= count
        self.AVG_tax_preference /= count
        self.AVG_healthcare_preference /= count
        self.AVG_education_preference /= count
        self.AVG_immigration_preference /= count
        self.AVG_environment_preference /= count
        self.AVG_crime_preference /= count
        self.AVG_government_size_preference /= count
        self.AVG_foreign_policy_preference /= count
        self.AVG_infrastructure_preference /= count

        self.AVG_economy_weight /= count
        self.AVG_tax_weight /= count
        self.AVG_healthcare_weight /= count
        self.AVG_education_weight /= count
        self.AVG_immigration_weight /= count
        self.AVG_environment_weight /= count
        self.AVG_crime_weight /= count
        self.AVG_government_size_weight /= count
        self.AVG_foreign_policy_weight /= count
        self.AVG_infrastructure_weight /= count

class World:
    def __init__(self, regions):
        self.regions = [Region(name=region, num_voters=REGION_VOTERS) for region in regions]
        for region in self.regions:
            region.getAvgs()

    def __repr__(self):
        return f"World(regions={self.regions})"

