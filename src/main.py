from simulation.voters import Voter, VoterList, GenerateVoterList
from simulation.world import Region, World
from settings import DEFAULT_REGIONS, REGION_VOTERS

world = World(regions=DEFAULT_REGIONS)

for region in world.regions:
    print(region)
