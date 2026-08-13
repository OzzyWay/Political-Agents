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
        return f"Preference(economy={self.economy},\ntax={self.tax},\nhealthcare={self.healthcare},\neducation={self.education},\nimmigration={self.immigration},\nenvironment={self.environment},\ncrime={self.crime},\ngovernment_size={self.government_size},\nforeign_policy={self.foreign_policy},\ninfrastructure={self.infrastructure})"

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
        return f"Weights(economy={self.economy},\ntax={self.tax},\nhealthcare={self.healthcare},\neducation={self.education},\nimmigration={self.immigration},\nenvironment={self.environment},\ncrime={self.crime},\ngovernment_size={self.government_size},\nforeign_policy={self.foreign_policy},\ninfrastructure={self.infrastructure})"