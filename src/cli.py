import json
import logging

from simulation.campaignmanager import CampaignManager
from simulation.polling import Poll
from simulation.world import World
from settings import (
    DEFAULT_CANDIDATES,
    DEFAULT_PARTY_PREFERENCES,
    DEFAULT_REGIONS,
    REGION_VOTERS,
    LOG_PATH,
    load_settings,
    save_settings,
)


def setup_logger(level_name: str = "INFO"):
    level = getattr(logging, str(level_name).upper(), logging.INFO)
    logger = logging.getLogger("political_agents")
    logger.setLevel(level)
    logger.handlers.clear()

    handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    return logger


def log_message(logger, message: str):
    print(message)
    logger.info(message)


def run_poll(world):
    region = world.regions[0] if world.regions else None
    if region is None:
        raise ValueError("No regions available to simulate.")

    poll = Poll("Regional", 1, region)
    poll.run_poll(world.parties)
    return poll.results


def run_campaign(settings, logger):
    world = World(regions=settings["regions"])
    manager = CampaignManager(
        world=world,
        campaign_weeks=int(settings["campaign_weeks"]),
        starting_budget_per_candidate=500000,
        use_ai=bool(settings.get("use_ai", True)),
        ai_model=str(settings.get("ai_model", "llama2")),
    )
    log_message(logger, f"Starting campaign simulation for {len(settings['regions'])} regions and {settings['campaign_weeks']} weeks.")
    report = manager.run_campaign()
    log_message(logger, "Campaign simulation completed.")
    return report


def view_log():
    if not LOG_PATH.exists():
        print("No log file exists yet.")
        return
    with LOG_PATH.open("r", encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    if not lines:
        print("Log is empty.")
        return
    print("\n--- LOG ---")
    for line in lines[-20:]:
        print(line)
    print("--- END LOG ---\n")


def change_settings(settings):
    while True:
        print("\nSettings")
        print("1. Regions")
        print("2. Voters per region")
        print("3. Campaign weeks")
        print("4. Toggle AI")
        print("5. AI model")
        print("6. Save and return")

        choice = input("Select an option: ").strip()

        if choice == "1":
            raw_regions = input("Enter regions as comma-separated names (current: %s): " % ", ".join(settings["regions"]))
            if raw_regions.strip():
                settings["regions"] = [region.strip() for region in raw_regions.split(",") if region.strip()]
        elif choice == "2":
            value = input(f"Enter voters per region (current: {settings['voters_per_region']}): ")
            if value.strip():
                settings["voters_per_region"] = max(100, int(value))
        elif choice == "3":
            value = input(f"Enter campaign weeks (current: {settings['campaign_weeks']}): ")
            if value.strip():
                settings["campaign_weeks"] = max(1, int(value))
        elif choice == "4":
            settings["use_ai"] = not settings.get("use_ai", True)
            print(f"AI mode is now {'ON' if settings['use_ai'] else 'OFF'}")
        elif choice == "5":
            value = input(f"Enter AI model name (current: {settings.get('ai_model', 'llama2')}): ")
            if value.strip():
                settings["ai_model"] = value.strip()
        elif choice == "6":
            save_settings(settings)
            return
        else:
            print("Invalid option.")


def show_runtime_config(settings):
    print("\nCurrent project settings")
    print(f"- Regions: {', '.join(settings['regions'])}")
    print(f"- Voters per region: {settings['voters_per_region']}")
    print(f"- Campaign weeks: {settings['campaign_weeks']}")
    print(f"- AI enabled: {'yes' if settings.get('use_ai', True) else 'no'}")
    print(f"- AI model: {settings.get('ai_model', 'llama2')}")
    print(f"- Parties: {', '.join(settings.get('party_names', list(DEFAULT_PARTY_PREFERENCES.keys())))}")
    print(f"- Candidates: {', '.join(settings.get('candidate_names', [candidate['name'] for candidate in DEFAULT_CANDIDATES.values()]))}")


def main():
    settings = load_settings()
    logger = setup_logger(settings.get("log_level", "INFO"))

    while True:
        print("\nPolitical Agents Console")
        print("1. Show current settings")
        print("2. Run quick poll")
        print("3. Run campaign simulation")
        print("4. View log")
        print("5. Change settings")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_runtime_config(settings)

        elif choice == "2":
            try:
                world = World(regions=settings["regions"])
                result = run_poll(world)
                log_message(logger, f"Quick poll complete: {result}")
                print(result)
            except Exception as exc:
                log_message(logger, f"Quick poll failed: {exc}")
                print(f"Quick poll failed: {exc}")

        elif choice == "3":
            try:
                run_campaign(settings, logger)
            except Exception as exc:
                log_message(logger, f"Campaign simulation failed: {exc}")
                print(f"Campaign simulation failed: {exc}")

        elif choice == "4":
            view_log()

        elif choice == "5":
            change_settings(settings)
            logger = setup_logger(settings.get("log_level", "INFO"))

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid input.")
