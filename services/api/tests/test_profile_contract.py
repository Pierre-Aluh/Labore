from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.api import UserResponse


def test_profile_contract_exposes_roles() -> None:
    profile = UserResponse(id="synthetic", email="user@example.invalid", display_name="Synthetic", roles=["Cliente"], company_ids=[])
    assert profile.roles == ["Cliente"]
