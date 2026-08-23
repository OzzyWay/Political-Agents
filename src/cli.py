import logging

from simulation.campaignmanager import CampaignManager
from simulation.polling import Poll
from simulation.world import World
from settings import (
    DEFAULT_CANDIDATES,
    DEFAULT_PARTY_PREFERENCES,
    DEFAULT_REGIONS,
    DEFAULT_REGIONAL_LEAN,
    LOG_PATH,
    load_settings,
    save_settings,
)


POLICY_KEYS = [
    "economy",
    "taxes",
    "healthcare",
    "education",
    "immigration",
    "environment",
    "crime",
    "government_size",
    "foreign_policy",
    "infrastructure",
]


def print_header(title):
    print("\n" + "=" * 72)
    print(f"{title:^{72}}")
    print("=" * 72)


def print_menu(title, options):
    print_header(title)
    for key, label in options.items():
        print(f"  {key}. {label}")
    print()


def prompt_float(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        print("  Please enter a number.")
        return prompt_float(prompt, default)


def prompt_int(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print("  Please enter an integer.")
        return prompt_int(prompt, default)


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


def run_poll(world, sample_size=500):
    region = world.regions[0] if world.regions else None
    if region is None:
        raise ValueError("No regions available to simulate.")

    poll = Poll("Regional", max(1, int(sample_size)), region.voter_list)
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


def display_policy_dict(title, value_dict):
    print(f"  {title}")
    for key in POLICY_KEYS:
        print(f"    - {key}: {value_dict.get(key, 0.0):.2f}")


def update_policy_dict(target_dict, section_name):
    while True:
        print(f"\nEditing {section_name}")
        for key in POLICY_KEYS:
            print(f"  {key}: {target_dict.get(key, 0.0):.2f}")
        print("  0. Back")
        choice = input("Select a field to edit: ").strip()

        if choice == "0":
            return

        if choice not in POLICY_KEYS:
            print("  Invalid field.")
            continue

        target_dict[choice] = prompt_float(f"Set {choice}", target_dict.get(choice, 0.0))


def edit_region_profiles(settings):
    region_names = list(settings.get("regions", DEFAULT_REGIONS))
    if not region_names:
        print("No regions configured.")
        return

    while True:
        print_menu("Regional model", {str(i): region for i, region in enumerate(region_names, 1)})
        print("  0. Back")
        choice = input("Choose a region: ").strip()

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            region_name = region_names[index]
        except (ValueError, IndexError):
            print("  Invalid selection.")
            continue

        region_data = DEFAULT_REGIONAL_LEAN.setdefault(region_name, {
            "preferences": {key: 0.0 for key in POLICY_KEYS},
            "weights": {key: 0.0 for key in POLICY_KEYS},
            "variation": 0.1,
        })

        while True:
            print_menu(f"Region: {region_name}", {
                "1": "Preferences",
                "2": "Weights",
                "3": "Variation",
                "0": "Back",
            })
            action = input("Select an option: ").strip()

            if action == "1":
                update_policy_dict(region_data.setdefault("preferences", {}), f"{region_name} preferences")
            elif action == "2":
                update_policy_dict(region_data.setdefault("weights", {}), f"{region_name} weights")
            elif action == "3":
                region_data["variation"] = prompt_float("Set regional variation", region_data.get("variation", 0.1))
            elif action == "0":
                break
            else:
                print("  Invalid choice.")


def edit_party_profiles(settings):
    party_names = list(DEFAULT_PARTY_PREFERENCES.keys())
    if not party_names:
        print("No parties configured.")
        return

    while True:
        print_menu("Party profiles", {str(i): party for i, party in enumerate(party_names, 1)})
        print("  0. Back")
        choice = input("Choose a party: ").strip()

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            party_name = party_names[index]
        except (ValueError, IndexError):
            print("  Invalid selection.")
            continue

        party_data = DEFAULT_PARTY_PREFERENCES.setdefault(party_name, {
            "preferences": {key: 0.0 for key in POLICY_KEYS},
            "weights": {key: 0.0 for key in POLICY_KEYS},
            "popularity": 0.5,
        })

        while True:
            print_menu(f"Party: {party_name}", {
                "1": "Preferences",
                "2": "Weights",
                "3": "Popularity",
                "0": "Back",
            })
            action = input("Select an option: ").strip()

            if action == "1":
                update_policy_dict(party_data.setdefault("preferences", {}), f"{party_name} preferences")
            elif action == "2":
                update_policy_dict(party_data.setdefault("weights", {}), f"{party_name} weights")
            elif action == "3":
                party_data["popularity"] = prompt_float("Set popularity", party_data.get("popularity", 0.5))
            elif action == "0":
                break
            else:
                print("  Invalid choice.")


def edit_candidate_profiles(settings):
    candidate_names = [candidate["name"] for candidate in DEFAULT_CANDIDATES.values()]
    if not candidate_names:
        print("No candidates configured.")
        return

    while True:
        print_menu("Candidate profiles", {str(i): name for i, name in enumerate(candidate_names, 1)})
        print("  0. Back")
        choice = input("Choose a candidate: ").strip()

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            candidate_name = candidate_names[index]
        except (ValueError, IndexError):
            print("  Invalid selection.")
            continue

        candidate_entry = next(
            entry for entry in DEFAULT_CANDIDATES.values() if entry["name"] == candidate_name
        )

        while True:
            print_menu(f"Candidate: {candidate_name}", {
                "1": "Preferences",
                "2": "Weights",
                "3": "Traits",
                "0": "Back",
            })
            action = input("Select an option: ").strip()

            if action == "1":
                update_policy_dict(candidate_entry.setdefault("preferences", {}), f"{candidate_name} preferences")
            elif action == "2":
                update_policy_dict(candidate_entry.setdefault("weights", {}), f"{candidate_name} weights")
            elif action == "3":
                trait_keys = sorted(candidate_entry.get("traits", {}).keys())
                print("  Traits:")
                for trait in trait_keys:
                    print(f"    - {trait}: {candidate_entry['traits'][trait]:.2f}")
                print("  0. Back")
                sub = input("Choose a trait: ").strip()
                if sub == "0":
                    continue
                if sub in candidate_entry.get("traits", {}):
                    candidate_entry["traits"][sub] = prompt_float(f"Set {sub}", candidate_entry["traits"][sub])
                else:
                    print("  Invalid trait.")
            elif action == "0":
                break
            else:
                print("  Invalid choice.")


def edit_runtime_settings(settings):
    while True:
        print_menu("Runtime settings", {
            "1": "Regions",
            "2": "Voters per region",
            "3": "Campaign weeks",
            "4": "People per poll",
            "5": "Toggle AI",
            "6": "AI model",
            "7": "Log level",
            "0": "Back",
        })
        choice = input("Select an option: ").strip()

        if choice == "0":
            return
        if choice == "1":
            raw_regions = input(f"Enter regions as a comma-separated list (current: {', '.join(settings['regions'])}): ").strip()
            if raw_regions:
                settings["regions"] = [region.strip() for region in raw_regions.split(",") if region.strip()]
        elif choice == "2":
            settings["voters_per_region"] = prompt_int("Set voters per region", settings.get("voters_per_region", 10000))
        elif choice == "3":
            settings["campaign_weeks"] = prompt_int("Set campaign weeks", settings.get("campaign_weeks", 8))
        elif choice == "4":
            settings["poll_sample_size"] = prompt_int("Set people per poll", settings.get("poll_sample_size", 500))
        elif choice == "5":
            settings["use_ai"] = not settings.get("use_ai", True)
            print(f"  AI mode is now {'ON' if settings['use_ai'] else 'OFF'}")
        elif choice == "6":
            settings["ai_model"] = input(f"Set AI model (current: {settings.get('ai_model', 'llama2')}): ").strip() or settings.get("ai_model", "llama2")
        elif choice == "7":
            settings["log_level"] = input(f"Set log level (current: {settings.get('log_level', 'INFO')}): ").strip().upper() or settings.get("log_level", "INFO")
        else:
            print("  Invalid option.")


def change_settings(settings):
    while True:
        print_menu("Configuration", {
            "1": "Runtime settings",
            "2": "Regional model",
            "3": "Party profiles",
            "4": "Candidate profiles",
            "5": "Save and return",
            "0": "Exit without saving",
        })
        choice = input("Select a configuration area: ").strip()

        if choice == "1":
            edit_runtime_settings(settings)
        elif choice == "2":
            edit_region_profiles(settings)
        elif choice == "3":
            edit_party_profiles(settings)
        elif choice == "4":
            edit_candidate_profiles(settings)
        elif choice == "5":
            save_settings(settings)
            print("  Settings saved.")
            return
        elif choice == "0":
            return
        else:
            print("  Invalid option.")


def show_runtime_config(settings):
    print_header("Current project settings")
    print(f"- Regions: {', '.join(settings['regions'])}")
    print(f"- Voters per region: {settings['voters_per_region']}")
    print(f"- Campaign weeks: {settings['campaign_weeks']}")
    print(f"- People per poll: {settings.get('poll_sample_size', 500)}")
    print(f"- AI enabled: {'yes' if settings.get('use_ai', True) else 'no'}")
    print(f"- AI model: {settings.get('ai_model', 'llama2')}")
    print(f"- Log level: {settings.get('log_level', 'INFO')}")
    print(f"- Parties: {', '.join(DEFAULT_PARTY_PREFERENCES.keys())}")
    print(f"- Candidates: {', '.join(candidate['name'] for candidate in DEFAULT_CANDIDATES.values())}")


def main():
    settings = load_settings()
    logger = setup_logger(settings.get("log_level", "INFO"))

    while True:
        print_menu("Political Agents Console", {
            "1": "Show current settings",
            "2": "Run quick poll",
            "3": "Run campaign simulation",
            "4": "View log",
            "5": "Change settings",
            "6": "Exit",
        })

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_runtime_config(settings)

        elif choice == "2":
            try:
                world = World(regions=settings["regions"])
                result = run_poll(world, settings.get("poll_sample_size", 500))
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
            print("  Invalid input.")
