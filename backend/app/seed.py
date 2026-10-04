from datetime import datetime
from .database import Base, engine, SessionLocal
from .models import User, Endpoint, SupportTicket, HealthCheck


def init_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            db.add_all([
                User(name="System Admin", email="admin@example.com", password_hash="demo", role="admin"),
                User(name="IT Technician", email="tech@example.com", password_hash="demo", role="technician"),
            ])
            db.commit()

        if db.query(Endpoint).count() == 0:
            endpoints = [
                Endpoint(hostname="DEMO-WIN-01", os="Windows", os_version="Windows 11", architecture="x86_64",
                         processor="Demo Intel Processor", cpu_cores=8, cpu_usage=24.50, memory_total_mb=16384,
                         memory_usage=58.20, disk_total_gb=512, disk_free_gb=181, disk_usage=64.65,
                         ip_address="192.168.1.21", mac_address="00:11:22:33:44:55", uptime_seconds=14400,
                         status="healthy", last_seen=datetime.now()),
                Endpoint(hostname="DEMO-LINUX-01", os="Linux", os_version="Ubuntu 24.04", architecture="x86_64",
                         processor="Demo AMD Processor", cpu_cores=8, cpu_usage=78.20, memory_total_mb=8192,
                         memory_usage=82.10, disk_total_gb=256, disk_free_gb=38, disk_usage=85.16,
                         ip_address="192.168.1.22", mac_address="00:11:22:33:44:66", uptime_seconds=28800,
                         status="warning", last_seen=datetime.now()),
                Endpoint(hostname="DEMO-WIN-02", os="Windows", os_version="Windows 10", architecture="x86_64",
                         processor="Demo Intel Processor", cpu_cores=4, cpu_usage=91.10, memory_total_mb=8192,
                         memory_usage=93.40, disk_total_gb=256, disk_free_gb=12, disk_usage=95.31,
                         ip_address="192.168.1.23", mac_address="00:11:22:33:44:77", uptime_seconds=7200,
                         status="critical", last_seen=datetime.now()),
            ]
            db.add_all(endpoints)
            db.commit()

        if db.query(SupportTicket).count() == 0:
            tech = db.query(User).filter(User.email == "tech@example.com").first()
            win1 = db.query(Endpoint).filter(Endpoint.hostname == "DEMO-WIN-01").first()
            win2 = db.query(Endpoint).filter(Endpoint.hostname == "DEMO-WIN-02").first()
            db.add_all([
                SupportTicket(ticket_number="INC-1001", endpoint_id=win1.id, title="Internet connectivity issue",
                              description="User reports intermittent internet connectivity.", category="Network",
                              priority="High", status="In Progress", assigned_to=tech.id),
                SupportTicket(ticket_number="INC-1002", endpoint_id=win2.id, title="Low disk space",
                              description="Endpoint has less than 10 percent free disk space.", category="Performance",
                              priority="Critical", status="Open", assigned_to=tech.id),
            ])
            db.commit()

        if db.query(HealthCheck).count() == 0:
            for e in db.query(Endpoint).all():
                db.add(HealthCheck(endpoint_id=e.id, cpu_usage=float(e.cpu_usage or 0),
                                   memory_usage=float(e.memory_usage or 0), disk_usage=float(e.disk_usage or 0),
                                   internet_status="pass", dns_status="pass", latency_ms=24.5,
                                   overall_status=e.status))
            db.commit()
    finally:
        db.close()
