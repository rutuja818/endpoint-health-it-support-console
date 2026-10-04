from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Endpoint
from ..schemas import EndpointPayload
from ..services.health_service import calculate_status

router = APIRouter(prefix="/api/endpoints", tags=["Endpoints"])

def serialize(e):
    return {
        "id": e.id,
        "hostname": e.hostname,
        "os": e.os,
        "os_version": e.os_version,
        "architecture": e.architecture,
        "processor": e.processor,
        "cpu_cores": e.cpu_cores,
        "cpu_usage": float(e.cpu_usage or 0),
        "memory_total_mb": float(e.memory_total_mb or 0),
        "memory_usage": float(e.memory_usage or 0),
        "disk_total_gb": float(e.disk_total_gb or 0),
        "disk_free_gb": float(e.disk_free_gb or 0),
        "disk_usage": float(e.disk_usage or 0),
        "ip_address": e.ip_address,
        "mac_address": e.mac_address,
        "uptime_seconds": e.uptime_seconds,
        "status": e.status,
        "last_seen": e.last_seen,
    }

@router.get("")
def list_endpoints(db: Session = Depends(get_db)):
    return [serialize(e) for e in db.query(Endpoint).order_by(Endpoint.hostname).all()]

@router.get("/{endpoint_id}")
def get_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    e = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if not e:
        raise HTTPException(404, "Endpoint not found")
    return serialize(e)

@router.post("")
def upsert_endpoint(payload: EndpointPayload, db: Session = Depends(get_db)):
    e = db.query(Endpoint).filter(Endpoint.hostname == payload.hostname).first()
    if not e:
        e = Endpoint(hostname=payload.hostname)
        db.add(e)

    data = payload.model_dump()
    for key, value in data.items():
        setattr(e, key, value)

    e.status = calculate_status(payload.cpu_usage, payload.memory_usage, payload.disk_usage)
    e.last_seen = datetime.now()
    db.commit()
    db.refresh(e)
    return serialize(e)

@router.put("/{endpoint_id}")
def update_endpoint(endpoint_id: int, payload: EndpointPayload, db: Session = Depends(get_db)):
    e = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if not e:
        raise HTTPException(404, "Endpoint not found")
    for key, value in payload.model_dump().items():
        setattr(e, key, value)
    e.status = calculate_status(payload.cpu_usage, payload.memory_usage, payload.disk_usage)
    e.last_seen = datetime.now()
    db.commit()
    db.refresh(e)
    return serialize(e)
