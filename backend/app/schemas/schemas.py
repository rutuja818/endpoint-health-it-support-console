from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class EndpointPayload(BaseModel):
    hostname: str
    os: Optional[str] = None
    os_version: Optional[str] = None
    architecture: Optional[str] = None
    processor: Optional[str] = None
    cpu_cores: Optional[int] = None
    cpu_usage: float = 0
    memory_total_mb: float = 0
    memory_usage: float = 0
    disk_total_gb: float = 0
    disk_free_gb: float = 0
    disk_usage: float = 0
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    uptime_seconds: int = 0

class EndpointResponse(EndpointPayload):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    last_seen: Optional[datetime] = None
    created_at: Optional[datetime] = None

class HealthCheckCreate(BaseModel):
    endpoint_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    internet_status: str = "unknown"
    dns_status: str = "unknown"
    latency_ms: Optional[float] = None

class TicketCreate(BaseModel):
    endpoint_id: Optional[int] = None
    title: str
    description: str
    category: str = "Other"
    priority: str = "Medium"
    assigned_to: Optional[int] = None

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None
    resolution: Optional[str] = None

class TicketResponse(TicketCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    ticket_number: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    role: str
    name: str
