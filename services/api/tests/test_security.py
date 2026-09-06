from datetime import UTC, datetime, timedelta

from app.security import hash_password, hash_session_token, verify_password


def test_password_hash_is_not_plaintext_and_verifies() -> None:
    password = "synthetic-test-password"
    password_hash = hash_password(password)
    assert password_hash != password
    assert verify_password(password, password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_session_token_hash_is_deterministic_and_not_plaintext() -> None:
    token = "synthetic-session-token"
    hashed = hash_session_token(token)
    assert hashed != token
    assert hash_session_token(token) == hashed


def test_expired_time_is_in_the_past() -> None:
    now = datetime.now(UTC)
    assert now - timedelta(seconds=1) < now
