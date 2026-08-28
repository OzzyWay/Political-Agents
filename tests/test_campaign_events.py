from simulation.campaignmanager import CampaignManager
from simulation.events import CampaignEvent, EventType
from simulation.world import World


def test_campaign_events_affect_affinity_and_popularity():
    world = World(regions=["North"], voters_per_region=20)
    candidate_name = world.parties[0].candidate.name
    event = CampaignEvent(
        event_type=EventType.SCANDAL,
        week=1,
        candidate_name=candidate_name,
        region="North",
        affinity_delta=-0.2,
        popularity_delta=-0.1,
    )

    manager = CampaignManager(
        world=world,
        campaign_weeks=2,
        starting_budget_per_candidate=50000,
        use_ai=False,
        events=[event],
    )

    before_affinity = world.regions[0].voter_list[0].candidate_affinity[candidate_name]
    before_popularity = world.parties[0].popularity

    manager._apply_week_events(1)

    after_affinity = world.regions[0].voter_list[0].candidate_affinity[candidate_name]
    after_popularity = world.parties[0].popularity

    assert abs(after_affinity - before_affinity) > 0
    assert abs(after_popularity - before_popularity) > 0
    assert len(manager.tracker.get_candidate_campaign(candidate_name).events_history) == 1
