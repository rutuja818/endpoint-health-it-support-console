#!/usr/bin/env bash
echo "System Health Report"
echo "--------------------"
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p 2>/dev/null || uptime)"
echo
./check_disk.sh
echo
./check_network.sh
