#!/usr/bin/env bash
# System validation script for Λ‑Möbius Pentastrat AI‑OS

set -e

echo "========================================="
echo "Λ‑Möbius System Validation"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "Testing $name... "
    
    if response=$(curl -s --max-time 5 "$url" 2>&1); then
        if echo "$response" | grep -q "$expected"; then
            echo -e "${GREEN}✓ PASS${NC}"
            ((PASSED++))
            return 0
        else
            echo -e "${RED}✗ FAIL${NC} (unexpected response)"
            echo "  Response: $response"
            ((FAILED++))
            return 1
        fi
    else
        echo -e "${RED}✗ FAIL${NC} (connection error)"
        ((FAILED++))
        return 1
    fi
}

# Function to test POST endpoint
test_post() {
    local name=$1
    local url=$2
    local data=$3
    local expected=$4
    
    echo -n "Testing $name... "
    
    if response=$(curl -s --max-time 5 -X POST -H 'Content-Type: application/json' -d "$data" "$url" 2>&1); then
        if echo "$response" | grep -q "$expected"; then
            echo -e "${GREEN}✓ PASS${NC}"
            ((PASSED++))
            return 0
        else
            echo -e "${RED}✗ FAIL${NC} (unexpected response)"
            echo "  Response: $response"
            ((FAILED++))
            return 1
        fi
    else
        echo -e "${RED}✗ FAIL${NC} (connection error)"
        ((FAILED++))
        return 1
    fi
}

echo "=== Health Checks ==="
test_endpoint "Arbiter health" "http://localhost:8001/health" "ok"
test_endpoint "TimeWrap health" "http://localhost:8002/health" "ok"
test_endpoint "Balance health" "http://localhost:8003/health" "ok"
test_endpoint "Optimize health" "http://localhost:8004/health" "ok"
test_endpoint "Regen health" "http://localhost:8005/health" "ok"
test_endpoint "Entropy health" "http://localhost:8006/health" "ok"
test_endpoint "Memory health" "http://localhost:8007/health" "ok"
test_endpoint "Safety health" "http://localhost:8008/health" "ok"
test_endpoint "Econ health" "http://localhost:8009/health" "ok"
test_endpoint "SecureIO health" "http://localhost:8010/health" "ok"
test_endpoint "Planner health" "http://localhost:8011/health" "ok"
test_endpoint "Explain health" "http://localhost:8080/health" "ok"

echo ""
echo "=== Functional Tests ==="

test_post "Arbiter Wrap decision" \
    "http://localhost:8001/decide_mode" \
    '{"theta":0.85}' \
    '"state":1'

test_post "Arbiter Steady decision" \
    "http://localhost:8001/decide_mode" \
    '{"theta":0.65}' \
    '"state":0'

test_post "TimeWrap Λ calculation" \
    "http://localhost:8002/lambda_time" \
    '{"mode":1,"T1":10,"k":2,"P":1.2,"U":8}' \
    '"value"'

test_post "Balance PID tuning" \
    "http://localhost:8003/tune" \
    '{"lat_p99":95.5,"Lmax":100.0}' \
    '"throttle"'

test_post "Optimize suggestions" \
    "http://localhost:8004/suggest" \
    '{"model":"test","hw":"gpu"}' \
    '"quantize"'

test_post "Regen detection" \
    "http://localhost:8005/detect" \
    '{"signals":{"test":1.0}}' \
    '"anomalies"'

test_post "Entropy experiment" \
    "http://localhost:8006/experiment" \
    '{"hypothesis":"test","budget":0.02}' \
    '"delta_k"'

test_post "Memory write" \
    "http://localhost:8007/write" \
    '{"type":"test","payload":{"data":"test"},"tags":["test"]}' \
    '"id"'

test_post "Safety verification" \
    "http://localhost:8008/verify" \
    '{"attested":true,"canary":true,"rollback_plan":true}' \
    '"pass"'

test_post "Econ ROI calculation" \
    "http://localhost:8009/roi" \
    '{"deltaU":10,"deltaCost":2,"deltaRisk":1,"invest":5}' \
    '"roi"'

test_post "SecureIO ingress" \
    "http://localhost:8010/ingress" \
    '{"payload":{"test":"data"},"source":"local"}' \
    '"ok"'

test_post "Planner decompose" \
    "http://localhost:8011/decompose" \
    '{"task":{"id":"test","description":"test task","priority":1}}' \
    '"plan"'

test_post "Explain metrics" \
    "http://localhost:8080/metrics" \
    '{}' \
    '"T1"'

echo ""
echo "=== Integration Tests ==="

echo -n "Testing Arbiter → TimeWrap flow... "
# Get Arbiter decision
STATE=$(curl -s -X POST http://localhost:8001/decide_mode \
    -H 'Content-Type: application/json' \
    -d '{"theta":0.85}' | grep -o '"state":[0-9]*' | cut -d':' -f2)

if [ "$STATE" = "1" ]; then
    # Use state in TimeWrap
    LAMBDA=$(curl -s -X POST http://localhost:8002/lambda_time \
        -H 'Content-Type: application/json' \
        -d "{\"mode\":$STATE,\"T1\":10,\"k\":2,\"P\":1.2,\"U\":8}" | grep -o '"value":[0-9.]*')
    
    if [ -n "$LAMBDA" ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} (no lambda value)"
        ((FAILED++))
    fi
else
    echo -e "${RED}✗ FAIL${NC} (wrong state)"
    ((FAILED++))
fi

echo ""
echo "=== Observability Stack ==="
test_endpoint "Prometheus" "http://localhost:9090/-/healthy" "Prometheus"
test_endpoint "Grafana" "http://localhost:3000/api/health" "ok"

echo ""
echo "========================================="
echo "Summary"
echo "========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
