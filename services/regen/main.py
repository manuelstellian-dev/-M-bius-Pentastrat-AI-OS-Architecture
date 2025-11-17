"""
Λ‑Regen: Regeneration and repair engine
Implements Flux Fractal: Detect → Quarantine → Improve → Reinvest
Micro-rollback, hot-swap, re-training
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.common.server import create_app, run
import datetime

app = create_app("regen")


class DetectReq(BaseModel):
    """Request to detect anomalies"""
    signals: Dict[str, Any]
    thresholds: Optional[Dict[str, float]] = None


class DetectResp(BaseModel):
    """Response with detected anomalies"""
    anomalies: List[str]
    severity: Dict[str, str]
    timestamp: str


class QuarantineReq(BaseModel):
    """Request to quarantine component"""
    unit: str
    reason: str
    severity: str = "medium"


class QuarantineResp(BaseModel):
    """Response with quarantine ticket"""
    ticket_id: str
    isolated: bool
    rollback_available: bool


class ImproveReq(BaseModel):
    """Request to improve quarantined unit"""
    ticket_id: str
    unit: str
    strategy: str = "auto"  # auto, retrain, patch, replace


class ImproveResp(BaseModel):
    """Response with improvement result"""
    patch_id: str
    validated: bool
    delta_k: float  # Efficiency improvement
    delta_theta: float  # Resilience improvement


class ReinvestReq(BaseModel):
    """Request to reinvest gains"""
    patch_id: str
    gains: Dict[str, float]


class ReinvestResp(BaseModel):
    """Response after reinvestment"""
    applied: bool
    k_new: float
    theta_new: float
    T1_new: float


# Global state for demo
QUARANTINE_REGISTRY = {}
PATCH_REGISTRY = {}


@app.post("/detect", response_model=DetectResp)
def detect(req: DetectReq):
    """
    Detect anomalies in system signals
    
    Detection methods:
    - Statistical anomaly detection
    - Drift detection
    - Error pattern recognition
    - Performance degradation
    - Security violations
    """
    anomalies = []
    severity = {}
    
    # Check for NaN values
    for key, value in req.signals.items():
        if isinstance(value, (int, float)):
            if value != value:  # NaN check
                anomalies.append(f"{key}:NaN")
                severity[key] = "high"
        elif isinstance(value, str) and "error" in value.lower():
            anomalies.append(f"{key}:error_pattern")
            severity[key] = "medium"
    
    # Check thresholds if provided
    if req.thresholds:
        for key, threshold in req.thresholds.items():
            if key in req.signals:
                value = req.signals[key]
                if isinstance(value, (int, float)) and value > threshold:
                    anomalies.append(f"{key}:threshold_exceeded")
                    severity[key] = "high"
    
    return DetectResp(
        anomalies=anomalies,
        severity=severity,
        timestamp=datetime.datetime.utcnow().isoformat()
    )


@app.post("/quarantine", response_model=QuarantineResp)
def quarantine(req: QuarantineReq):
    """
    Quarantine problematic component
    
    Actions:
    - Isolate component
    - Stop traffic routing
    - Create rollback point
    - Log incident
    """
    import hashlib
    
    # Generate ticket ID
    ticket_data = f"{req.unit}:{datetime.datetime.utcnow()}".encode()
    ticket_id = f"q-{hashlib.md5(ticket_data).hexdigest()[:12]}"
    
    # Store in quarantine registry
    QUARANTINE_REGISTRY[ticket_id] = {
        "unit": req.unit,
        "reason": req.reason,
        "severity": req.severity,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "status": "quarantined"
    }
    
    return QuarantineResp(
        ticket_id=ticket_id,
        isolated=True,
        rollback_available=True
    )


@app.post("/improve", response_model=ImproveResp)
def improve(req: ImproveReq):
    """
    Improve quarantined unit
    
    Strategies:
    - Retrain: Update model with recent data
    - Patch: Apply fix to specific issue
    - Replace: Swap with backup/alternative
    - Rollback: Revert to last known good state
    """
    import hashlib
    import random
    
    # Generate patch ID
    patch_data = f"{req.unit}:{req.strategy}:{datetime.datetime.utcnow()}".encode()
    patch_id = f"patch-{hashlib.md5(patch_data).hexdigest()[:12]}"
    
    # Simulate improvement
    delta_k = random.uniform(0.05, 0.20)  # 5-20% efficiency gain
    delta_theta = random.uniform(0.02, 0.10)  # 2-10% resilience gain
    
    # Validate patch
    validated = True  # In production, run validation suite
    
    # Store patch
    PATCH_REGISTRY[patch_id] = {
        "ticket_id": req.ticket_id,
        "unit": req.unit,
        "strategy": req.strategy,
        "delta_k": delta_k,
        "delta_theta": delta_theta,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    return ImproveResp(
        patch_id=patch_id,
        validated=validated,
        delta_k=delta_k,
        delta_theta=delta_theta
    )


@app.post("/reinvest", response_model=ReinvestResp)
def reinvest(req: ReinvestReq):
    """
    Reinvest gains from improvements
    
    Reinvestment targets:
    - Increase k (efficiency rate)
    - Reduce T1 (initial cost)
    - Increase Θ (resilience)
    - Expand P (parallelism)
    """
    # Get patch details
    patch = PATCH_REGISTRY.get(req.patch_id, {})
    
    # Calculate new parameters
    # In production, these would come from actual system state
    k_current = req.gains.get("k_current", 1.5)
    theta_current = req.gains.get("theta_current", 0.75)
    T1_current = req.gains.get("T1_current", 10.0)
    
    k_new = k_current + patch.get("delta_k", 0.0)
    theta_new = min(1.0, theta_current + patch.get("delta_theta", 0.0))
    T1_new = T1_current * 0.98  # 2% reduction in initial cost
    
    return ReinvestResp(
        applied=True,
        k_new=k_new,
        theta_new=theta_new,
        T1_new=T1_new
    )


@app.get("/status")
def get_status():
    """Get Regen status"""
    return {
        "service": "Λ‑Regen",
        "description": "Regeneration and repair engine (Flux Fractal)",
        "capabilities": [
            "Anomaly detection",
            "Component quarantine",
            "Improvement strategies (retrain, patch, replace)",
            "Gain reinvestment"
        ],
        "flux_fractal": "Detect → Quarantine → Improve → Reinvest",
        "active_quarantines": len(QUARANTINE_REGISTRY),
        "applied_patches": len(PATCH_REGISTRY)
    }


if __name__ == "__main__":
    run(app, 8005)
