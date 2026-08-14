from simulation.voters import Voter, GenerateVoterList
from simulation.world import Region, World
from simulation.polling import Poll
from settings import DEFAULT_REGIONS, REGION_VOTERS

world = World(regions=DEFAULT_REGIONS)

for region in world.regions:
    print(region)

poll = Poll("Regional", 1, world.regions[3])

poll.run_poll(world.parties)

print(poll.results)