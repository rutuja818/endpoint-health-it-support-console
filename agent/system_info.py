import platform
import socket
import uuid
import psutil

def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "127.0.0.1"

def get_mac_address():
    try:
        mac = uuid.getnode()
        return ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
    except Exception:
        return "unknown"

def get_system_info():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot_time = psutil.boot_time()

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor() or platform.uname().processor,
        "cpu_cores": psutil.cpu_count(logical=True) or 0,
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_total_mb": round(memory.total / (1024 * 1024), 2),
        "memory_usage": memory.percent,
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "disk_usage": disk.percent,
        "ip_address": get_ip_address(),
        "mac_address": get_mac_address(),
        "uptime_seconds": int(__import__("time").time() - boot_time),
    }
