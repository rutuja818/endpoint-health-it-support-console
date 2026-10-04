from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, BigInteger, ForeignKey, Enum
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("admin", "technician"), default="technician", nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Endpoint(Base):
    __tablename__ = "endpoints"
    id = Column(Integer, primary_key=True)
    hostname = Column(String(150), unique=True, nullable=False)
    os = Column(String(100))
    os_version = Column(String(200))
    architecture = Column(String(100))
    processor = Column(String(255))
    cpu_cores = Column(Integer)
    cpu_usage = Column(Numeric(5,2), default=0)
    memory_total_mb = Column(Numeric(12,2), default=0)
    memory_usage = Column(Numeric(5,2), default=0)
    disk_total_gb = Column(Numeric(12,2), default=0)
    disk_free_gb = Column(Numeric(12,2), default=0)
    disk_usage = Column(Numeric(5,2), default=0)
    ip_address = Column(String(100))
    mac_address = Column(String(100))
    uptime_seconds = Column(BigInteger, default=0)
    status = Column(Enum("healthy","warning","critical","offline"), default="healthy")
    last_seen = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(Integer, primary_key=True)
    endpoint_id = Column(Integer, ForeignKey("endpoints.id", ondelete="CASCADE"), nullable=False)
    cpu_usage = Column(Numeric(5,2), default=0)
    memory_usage = Column(Numeric(5,2), default=0)
    disk_usage = Column(Numeric(5,2), default=0)
    internet_status = Column(Enum("pass","fail","unknown"), default="unknown")
    dns_status = Column(Enum("pass","fail","unknown"), default="unknown")
    latency_ms = Column(Numeric(10,2))
    overall_status = Column(Enum("healthy","warning","critical"), default="healthy")
    checked_at = Column(DateTime, server_default=func.now())

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True)
    ticket_number = Column(String(30), unique=True, nullable=False)
    endpoint_id = Column(Integer, ForeignKey("endpoints.id", ondelete="SET NULL"))
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum("Network","Hardware","Software","Operating System","Application","Security","Performance","Other"), default="Other")
    priority = Column(Enum("Low","Medium","High","Critical"), default="Medium")
    status = Column(Enum("Open","In Progress","Resolved","Closed"), default="Open")
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    resolution = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime)

class TroubleshootingLog(Base):
    __tablename__ = "troubleshooting_logs"
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False)
    step = Column(Integer, nullable=False)
    action_taken = Column(Text, nullable=False)
    result = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
