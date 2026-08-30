import logging

from simulation.campaignmanager import CampaignManager
from simulation.polling import Poll
from simulation.world import World
from simulation.events import CampaignEvent, EventType
from settings import (
    DEFAULT_CANDIDATES,
    DEFAULT_PARTY_PREFERENCES,
    DEFAULT_REGIONS,
    DEFAULT_REGIONAL_LEAN,
    LOG_PATH,
    load_settings,
    save_settings,
)
from simulation.campaignaction import ActionType


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
    ai_strategies = {}
    prompt = settings.get("campaign_style_prompt")
    if prompt:
        for party in world.parties:
            ai_strategies[party.candidate.name] = {"prompt": prompt}
    events_cfg = settings.get("events", [])
    events = [CampaignEvent.from_dict(e) for e in events_cfg] if events_cfg else None

    manager = CampaignManager(
        world=world,
        campaign_weeks=int(settings["campaign_weeks"]),
        starting_budget_per_candidate=settings.get("starting_budget_per_candidate"),
        use_ai=bool(settings.get("use_ai", True)),
        ai_model=str(settings.get("ai_model", "llama2")),
        ai_strategies=ai_strategies,
        events=events,
    )
    log_message(logger, f"Starting campaign simulation for {len(settings['regions'])} regions and {settings['campaign_weeks']} weeks.")
    report = manager.run_campaign()
    log_message(logger, "Campaign simulation completed.")
    try:
        from simulation.voting import run_election
        results = run_election(manager.world.regions, manager.world.parties)
        log_message(logger, f"Election results: {results}")
        print("\n--- ELECTION RESULTS ---")
        for k, v in results.items():
            print(f"  {k}: {v:.3%}")
        print("--- END RESULTS ---\n")
    except Exception as e:
        log_message(logger, f"Election simulation failed: {e}")
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
            "8": "Campaign style prompt",
            "9": "Simulation parameters",
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
        elif choice == "8":
            raw_prompt = input(f"Set campaign style prompt (current present: {'yes' if settings.get('campaign_style_prompt') else 'no'}): ").strip()
            settings["campaign_style_prompt"] = raw_prompt or None
        elif choice == "9":
            sim = settings.setdefault("simulation", {})
            while True:
                print_menu("Simulation parameters", {
                    "1": "Starting budget per candidate",
                    "2": "Diminishing return decay",
                    "3": "Fundraising params (JSON)",
                    "4": "Base action costs (JSON)",
                    "5": "Action effectiveness (JSON)",
                    "6": "Per-action parameter editor",
                    "0": "Back",
                })
                sub = input("Choose: ").strip()
                if sub == "0":
                    break
                if sub == "1":
                    val = input(f"Starting budget (current: {settings.get('starting_budget_per_candidate', 500000)}): ").strip()
                    try:
                        settings["starting_budget_per_candidate"] = float(val)
                    except Exception:
                        print("Invalid number.")
                elif sub == "2":
                    val = input(f"Diminishing return decay (current: {settings.get('diminishing_return_decay', 0.35)}): ").strip()
                    try:
                        settings["diminishing_return_decay"] = float(val)
                    except Exception:
                        print("Invalid number.")
                elif sub in ("3", "4", "5"):
                    key_map = {"3": "fundraising_params", "4": "base_action_costs", "5": "action_effectiveness"}
                    key = key_map[sub]
                    cur = settings.get(key)
                    print(f"Current {key}: {cur}")
                    raw = input("Enter JSON to replace or blank to cancel: ").strip()
                    if not raw:
                        continue
                    try:
                        import json

                        parsed = json.loads(raw)
                        settings[key] = parsed
                    except Exception as e:
                        print(f"Invalid JSON: {e}")
                elif sub == "6":
                    cfg = settings
                    bac = cfg.setdefault("base_action_costs", {})
                    eff = cfg.setdefault("action_effectiveness", {})
                    reach = cfg.setdefault("action_reach", {})
                    efficiency = cfg.setdefault("action_efficiency", {})
                    pop = cfg.setdefault("action_popularity_impact", {})
                    action_names = [at.name for at in ActionType]
                    while True:
                        menu = {str(i+1): name for i, name in enumerate(action_names)}
                        menu["0"] = "Back"
                        print_menu("Per-action editor", menu)
                        choice_a = input("Choose action to edit: ").strip()
                        if choice_a == "0":
                            break
                        try:
                            idx = int(choice_a) - 1
                            action_key = action_names[idx]
                        except Exception:
                            print("Invalid selection.")
                            continue

                        current = {
                            "base_cost": bac.get(action_key, None),
                            "effectiveness": eff.get(action_key, None),
                            "reach": reach.get(action_key, None),
                            "efficiency": efficiency.get(action_key, None),
                            "popularity": pop.get(action_key, None),
                        }
                        print(f"Current for {action_key}: {current}")
                        print("Enter new values or leave blank to keep current")
                        val = input(f"Base cost (current {current['base_cost']}): ").strip()
                        if val:
                            try:
                                bac[action_key] = float(val)
                            except Exception:
                                print("Invalid number for base cost.")
                        val = input(f"Effectiveness (current {current['effectiveness']}): ").strip()
                        if val:
                            try:
                                eff[action_key] = float(val)
                            except Exception:
                                print("Invalid number for effectiveness.")
                        val = input(f"Reach (current {current['reach']}): ").strip()
                        if val:
                            try:
                                reach[action_key] = float(val)
                            except Exception:
                                print("Invalid number for reach.")
                        val = input(f"Efficiency (current {current['efficiency']}): ").strip()
                        if val:
                            try:
                                efficiency[action_key] = float(val)
                            except Exception:
                                print("Invalid number for efficiency.")
                        val = input(f"Popularity impact (current {current['popularity']}): ").strip()
                        if val:
                            try:
                                pop[action_key] = float(val)
                            except Exception:
                                print("Invalid number for popularity.")
                else:
                    print("Invalid choice.")
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
    print(f"- Campaign style prompt present: {'yes' if settings.get('campaign_style_prompt') else 'no'}")
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
        elif choice == "7":
            try:
                randomize = input("Create random events now? (y/n): ").strip().lower()
                if randomize == "y":
                    num = prompt_int("Number of events", 3)
                    max_week = prompt_int("Max week (campaign weeks)", settings.get("campaign_weeks", 8))
                    scandal_only = input("Scandals only? (y/n)").strip().lower() == "y"
                    import random

                    evs = []
                    candidates = [c["name"] for c in DEFAULT_CANDIDATES.values()]
                    regions = settings.get("regions", [])
                    types = [EventType.SCANDAL] if scandal_only else list(EventType)
                    for i in range(num):
                        et = random.choice(types)
                        week = random.randint(1, max(1, max_week))
                        cand = random.choice(candidates)
                        region = random.choice(regions + [None])
                        affinity = -abs(random.uniform(0.05, 0.25)) if et == EventType.SCANDAL else random.uniform(-0.1, 0.1)
                        popularity = -abs(random.uniform(0.01, 0.08)) if et == EventType.SCANDAL else random.uniform(-0.05, 0.05)
                        ev = CampaignEvent(event_type=et, week=week, candidate_name=cand, region=region, affinity_delta=affinity, popularity_delta=popularity, description=f"Random {et.name.lower()} for {cand}")
                        evs.append(ev.to_dict())
                    settings["events"] = evs
                    save_settings(settings)
                    print(f"Saved {len(evs)} events to settings. Running campaign...")
                    run_campaign(settings, logger)
                else:
                    print("Cancelled.")
            except Exception as exc:
                log_message(logger, f"Randomize events failed: {exc}")
                print(f"Randomize events failed: {exc}")

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
