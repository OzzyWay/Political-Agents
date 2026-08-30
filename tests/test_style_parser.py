from simulation.style_parser import parse_prompt_to_style
from simulation.strategies import PRESETS


def test_parse_preset_name_matches():
    for name, preset in PRESETS.items():
        out = parse_prompt_to_style(name)
        assert isinstance(out, dict)
        assert set(out.keys()) == set(preset.keys())
        for k in preset:
            assert abs(out[k] - preset[k]) < 1e-6


def test_parse_freeform_returns_normalized():
    prompt = "A campaign focused on online outreach and social media heavy efforts."
    out = parse_prompt_to_style(prompt)
    assert isinstance(out, dict)
    keys = {"fundraising", "media", "ground", "digital", "attack"}
    assert set(out.keys()) == keys
    total = sum(out.values())
    assert abs(total - 1.0) < 1e-6
