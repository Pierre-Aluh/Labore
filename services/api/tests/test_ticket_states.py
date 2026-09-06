from app.models import TicketStatus


def test_ticket_status_catalog_contains_required_states() -> None:
    assert {status.value for status in TicketStatus} == {"open", "waiting_client", "waiting_office", "closed", "reopened"}
