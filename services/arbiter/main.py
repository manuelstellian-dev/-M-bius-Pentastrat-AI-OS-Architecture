"""
Λ‑Arbiter Core: Meta-decisional cortex
Monitors global state (Regen, Optimize, Balance, Entropy)
Decides active regime and allocates resources
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional
from services.common.server import create_app, run
import math

app = create_app("arbiter")


class DecideReq(BaseModel):
    """Request to decide operation mode based on resilience"""
    theta: float
    low: float = 0.55
    high: float = 0.80


class DecideResp(BaseModel):
    """Response with decided state"""
    state: int  # +1 wrap, 0 steady, -1 unwrap
    mode_name: str


class Metrics(BaseModel):
    """System metrics for decision making"""
    T1: float  # Initial cost
    k: float  # Efficiency rate
    P: float  # Parallelism
    U: float  # Utility
    theta: float  # Resilience
    throughput: float = 0.0
    energy_eff: float = 0.0
    latency: float = 0.0
    risk: float = 0.0
    cost: float = 0.0
    

class UtilityWeights(BaseModel):
    """Weights for utility function"""
    wT: float = 0.35  # Throughput weight
    wE: float = 0.15  # Energy efficiency weight
    wL: float = 0.30  # Latency weight (negative)
    wR: float = 0.15  # Risk weight (negative)
    wC: float = 0.05  # Cost weight (negative)


class AllocateReq(BaseModel):
    """Request to allocate resources"""
    metrics: Metrics
    constraints: Dict[str, float]
    weights: Optional[UtilityWeights] = None


class AllocateResp(BaseModel):
    """Response with resource allocation plan"""
    P_local: float
    P_cloud: float
    P_edge: float
    placement: Dict[str, str]
    utility: float


@app.post("/decide_mode", response_model=DecideResp)
def decide_mode(req: DecideReq):
    """
    Decide operational mode based on resilience (Θ)
    
    Formula:
    - Θ ≥ θ_high → Wrap mode (+1) - compression/regeneration
    - θ_low ≤ Θ < θ_high → Steady mode (0) - maintain equilibrium
    - Θ < θ_low → Unwrap mode (-1) - expansion/stress testing
    """
    if req.theta >= req.high:
        return {"state": 1, "mode_name": "Λ‑Wrap (Compression)"}
    elif req.theta >= req.low:
        return {"state": 0, "mode_name": "Λ‑Steady (Equilibrium)"}
    else:
        return {"state": -1, "mode_name": "Λ‑Unwrap (Expansion)"}


@app.post("/utility", response_model=Dict[str, float])
def calculate_utility(metrics: Metrics, weights: Optional[UtilityWeights] = None):
    """
    Calculate utility function:
    U = w₁·Throughput + w₂·EnergyEfficiency − w₃·Latency − w₄·Risk − w₅·Cost
    
    Subject to constraints:
    - Latency_p99 ≤ Lmax
    - Error_rate ≤ Emax
    - MTTR ≤ Rmax
    """
    if weights is None:
        weights = UtilityWeights()
    
    utility = (
        weights.wT * metrics.throughput +
        weights.wE * metrics.energy_eff -
        weights.wL * metrics.latency -
        weights.wR * metrics.risk -
        weights.wC * metrics.cost
    )
    
    return {
        "utility": utility,
        "throughput_contribution": weights.wT * metrics.throughput,
        "energy_contribution": weights.wE * metrics.energy_eff,
        "latency_penalty": weights.wL * metrics.latency,
        "risk_penalty": weights.wR * metrics.risk,
        "cost_penalty": weights.wC * metrics.cost
    }


@app.post("/allocate", response_model=AllocateResp)
def allocate_resources(req: AllocateReq):
    """
    Allocate resources across local, cloud, and edge
    
    Heuristic MPC:
    - minimize L + λC·Cost + λR·Risk
    - P_eff = P_local + P_cloud − Overhead_sync
    
    Rules:
    - Low-latency critical → local
    - Heavy training → cloud
    - Personalization/private → edge with distillation
    """
    weights = req.weights or UtilityWeights()
    m = req.metrics
    
    # Simple heuristic allocation based on latency requirements
    latency_threshold = req.constraints.get("latency_max", 100.0)
    
    if m.latency < latency_threshold * 0.5:
        # Low latency requirement - prefer local
        P_local = m.P * 0.7
        P_cloud = m.P * 0.2
        P_edge = m.P * 0.1
        placement = {
            "inference": "local",
            "training": "cloud",
            "personalization": "edge"
        }
    elif m.latency < latency_threshold:
        # Moderate latency - balanced
        P_local = m.P * 0.4
        P_cloud = m.P * 0.4
        P_edge = m.P * 0.2
        placement = {
            "inference": "local+cloud",
            "training": "cloud",
            "personalization": "edge"
        }
    else:
        # High latency tolerance - prefer cloud
        P_local = m.P * 0.2
        P_cloud = m.P * 0.6
        P_edge = m.P * 0.2
        placement = {
            "inference": "cloud",
            "training": "cloud",
            "personalization": "edge"
        }
    
    # Calculate utility with allocation
    overhead_sync = 0.05 * (P_cloud + P_edge)
    P_effective = P_local + P_cloud + P_edge - overhead_sync
    
    utility = (
        weights.wT * m.throughput * (P_effective / m.P) +
        weights.wE * m.energy_eff -
        weights.wL * m.latency -
        weights.wR * m.risk -
        weights.wC * m.cost
    )
    
    return AllocateResp(
        P_local=P_local,
        P_cloud=P_cloud,
        P_edge=P_edge,
        placement=placement,
        utility=utility
    )


@app.get("/status")
def get_status():
    """Get Arbiter status"""
    return {
        "service": "Λ‑Arbiter Core",
        "description": "Meta-decisional cortex for Λ‑Möbius Pentastrat",
        "capabilities": [
            "Mode decision (Wrap/Steady/Unwrap)",
            "Utility calculation",
            "Resource allocation (local/cloud/edge)",
            "Policy enforcement"
        ]
    }


if __name__ == "__main__":
    run(app, 8001)
