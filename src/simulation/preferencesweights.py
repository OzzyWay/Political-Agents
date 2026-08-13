class Preferences:
    def __init__(self, economy, tax, healthcare, education, immigration, environment, crime, government_size, foreign_policy, infrastructure):
        self.economy = economy
        self.tax = tax
        self.healthcare = healthcare
        self.education = education
        self.immigration = immigration
        self.environment = environment
        self.crime = crime
        self.government_size = government_size
        self.foreign_policy = foreign_policy
        self.infrastructure = infrastructure

    def __repr__(self):
        return f"Preference(economy={self.economy}, tax={self.tax}, healthcare={self.healthcare}, education={self.education}, immigration={self.immigration}, environment={self.environment}, crime={self.crime}, government_size={self.government_size}, foreign_policy={self.foreign_policy}, infrastructure={self.infrastructure})"

class Weights:
    def __init__(self, economy, tax, healthcare, education, immigration, environment, crime, government_size, foreign_policy, infrastructure):
        self.economy = economy
        self.tax = tax
        self.healthcare = healthcare
        self.education = education
        self.immigration = immigration
        self.environment = environment
        self.crime = crime
        self.government_size = government_size
        self.foreign_policy = foreign_policy
        self.infrastructure = infrastructure

    def __repr__(self):
        return f"Weights(economy={self.economy}, tax={self.tax}, healthcare={self.healthcare}, education={self.education}, immigration={self.immigration}, environment={self.environment}, crime={self.crime}, government_size={self.government_size}, foreign_policy={self.foreign_policy}, infrastructure={self.infrastructure})"