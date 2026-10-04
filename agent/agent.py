import requests
from config import API_URL
from system_info import get_system_info
from network_check import check_network
from health_check import calculate_status

def main():
    system = get_system_info()
    network = check_network()

    system["status"] = calculate_status(
        system["cpu_usage"],
        system["memory_usage"],
        system["disk_usage"]
    )

    print("Endpoint Health Report")
    print("----------------------")
    for key, value in system.items():
        print(f"{key}: {value}")

    print("\nNetwork")
    print("-------")
    print(f"Internet: {network['internet_status']}")
    print(f"DNS: {network['dns_status']}")
    print(f"Latency: {network['latency_ms']} ms")

    url = f"{API_URL}/api/endpoints"

    try:
        response = requests.post(url, json=system, timeout=10)
        response.raise_for_status()
        endpoint = response.json()
        print("\nEndpoint data sent successfully.")
        print(f"Endpoint ID: {endpoint['id']}")
        print(f"Status: {endpoint['status']}")

        health_payload = {
            "endpoint_id": endpoint["id"],
            "cpu_usage": system["cpu_usage"],
            "memory_usage": system["memory_usage"],
            "disk_usage": system["disk_usage"],
            "internet_status": network["internet_status"],
            "dns_status": network["dns_status"],
            "latency_ms": network["latency_ms"],
        }

        health_response = requests.post(
            f"{API_URL}/api/health/check",
            json=health_payload,
            timeout=10
        )
        health_response.raise_for_status()
        print("Health check saved successfully.")

    except requests.RequestException as exc:
        print(f"\nCould not connect to backend: {exc}")

if __name__ == "__main__":
    main()
