-- SQLite schema reference.
-- The FastAPI application creates these tables automatically on first start.
-- No XAMPP, MySQL Server, or Workbench is required.

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'technician',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS endpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname VARCHAR(150) NOT NULL UNIQUE,
    os VARCHAR(100), os_version VARCHAR(200), architecture VARCHAR(100), processor VARCHAR(255),
    cpu_cores INTEGER, cpu_usage NUMERIC(5,2) DEFAULT 0,
    memory_total_mb NUMERIC(12,2) DEFAULT 0, memory_usage NUMERIC(5,2) DEFAULT 0,
    disk_total_gb NUMERIC(12,2) DEFAULT 0, disk_free_gb NUMERIC(12,2) DEFAULT 0, disk_usage NUMERIC(5,2) DEFAULT 0,
    ip_address VARCHAR(100), mac_address VARCHAR(100), uptime_seconds INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'healthy', last_seen DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS health_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint_id INTEGER NOT NULL REFERENCES endpoints(id) ON DELETE CASCADE,
    cpu_usage NUMERIC(5,2) DEFAULT 0, memory_usage NUMERIC(5,2) DEFAULT 0, disk_usage NUMERIC(5,2) DEFAULT 0,
    internet_status VARCHAR(20) DEFAULT 'unknown', dns_status VARCHAR(20) DEFAULT 'unknown',
    latency_ms NUMERIC(10,2), overall_status VARCHAR(20) DEFAULT 'healthy', checked_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS support_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_number VARCHAR(30) NOT NULL UNIQUE,
    endpoint_id INTEGER REFERENCES endpoints(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL, description TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'Other', priority VARCHAR(20) DEFAULT 'Medium', status VARCHAR(30) DEFAULT 'Open',
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    resolution TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, resolved_at DATETIME
);

CREATE TABLE IF NOT EXISTS troubleshooting_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL REFERENCES support_tickets(id) ON DELETE CASCADE,
    step INTEGER NOT NULL, action_taken TEXT NOT NULL, result TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
