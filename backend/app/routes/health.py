from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Endpoint, HealthCheck
from ..schemas import HealthCheckCreate
from ..services.health_service import calculate_status

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.post("/check")
def create_health_check(payload: HealthCheckCreate, db: Session = Depends(get_db)):
    endpoint = db.query(Endpoint).filter(Endpoint.id == payload.endpoint_id).first()
    if not endpoint:
        raise HTTPException(404, "Endpoint not found")

    status = calculate_status(payload.cpu_usage, payload.memory_usage, payload.disk_usage)
    check = HealthCheck(
        endpoint_id=payload.endpoint_id,
        cpu_usage=payload.cpu_usage,
        memory_usage=payload.memory_usage,
        disk_usage=payload.disk_usage,
        internet_status=payload.internet_status,
        dns_status=payload.dns_status,
        latency_ms=payload.latency_ms,
        overall_status=status
    )
    endpoint.status = status
    endpoint.last_seen = datetime.now()
    db.add(check)
    db.commit()
    db.refresh(check)

    return {
        "id": check.id,
        "endpoint_id": check.endpoint_id,
        "overall_status": check.overall_status,
        "checked_at": check.checked_at
    }

@router.get("/endpoint/{endpoint_id}")
def endpoint_health(endpoint_id: int, db: Session = Depends(get_db)):
    checks = (
        db.query(HealthCheck)
        .filter(HealthCheck.endpoint_id == endpoint_id)
        .order_by(HealthCheck.checked_at.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "id": c.id,
            "cpu_usage": float(c.cpu_usage or 0),
            "memory_usage": float(c.memory_usage or 0),
            "disk_usage": float(c.disk_usage or 0),
            "internet_status": c.internet_status,
            "dns_status": c.dns_status,
            "latency_ms": float(c.latency_ms) if c.latency_ms is not None else None,
            "overall_status": c.overall_status,
            "checked_at": c.checked_at,
        }
        for c in checks
    ]
