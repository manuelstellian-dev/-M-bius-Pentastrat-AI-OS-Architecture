# Runbook: High p99 Latency Incident

## Symptoms
- p99 latency exceeds SLA threshold (>120ms for MVP)
- User complaints about slow responses
- Grafana alerts triggered

## Investigation Steps

### 1. Check Current Metrics
```bash
# Access Grafana
open http://localhost:3000

# Check Prometheus directly
curl http://localhost:9090/api/v1/query?query=tail_p99
```

### 2. Verify System State
```bash
# Check Arbiter decision
curl -X POST http://localhost:8001/decide_mode \
  -H 'Content-Type: application/json' \
  -d '{"theta": 0.65}'

# Check all services health
for port in 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010 8011 8080; do
  echo "Port $port:"
  curl -s http://localhost:$port/health
done
```

### 3. Check Explain Metrics
```bash
curl -X POST http://localhost:8080/metrics \
  -H 'Content-Type: application/json' \
  -d '{}'
```

## Remediation Actions

### Immediate Actions

1. **Increase Throttling (Λ‑Balance)**
```bash
curl -X POST http://localhost:8003/tune \
  -H 'Content-Type: application/json' \
  -d '{"lat_p99":125.0,"Lmax":100.0}'
```

2. **Reduce Entropy Rate (Λ‑Arbiter)**
- Arbiter automatically reduces entropy budget when Θ drops
- Verify: Check that entropy experiments are paused

3. **Enable Hedging (Λ‑TimeWrap)**
- TimeWrap automatically activates hedging for p99 requests
- Verify fast-path utilization is optimized

4. **Check for Drift (Λ‑Regen)**
```bash
curl -X POST http://localhost:8005/detect \
  -H 'Content-Type: application/json' \
  -d '{"signals":{"latency":125,"error_rate":0.02}}'
```

### Secondary Actions

5. **Review Recent Changes**
```bash
# Check change cards
curl http://localhost:8080/status
```

6. **Rollback Recent Canaries**
- Identify recent deployments
- Initiate rollback if correlated with latency increase

7. **Redistribute Workload**
- Move more traffic to local (lower latency)
- Reduce cloud allocation temporarily

```bash
curl -X POST http://localhost:8001/allocate \
  -H 'Content-Type: application/json' \
  -d '{
    "metrics": {
      "T1": 10.0,
      "k": 1.8,
      "P": 1.2,
      "U": 8.0,
      "theta": 0.65,
      "throughput": 200,
      "energy_eff": 0.8,
      "latency": 125,
      "risk": 0.3,
      "cost": 0.5
    },
    "constraints": {"latency_max": 100}
  }'
```

## Verification

### Check if Remediation Worked
```bash
# Monitor p99 for 5 minutes
watch -n 30 'curl -s http://localhost:8080/metrics | jq .lat_p99'
```

### Expected Results
- p99 latency drops below 100ms within 5-10 minutes
- Θ (resilience) stabilizes or increases
- No new errors introduced

## Post-Incident

### 1. Create Change Card
```bash
curl -X POST http://localhost:8080/changecard \
  -H 'Content-Type: application/json' \
  -d '{
    "who": "oncall-engineer",
    "why": "p99 latency incident response",
    "delta_k": 0.0,
    "delta_theta": 0.05,
    "roi": 0.0,
    "rollback_plan": "revert throttling settings"
  }'
```

### 2. Root Cause Analysis
```bash
curl -X POST http://localhost:8080/rootcause \
  -H 'Content-Type: application/json' \
  -d '{
    "incident_id": "inc-p99-TIMESTAMP",
    "signals": {
      "latency": 125,
      "cpu_util": 0.85,
      "error_rate": 0.02
    }
  }'
```

### 3. Document Lessons Learned
- What triggered the incident?
- What worked well in remediation?
- What needs improvement?
- Update this runbook with new findings

## Prevention

1. **Increase Monitoring Sensitivity**
   - Lower alert threshold to 100ms (from 120ms)
   - Add predictive alerts based on trend

2. **Improve Λ‑Balance Tuning**
   - Adjust PID parameters based on observed behavior
   - Implement more aggressive throttling earlier

3. **Optimize Hot Paths**
   - Profile slow endpoints
   - Apply Λ‑Optimize suggestions

4. **Capacity Planning**
   - Review resource allocation
   - Consider scaling P (parallelism)

## Escalation

If remediation doesn't work within 30 minutes:
1. Engage senior engineer
2. Consider activating kill-switch for problematic components
3. Prepare for full system rollback

## Related Runbooks
- [Drift Detection](./drift-detected.md)
- [Service Failure](./service-failure.md)
- [Resource Exhaustion](./resource-exhaustion.md)
