import socket
import time

def check_network():
    internet = "fail"
    dns = "fail"
    latency = None

    try:
        start = time.perf_counter()
        socket.gethostbyname("example.com")
        latency = round((time.perf_counter() - start) * 1000, 2)
        dns = "pass"
        internet = "pass"
    except Exception:
        pass

    return {
        "internet_status": internet,
        "dns_status": dns,
        "latency_ms": latency
    }
