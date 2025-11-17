"""
Λ‑Explain: Observability & Causality Engine
Telemetry, tracing, root cause analysis, change cards
Maps decisions to U and SLA
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from services.common.server import create_app, run
import datetime

app = create_app("explain")


class ChangeCard(BaseModel):
    """Change card for tracking modifications"""
    who: str
    why: str
    delta_k: float = 0.0
    delta_theta: float = 0.0
    roi: float = 0.0
    rollback_plan: str = "available"
    canary_scope: str = "2%"


class ChangeCardResp(BaseModel):
    """Response after creating change card"""
    card_id: str
    timestamp: str


class MetricsReq(BaseModel):
    """Request for system metrics"""
    include: Optional[List[str]] = None


class MetricsResp(BaseModel):
    """Response with system metrics"""
    T1: float
    k: float
    P: float
    U: float
    theta: float
    kP: float
    lat_p99: float
    mttr: float
    mtbf: float
    energy: float
    risk: float


class TraceReq(BaseModel):
    """Request for trace information"""
    trace_id: str


class TraceResp(BaseModel):
    """Response with trace graph"""
    trace_id: str
    spans: List[Dict[str, Any]]
    duration_ms: float
    service_path: List[str]


class RootCauseReq(BaseModel):
    """Request for root cause analysis"""
    incident_id: str
    signals: Dict[str, Any]


class RootCauseResp(BaseModel):
    """Response with root cause"""
    incident_id: str
    likely_causes: List[Dict[str, Any]]
    suggested_actions: List[str]


# Storage
CHANGE_CARDS = []
TRACES = {}


@app.post("/changecard", response_model=ChangeCardResp)
def create_changecard(card: ChangeCard):
    """
    Create change card for tracking
    
    Change cards document:
    - Who made the change
    - Why it was made
    - Expected Δk, ΔΘ, ROI
    - Safety checks passed
    - Rollback plan
    - Canary scope
    """
    import hashlib
    
    timestamp = datetime.datetime.utcnow().isoformat()
    card_data = f"{card.who}:{card.why}:{timestamp}".encode()
    card_id = f"cc-{hashlib.md5(card_data).hexdigest()[:12]}"
    
    record = card.model_dump()
    record["card_id"] = card_id
    record["timestamp"] = timestamp
    
    CHANGE_CARDS.append(record)
    
    return ChangeCardResp(
        card_id=card_id,
        timestamp=timestamp
    )


@app.post("/metrics", response_model=MetricsResp)
def get_metrics(req: MetricsReq):
    """
    Get current system metrics
    
    Metrics tracked:
    - T1: Initial cost
    - k: Efficiency rate
    - P: Parallelism
    - U: Utility
    - Θ: Resilience
    - k·P: Combined efficiency
    - lat_p99: Tail latency
    - MTTR, MTBF: Reliability
    - Energy, Risk
    """
    import random
    
    # Simulate current metrics
    # In production, these come from actual monitoring
    T1 = 10.0
    k = 1.8
    P = 1.2
    U = 8.5
    theta = 0.78
    
    return MetricsResp(
        T1=T1,
        k=k,
        P=P,
        U=U,
        theta=theta,
        kP=k * P,
        lat_p99=random.uniform(80, 120),
        mttr=random.uniform(5, 15),
        mtbf=random.uniform(500, 1000),
        energy=random.uniform(0.6, 0.9),
        risk=random.uniform(0.1, 0.3)
    )


@app.post("/trace", response_model=TraceResp)
def get_trace(req: TraceReq):
    """
    Get distributed trace
    
    Traces show:
    - Service path
    - Timing breakdown
    - Error propagation
    - Resource usage
    """
    # Check if trace exists
    if req.trace_id in TRACES:
        return TraceResp(**TRACES[req.trace_id])
    
    # Generate sample trace
    trace = TraceResp(
        trace_id=req.trace_id,
        spans=[
            {"service": "arbiter", "duration_ms": 5.2, "status": "ok"},
            {"service": "timewrap", "duration_ms": 12.8, "status": "ok"},
            {"service": "balance", "duration_ms": 3.5, "status": "ok"},
        ],
        duration_ms=21.5,
        service_path=["arbiter", "timewrap", "balance"]
    )
    
    TRACES[req.trace_id] = trace.model_dump()
    return trace


@app.post("/rootcause", response_model=RootCauseResp)
def analyze_root_cause(req: RootCauseReq):
    """
    Analyze root cause of incident
    
    Uses:
    - Causal scoring on event graph
    - Pattern matching
    - Historical correlation
    
    Suggests:
    - Regen actions
    - Optimize transformations
    - Balance adjustments
    """
    # Simple heuristic root cause analysis
    causes = []
    actions = []
    
    # Check for latency issues
    if "latency" in req.signals and req.signals["latency"] > 100:
        causes.append({
            "cause": "High latency detected",
            "confidence": 0.85,
            "component": "network"
        })
        actions.append("Activate Λ‑Balance throttling")
        actions.append("Enable Λ‑TimeWrap hedging")
    
    # Check for error rate
    if "error_rate" in req.signals and req.signals["error_rate"] > 0.05:
        causes.append({
            "cause": "Elevated error rate",
            "confidence": 0.90,
            "component": "inference"
        })
        actions.append("Trigger Λ‑Regen detection")
        actions.append("Quarantine affected models")
    
    # Check for resource exhaustion
    if "cpu_util" in req.signals and req.signals["cpu_util"] > 0.9:
        causes.append({
            "cause": "Resource exhaustion",
            "confidence": 0.80,
            "component": "compute"
        })
        actions.append("Apply Λ‑Optimize scaling")
        actions.append("Redistribute workload (cloud/edge)")
    
    return RootCauseResp(
        incident_id=req.incident_id,
        likely_causes=causes,
        suggested_actions=actions
    )


@app.get("/status")
def get_status():
    """Get Explain status"""
    return {
        "service": "Λ‑Explain",
        "description": "Observability & Causality Engine",
        "capabilities": [
            "Change card tracking",
            "Metrics collection",
            "Distributed tracing",
            "Root cause analysis",
            "Causal graph analysis"
        ],
        "change_cards_created": len(CHANGE_CARDS),
        "traces_stored": len(TRACES)
    }


if __name__ == "__main__":
    run(app, 8080)
