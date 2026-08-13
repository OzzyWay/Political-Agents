import numpy as np
from settings import EDUCATION_LEVELS, EDUCATION_WEIGHTS, REGION_VOTERS, DEFAULT_REGIONAL_LEAN

class Voter:
    def __init__(self, id, name, age, region):
        self.id = id
        self.name = name
        self.age = age
        self.income = round(np.random.lognormal(mean=np.log(65000), sigma=0.6))
        self.education = np.random.choice(EDUCATION_LEVELS, size=EDUCATION_LEVELS.__len__(),p=EDUCATION_WEIGHTS)
        self.region = region

        self.turnout_probability = np.clip(np.random.normal(loc=0.6, scale=0.1), 0, 1)

        region_data = DEFAULT_REGIONAL_LEAN.get(region, {})
        region_preferences = region_data.get("preferences", {})
        region_weights = region_data.get("weights", {})
        region_variation = region_data.get("variation", 0.1)

        self.economy_preference = region_preferences.get("economy", 0.5) + np.random.normal(0, region_variation)
        self.tax_preference = region_preferences.get("taxes", 0.5) + np.random.normal(0, region_variation)
        self.healthcare_preference = region_preferences.get("healthcare", 0.5) + np.random.normal(0, region_variation)
        self.education_preference = region_preferences.get("education", 0.5) + np.random.normal(0, region_variation)
        self.immigration_preference = region_preferences.get("immigration", 0.5) + np.random.normal(0, region_variation)
        self.environment_preference = region_preferences.get("environment", 0.5) + np.random.normal(0, region_variation)
        self.crime_preference = region_preferences.get("crime", 0.5) + np.random.normal(0, region_variation)
        self.government_size_preference = region_preferences.get("government_size", 0.5) + np.random.normal(0, region_variation)
        self.foreign_policy_preference = region_preferences.get("foreign_policy", 0.5) + np.random.normal(0, region_variation)
        self.infrastructure_preference = region_preferences.get("infrastructure", 0.5) + np.random.normal(0, region_variation)

        self.economy_weight = region_weights.get("economy", 0.5) + np.random.normal(0, region_variation)
        self.tax_weight = region_weights.get("taxes", 0.5) + np.random.normal(0, region_variation)
        self.healthcare_weight = region_weights.get("healthcare", 0.5) + np.random.normal(0, region_variation)
        self.education_weight = region_weights.get("education", 0.5) + np.random.normal(0, region_variation)
        self.immigration_weight = region_weights.get("immigration", 0.5) + np.random.normal(0, region_variation)
        self.environment_weight = region_weights.get("environment", 0.5) + np.random.normal(0, region_variation)
        self.crime_weight = region_weights.get("crime", 0.5) + np.random.normal(0, region_variation)
        self.government_size_weight = region_weights.get("government_size", 0.5) + np.random.normal(0, region_variation)
        self.foreign_policy_weight = region_weights.get("foreign_policy", 0.5) + np.random.normal(0, region_variation)
        self.infrastructure_weight = region_weights.get("infrastructure", 0.5) + np.random.normal(0, region_variation)

    def __repr__(self):
        return f"Voter(id={self.id}, name='{self.name}', age={self.age}, economy_preference={self.economy_preference}, tax_preference={self.tax_preference}, healthcare_preference={self.healthcare_preference}, education_preference={self.education_preference}, immigration_preference={self.immigration_preference}, environment_preference={self.environment_preference}, crime_preference={self.crime_preference}, government_size_preference={self.government_size_preference}, foreign_policy_preference={self.foreign_policy_preference}, infrastructure_preference={self.infrastructure_preference}, economy_weight={self.economy_weight}, tax_weight={self.tax_weight}, healthcare_weight={self.healthcare_weight}, education_weight={self.education_weight}, immigration_weight={self.immigration_weight}, environment_weight={self.environment_weight}, crime_weight={self.crime_weight}, government_size_weight={self.government_size_weight}, foreign_policy_weight={self.foreign_policy_weight}, infrastructure_weight={self.infrastructure_weight})"

class VoterList:
    def __init__(self, voter):
        self.voter = voter
        self.next = None
        self.prev = None

def GenerateVoterList(region, num_voters):
    head = None
    tail = None

    for i in range(num_voters):
        voter = Voter(id=i, name=f"Voter {i}", age=np.random.randint(18, 80), region=region)
        new_node = VoterList(voter)

        if head is None:
            head = new_node
            tail = new_node
        else:
            tail.next = new_node
            new_node.prev = tail
            tail = new_node

    return head
