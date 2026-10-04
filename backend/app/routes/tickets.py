from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import SupportTicket, TroubleshootingLog
from ..schemas import TicketCreate, TicketUpdate

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

def serialize(t):
    return {
        "id": t.id,
        "ticket_number": t.ticket_number,
        "endpoint_id": t.endpoint_id,
        "title": t.title,
        "description": t.description,
        "category": t.category,
        "priority": t.priority,
        "status": t.status,
        "assigned_to": t.assigned_to,
        "resolution": t.resolution,
        "created_at": t.created_at,
        "updated_at": t.updated_at,
        "resolved_at": t.resolved_at,
    }

@router.get("")
def list_tickets(db: Session = Depends(get_db)):
    return [serialize(t) for t in db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).all()]

@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    t = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not t:
        raise HTTPException(404, "Ticket not found")
    return serialize(t)

@router.post("")
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    count = db.query(SupportTicket).count() + 1001
    ticket = SupportTicket(
        ticket_number=f"INC-{count}",
        **payload.model_dump()
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return serialize(ticket)

@router.put("/{ticket_id}")
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    t = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not t:
        raise HTTPException(404, "Ticket not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(t, key, value)

    if payload.status in ("Resolved", "Closed"):
        t.resolved_at = datetime.now()

    db.commit()
    db.refresh(t)
    return serialize(t)

@router.post("/{ticket_id}/logs")
def add_log(ticket_id: int, action_taken: str, result: str = "", db: Session = Depends(get_db)):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Ticket not found")

    existing = db.query(TroubleshootingLog).filter(
        TroubleshootingLog.ticket_id == ticket_id
    ).count()

    log = TroubleshootingLog(
        ticket_id=ticket_id,
        step=existing + 1,
        action_taken=action_taken,
        result=result
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {
        "id": log.id,
        "step": log.step,
        "action_taken": log.action_taken,
        "result": log.result
    }
