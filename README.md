# Endpoint Health & IT Support System

A portfolio-ready endpoint monitoring and IT support platform built with:

- Python endpoint agent
- FastAPI backend
- SQLite (included with Python)
- React + Vite frontend
- Bash troubleshooting scripts

The project collects endpoint health information, stores it through REST APIs, displays endpoint inventory and health status, and provides an IT support ticket workflow.

## Important

This is a learning/portfolio project. It does not provide real Jamf Pro or Microsoft Intune management. The compliance page is a clearly labeled simulation.

## Architecture

```text
Endpoint Computer
      |
      v
Python Endpoint Agent
      |
      | REST API
      v
FastAPI Backend
      |
      v
SQLite Database
      |
      v
React Dashboard
```

## Requirements

- Python 3.10+
- Node.js 18+
- MySQL 8+
- Git
- Optional: Bash/Git Bash/WSL for scripts

## 1. Database

No database server installation is required. The backend uses SQLite by default.

When the FastAPI backend starts for the first time, it automatically:
- creates `backend/endpoint_support.db`
- creates all required tables
- inserts demo users, endpoints, tickets, and health checks

The SQL files in `database/` are reference schemas only. You do not need XAMPP, MySQL Server, or MySQL Workbench.

## 2. Backend

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` only if you want to change development settings. The default SQLite database works without any database password.

Run:

```bash
uvicorn app.main:app --reload
```

API:
`http://127.0.0.1:8000`

Swagger:
`http://127.0.0.1:8000/docs`

## 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally:

`http://localhost:5173`

## 4. Endpoint Agent

```bash
cd agent
python -m venv venv
```

Activate the environment and install:

```bash
pip install -r requirements.txt
```

Set the API URL if required:

Windows PowerShell:

```powershell
$env:API_URL="http://127.0.0.1:8000"
```

Run:

```bash
python agent.py
```

The agent collects real local system information and sends it to the backend.

## Demo account

The backend includes simple demo authentication endpoints. The seeded demo users are:

- Admin: `admin@example.com` / `admin123`
- Technician: `tech@example.com` / `tech123`

These are development/demo credentials only. Change them for any real deployment.

## Main features

- Endpoint inventory
- CPU/RAM/disk monitoring
- Internet and DNS health checks
- Endpoint status classification
- Support tickets
- Ticket priorities and status
- Troubleshooting logs
- Compliance simulation
- Dashboard statistics
- Search/filtering
- REST API
- SQLite persistence
- Bash system/network checks

## Resume project title

**Endpoint Health & IT Support System | Python, FastAPI, React, MySQL, Bash, Networking**

Use resume claims only for features you have personally tested and can explain in an interview.
