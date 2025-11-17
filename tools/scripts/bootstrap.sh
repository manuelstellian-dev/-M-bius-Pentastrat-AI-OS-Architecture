#!/usr/bin/env bash
set -e

echo "========================================="
echo "Λ‑Möbius Pentastrat AI‑OS Bootstrap"
echo "========================================="
echo ""

# Start all services
echo "Starting all services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo ""
echo "Waiting for services to be ready..."
sleep 10

# Health checks
echo ""
echo "Running health checks..."
services=("arbiter:8001" "timewrap:8002" "balance:8003" "optimize:8004" "regen:8005" "entropy:8006" "memory:8007" "safety:8008" "econ:8009" "secureio:8010" "planner:8011" "explain:8080")

for service in "${services[@]}"; do
    name="${service%:*}"
    port="${service#*:}"
    echo -n "Checking $name... "
    if curl -s http://localhost:$port/health > /dev/null; then
        echo "✓ OK"
    else
        echo "✗ FAILED"
    fi
done

# Test basic functionality
echo ""
echo "========================================="
echo "Testing core functionality..."
echo "========================================="
echo ""

# Test Arbiter decision
echo "1. Testing Λ‑Arbiter mode decision..."
curl -s -X POST http://localhost:8001/decide_mode \
  -H 'Content-Type: application/json' \
  -d '{"theta": 0.82}' | python -m json.tool
echo ""

# Test TimeWrap lambda calculation
echo "2. Testing Λ‑TimeWrap calculation..."
curl -s -X POST http://localhost:8002/lambda_time \
  -H 'Content-Type: application/json' \
  -d '{"mode":1,"T1":10,"k":2,"P":1.2,"U":8}' | python -m json.tool
echo ""

# Test Balance PID tuning
echo "3. Testing Λ‑Balance PID tuning..."
curl -s -X POST http://localhost:8003/tune \
  -H 'Content-Type: application/json' \
  -d '{"lat_p99":95.5,"Lmax":100.0}' | python -m json.tool
echo ""

# Test Memory write
echo "4. Testing Λ‑Memory write..."
curl -s -X POST http://localhost:8007/write \
  -H 'Content-Type: application/json' \
  -d '{"type":"episodic","payload":{"event":"bootstrap","status":"success"},"tags":["bootstrap","test"]}' | python -m json.tool
echo ""

# Test Explain metrics
echo "5. Testing Λ‑Explain metrics..."
curl -s -X POST http://localhost:8080/metrics \
  -H 'Content-Type: application/json' \
  -d '{}' | python -m json.tool
echo ""

echo "========================================="
echo "Bootstrap complete!"
echo ""
echo "Services running:"
echo "  - Arbiter:   http://localhost:8001"
echo "  - TimeWrap:  http://localhost:8002"
echo "  - Balance:   http://localhost:8003"
echo "  - Optimize:  http://localhost:8004"
echo "  - Regen:     http://localhost:8005"
echo "  - Entropy:   http://localhost:8006"
echo "  - Memory:    http://localhost:8007"
echo "  - Safety:    http://localhost:8008"
echo "  - Econ:      http://localhost:8009"
echo "  - SecureIO:  http://localhost:8010"
echo "  - Planner:   http://localhost:8011"
echo "  - Explain:   http://localhost:8080"
echo ""
echo "Observability:"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana:    http://localhost:3000 (admin/admin)"
echo ""
echo "========================================="
