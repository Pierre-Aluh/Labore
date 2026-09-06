import json
from pathlib import Path


def test_homologation_fixture_is_synthetic() -> None:
    fixture = json.loads((Path(__file__).parent / "fixtures" / "synthetic_data.json").read_text(encoding="utf-8"))
    assert all(company["tax_identifier"].startswith("SYNTH-") for company in fixture["companies"])
    assert all(user["email"].endswith("@example.invalid") for user in fixture["users"])
    assert "fictícios" in fixture["notice"]
