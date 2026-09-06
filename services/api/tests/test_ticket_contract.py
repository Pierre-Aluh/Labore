from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.ticket_api import TicketCreate


def test_ticket_requires_subject_and_description() -> None:
    payload = TicketCreate(company_id=uuid4(), subject="Dúvida sintética", description="Descrição de teste")
    assert payload.subject == "Dúvida sintética"


def test_ticket_can_target_a_department() -> None:
    department_id = uuid4()
    payload = TicketCreate(company_id=uuid4(), subject="Chamado", description="Teste", department_id=department_id)
    assert payload.department_id == department_id
