"""
Λ‑Entropy: Controlled stress and experimentation engine
A/B testing, chaos testing, adversarial training
Generates feedback data for Λ‑Flux Fractal
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional
from services.common.server import create_app, run
import random

app = create_app("entropy")


class ExperimentReq(BaseModel):
    """Request to run experiment"""
    hypothesis: str
    budget: float  # Max 5% of compute
    experiment_type: str = "ab"  # ab, chaos, adversarial


class ExperimentResp(BaseModel):
    """Response with experiment results"""
    experiment_id: str
    delta_k: float  # Efficiency delta
    delta_theta: float  # Resilience delta
    risk: str  # bounded, elevated, critical
    insights: Dict[str, Any]


class ChaosReq(BaseModel):
    """Request for chaos testing"""
    target: str  # Service or component
    action: str  # latency, failure, resource_limit
    intensity: float = 0.5  # 0.0 to 1.0
    duration_s: int = 60


class ChaosResp(BaseModel):
    """Response from chaos test"""
    test_id: str
    impact_observed: Dict[str, float]
    system_recovered: bool
    recovery_time_s: float


class AdversarialReq(BaseModel):
    """Request for adversarial training"""
    model_id: str
    attack_types: list[str]
    budget: float


class AdversarialResp(BaseModel):
    """Response from adversarial training"""
    robustness_score: float
    vulnerabilities_found: int
    patched_model_id: str


EXPERIMENTS = {}


@app.post("/experiment", response_model=ExperimentResp)
def experiment(req: ExperimentReq):
    """
    Run controlled experiment
    
    Types:
    - A/B testing: Compare variants
    - Chaos testing: Inject failures
    - Adversarial: Test robustness
    
    Budget constraint: ≤5% compute
    """
    import hashlib
    import datetime
    
    # Validate budget
    if req.budget > 0.05:
        req.budget = 0.05  # Cap at 5%
    
    # Generate experiment ID
    exp_data = f"{req.hypothesis}:{datetime.datetime.utcnow()}".encode()
    experiment_id = f"exp-{hashlib.md5(exp_data).hexdigest()[:12]}"
    
    # Simulate experiment results
    # Entropy introduces controlled variation
    delta_k = random.uniform(0.01, 0.05) * (req.budget / 0.05)
    delta_theta = random.uniform(0.005, 0.02) * (req.budget / 0.05)
    
    # Risk assessment
    if req.budget < 0.02:
        risk = "bounded"
    elif req.budget < 0.04:
        risk = "elevated"
    else:
        risk = "critical"
    
    insights = {
        "hypothesis_supported": random.choice([True, False]),
        "confidence": random.uniform(0.7, 0.95),
        "sample_size": int(1000 * req.budget / 0.05),
        "p_value": random.uniform(0.01, 0.05)
    }
    
    # Store experiment
    EXPERIMENTS[experiment_id] = {
        "hypothesis": req.hypothesis,
        "type": req.experiment_type,
        "budget": req.budget,
        "results": insights,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    return ExperimentResp(
        experiment_id=experiment_id,
        delta_k=delta_k,
        delta_theta=delta_theta,
        risk=risk,
        insights=insights
    )


@app.post("/chaos", response_model=ChaosResp)
def chaos_test(req: ChaosReq):
    """
    Run chaos engineering test
    
    Actions:
    - latency: Inject network delay
    - failure: Simulate component crash
    - resource_limit: Throttle CPU/memory
    """
    import hashlib
    import datetime
    
    # Generate test ID
    test_data = f"{req.target}:{req.action}:{datetime.datetime.utcnow()}".encode()
    test_id = f"chaos-{hashlib.md5(test_data).hexdigest()[:12]}"
    
    # Simulate chaos impact
    impact_observed = {
        "latency_p99_delta_ms": req.intensity * 100.0,
        "error_rate_delta": req.intensity * 0.05,
        "throughput_delta": -req.intensity * 0.3
    }
    
    # System recovery
    system_recovered = True
    recovery_time_s = random.uniform(5.0, 30.0) * req.intensity
    
    return ChaosResp(
        test_id=test_id,
        impact_observed=impact_observed,
        system_recovered=system_recovered,
        recovery_time_s=recovery_time_s
    )


@app.post("/adversarial", response_model=AdversarialResp)
def adversarial_train(req: AdversarialReq):
    """
    Run adversarial training
    
    Attack types:
    - FGSM, PGD, C&W
    - Backdoor, poisoning
    - Evasion, model extraction
    """
    import hashlib
    
    # Generate patched model ID
    patch_data = f"{req.model_id}:adversarial".encode()
    patched_model_id = f"model-{hashlib.md5(patch_data).hexdigest()[:12]}"
    
    # Simulate adversarial training results
    robustness_score = random.uniform(0.75, 0.95)
    vulnerabilities_found = random.randint(0, 5)
    
    return AdversarialResp(
        robustness_score=robustness_score,
        vulnerabilities_found=vulnerabilities_found,
        patched_model_id=patched_model_id
    )


@app.get("/status")
def get_status():
    """Get Entropy status"""
    return {
        "service": "Λ‑Entropy",
        "description": "Controlled stress and experimentation engine",
        "capabilities": [
            "A/B testing",
            "Chaos engineering",
            "Adversarial training",
            "Stress testing"
        ],
        "budget_constraint": "≤5% compute",
        "experiments_run": len(EXPERIMENTS)
    }


if __name__ == "__main__":
    run(app, 8006)
