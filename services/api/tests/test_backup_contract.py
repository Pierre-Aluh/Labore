from pathlib import Path


ROOT = Path(__file__).parents[3]


def test_backup_script_excludes_secrets_and_captures_database() -> None:
    script = (ROOT / "infra" / "scripts" / "backup.ps1").read_text(encoding="utf-8")
    assert "pg_dump" in script
    assert "includes_secrets = $false" in script
    assert "CLOUDFLARE" not in script


def test_restore_is_simulation_by_default() -> None:
    script = (ROOT / "infra" / "scripts" / "restore.ps1").read_text(encoding="utf-8")
    assert "[switch]$ConfirmRestore" in script
    assert "Simulação concluída" in script
