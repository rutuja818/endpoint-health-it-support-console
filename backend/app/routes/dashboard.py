from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Endpoint, SupportTicket

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    endpoints = db.query(Endpoint).all()
    tickets = db.query(SupportTicket).all()

    return {
        "total_endpoints": len(endpoints),
        "healthy": sum(1 for e in endpoints if e.status == "healthy"),
        "warning": sum(1 for e in endpoints if e.status == "warning"),
        "critical": sum(1 for e in endpoints if e.status == "critical"),
        "offline": sum(1 for e in endpoints if e.status == "offline"),
        "open_tickets": sum(1 for t in tickets if t.status in ("Open", "In Progress")),
        "high_priority": sum(1 for t in tickets if t.priority in ("High", "Critical") and t.status not in ("Resolved","Closed")),
        "tickets": len(tickets),
    }

@router.get("/reports")
def reports(db: Session = Depends(get_db)):
    endpoints = db.query(Endpoint).all()
    tickets = db.query(SupportTicket).all()

    os_distribution = {}
    for e in endpoints:
        os_distribution[e.os or "Unknown"] = os_distribution.get(e.os or "Unknown", 0) + 1

    ticket_status = {}
    for t in tickets:
        ticket_status[t.status] = ticket_status.get(t.status, 0) + 1

    return {
        "os_distribution": os_distribution,
        "ticket_status": ticket_status,
    }
