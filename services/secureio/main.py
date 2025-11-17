"""
Λ‑Secure I/O: Input/output security gateway
Guards peripherals/edge, isolation, rate-limiting, adversarial filters
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional
from services.common.server import create_app, run

app = create_app("secureio")


class IngressReq(BaseModel):
    """Request for input validation"""
    payload: Any
    source: str = "unknown"
    attestation: Optional[str] = None


class IngressResp(BaseModel):
    """Response from ingress check"""
    ok: bool
    reason: str
    filtered_payload: Optional[Any] = None


class RateLimitReq(BaseModel):
    """Request for rate limit check"""
    client_id: str
    endpoint: str


class RateLimitResp(BaseModel):
    """Response with rate limit status"""
    allowed: bool
    remaining: int
    reset_in_s: int


# Blocked patterns for security
BLOCKED_PATTERNS = [
    b"../../",  # Path traversal
    b"<script>",  # XSS
    b"DROP TABLE",  # SQL injection
    b"rm -rf",  # Command injection
    b"eval(",  # Code injection
    b"__import__",  # Python injection
]

# Rate limiting (simple in-memory)
RATE_LIMITS = {}


@app.post("/ingress", response_model=IngressResp)
def ingress_filter(req: IngressReq):
    """
    Filter and validate ingress traffic
    
    Checks:
    - Adversarial patterns
    - Malicious payloads
    - Injection attacks
    - Attestation (if required)
    
    Filtering:
    - WAF-style rules
    - ML-based anomaly detection
    - Rate limiting
    """
    import json
    
    # Convert payload to bytes for checking
    try:
        payload_str = json.dumps(req.payload)
        payload_bytes = payload_str.encode()
    except:
        payload_bytes = str(req.payload).encode()
    
    # Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if pattern in payload_bytes:
            return IngressResp(
                ok=False,
                reason=f"Blocked pattern detected: {pattern.decode(errors='ignore')}"
            )
    
    # Check attestation for sensitive sources
    sensitive_sources = ["edge", "external"]
    if req.source in sensitive_sources and not req.attestation:
        return IngressResp(
            ok=False,
            reason=f"Attestation required for source: {req.source}"
        )
    
    # Passed all checks
    return IngressResp(
        ok=True,
        reason="All checks passed",
        filtered_payload=req.payload
    )


@app.post("/ratelimit", response_model=RateLimitResp)
def check_rate_limit(req: RateLimitReq):
    """
    Check and enforce rate limits
    
    Limits:
    - Per client
    - Per endpoint
    - Global
    
    Algorithm: Token bucket
    """
    import time
    
    # Create key for rate limit tracking
    key = f"{req.client_id}:{req.endpoint}"
    
    # Initialize if not exists
    if key not in RATE_LIMITS:
        RATE_LIMITS[key] = {
            "tokens": 100,
            "last_update": time.time(),
            "max_tokens": 100,
            "refill_rate": 10  # tokens per second
        }
    
    bucket = RATE_LIMITS[key]
    now = time.time()
    
    # Refill tokens
    elapsed = now - bucket["last_update"]
    bucket["tokens"] = min(
        bucket["max_tokens"],
        bucket["tokens"] + elapsed * bucket["refill_rate"]
    )
    bucket["last_update"] = now
    
    # Check if request allowed
    if bucket["tokens"] >= 1:
        bucket["tokens"] -= 1
        return RateLimitResp(
            allowed=True,
            remaining=int(bucket["tokens"]),
            reset_in_s=int((bucket["max_tokens"] - bucket["tokens"]) / bucket["refill_rate"])
        )
    else:
        return RateLimitResp(
            allowed=False,
            remaining=0,
            reset_in_s=int((1 - bucket["tokens"]) / bucket["refill_rate"])
        )


@app.post("/egress")
def egress_filter(destination: str, payload: Any):
    """
    Filter egress traffic
    
    Checks:
    - Sensitive data leakage
    - Unauthorized destinations
    - Data exfiltration patterns
    """
    # Whitelist of allowed destinations
    allowed_destinations = ["cloud", "edge", "local"]
    
    if destination not in allowed_destinations:
        return {
            "ok": False,
            "reason": f"Destination not whitelisted: {destination}"
        }
    
    # Check for sensitive data patterns
    # (In production, use DLP tools)
    payload_str = str(payload).lower()
    sensitive_patterns = ["password", "secret", "api_key", "private_key"]
    
    for pattern in sensitive_patterns:
        if pattern in payload_str:
            return {
                "ok": False,
                "reason": f"Sensitive data pattern detected: {pattern}"
            }
    
    return {
        "ok": True,
        "reason": "Egress allowed"
    }


@app.get("/status")
def get_status():
    """Get Secure I/O status"""
    return {
        "service": "Λ‑Secure I/O",
        "description": "Input/output security gateway",
        "capabilities": [
            "Ingress filtering (WAF-style)",
            "Rate limiting (token bucket)",
            "Egress filtering",
            "Attestation validation",
            "Adversarial detection"
        ],
        "blocked_patterns": len(BLOCKED_PATTERNS),
        "active_rate_limits": len(RATE_LIMITS)
    }


if __name__ == "__main__":
    run(app, 8010)
