def calculate_status(cpu: float, memory: float, disk: float) -> str:
    values = [cpu, memory, disk]
    if any(v > 90 for v in values):
        return "critical"
    if any(v >= 70 for v in values):
        return "warning"
    return "healthy"
