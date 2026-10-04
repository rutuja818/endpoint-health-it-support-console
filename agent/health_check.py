def calculate_status(cpu, memory, disk):
    values = [cpu, memory, disk]
    if any(value > 90 for value in values):
        return "critical"
    if any(value >= 70 for value in values):
        return "warning"
    return "healthy"
