#!/usr/bin/env bash
echo "Network Health"
echo "--------------"
if getent hosts example.com >/dev/null 2>&1; then
  echo "DNS: PASS"
else
  echo "DNS: FAIL"
fi

if curl -Is --max-time 5 https://example.com >/dev/null 2>&1; then
  echo "Internet: PASS"
else
  echo "Internet: FAIL"
fi
