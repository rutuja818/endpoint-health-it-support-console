# Architecture

## Components

### Endpoint Agent
Runs on a workstation and collects system information using Python and psutil.

### FastAPI
Receives endpoint telemetry, performs validation and exposes endpoint/ticket APIs.

### MySQL
Stores endpoint inventory, health checks, tickets and troubleshooting logs.

### React
Provides the IT technician dashboard.

## Data flow

1. Agent reads local system metrics.
2. Agent performs basic network checks.
3. Agent sends telemetry to `/api/endpoints`.
4. Backend calculates endpoint status.
5. Backend stores the endpoint in MySQL.
6. Agent submits a health-check record.
7. React dashboard reads the stored data.
8. Technician can create and resolve support tickets.
