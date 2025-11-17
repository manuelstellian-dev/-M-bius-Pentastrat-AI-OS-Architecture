"""
Λ‑Planner: Task & Trajectory Planning
Hierarchical planning (L0-L3), code synthesis, validation
Connected to Arbiter and Optimize
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.common.server import create_app, run

app = create_app("planner")


class Task(BaseModel):
    """Task definition"""
    id: str
    description: str
    priority: int = 0
    constraints: Dict[str, Any] = {}


class Plan(BaseModel):
    """Execution plan"""
    task_id: str
    steps: List[Dict[str, Any]]
    resources_required: Dict[str, float]
    estimated_duration_s: float


class DecomposeReq(BaseModel):
    """Request to decompose task"""
    task: Task


class DecomposeResp(BaseModel):
    """Response with decomposed plan"""
    plan: Plan


class SynthCodeReq(BaseModel):
    """Request to synthesize code"""
    spec: str
    language: str = "python"
    safety_level: str = "high"


class SynthCodeResp(BaseModel):
    """Response with synthesized code"""
    code: str
    artifact_id: str
    tests_generated: List[str]
    validated: bool


class ValidateReq(BaseModel):
    """Request to validate and ship"""
    artifact_id: str
    canary_percent: float = 0.02


class ValidateResp(BaseModel):
    """Response after validation"""
    deploy_id: str
    validation_passed: bool
    deployed: bool


@app.post("/decompose", response_model=DecomposeResp)
def decompose_task(req: DecomposeReq):
    """
    Decompose high-level task into execution plan
    
    Hierarchy:
    - L0: Mission/objective
    - L1: Strategic plan
    - L2: Tactical steps
    - L3: Atomic actions
    
    Integrates with Arbiter for resource allocation
    """
    task = req.task
    
    # Simple decomposition logic
    steps = [
        {
            "level": "L2",
            "action": "analyze_requirements",
            "params": {"task_id": task.id},
            "duration_s": 5.0
        },
        {
            "level": "L2",
            "action": "allocate_resources",
            "params": {"arbiter_consult": True},
            "duration_s": 2.0
        },
        {
            "level": "L3",
            "action": "execute_transformation",
            "params": {"optimize_service": True},
            "duration_s": 30.0
        },
        {
            "level": "L3",
            "action": "validate_results",
            "params": {"safety_check": True},
            "duration_s": 10.0
        },
        {
            "level": "L2",
            "action": "deploy_canary",
            "params": {"canary_percent": 0.02},
            "duration_s": 15.0
        }
    ]
    
    resources_required = {
        "cpu": 4.0,
        "memory_gb": 8.0,
        "gpu": 0.5
    }
    
    estimated_duration = sum(s["duration_s"] for s in steps)
    
    plan = Plan(
        task_id=task.id,
        steps=steps,
        resources_required=resources_required,
        estimated_duration_s=estimated_duration
    )
    
    return DecomposeResp(plan=plan)


@app.post("/synth_code", response_model=SynthCodeResp)
def synthesize_code(req: SynthCodeReq):
    """
    Synthesize code from specification
    
    Process:
    1. LLM generation (controlled, sandboxed)
    2. Static analysis
    3. Generate unit tests
    4. Property-based tests
    5. Safety verification
    6. Canary deployment
    
    Safety levels:
    - low: Basic syntax check
    - medium: + Unit tests
    - high: + Property tests + Formal verification
    """
    import hashlib
    
    # Generate artifact ID
    artifact_data = f"{req.spec}:{req.language}".encode()
    artifact_id = f"code-{hashlib.md5(artifact_data).hexdigest()[:12]}"
    
    # Simulate code generation
    # In production, this would use LLM with safety controls
    code = f"""
# Generated code for: {req.spec}
def generated_function():
    \"\"\"
    Specification: {req.spec}
    Language: {req.language}
    Safety level: {req.safety_level}
    \"\"\"
    # Implementation would go here
    pass
"""
    
    # Generate tests
    tests_generated = [
        "test_basic_functionality",
        "test_edge_cases",
        "test_error_handling"
    ]
    
    if req.safety_level == "high":
        tests_generated.extend([
            "test_property_invariants",
            "test_security_boundaries"
        ])
    
    # Validate
    validated = True  # In production, run actual validation
    
    return SynthCodeResp(
        code=code,
        artifact_id=artifact_id,
        tests_generated=tests_generated,
        validated=validated
    )


@app.post("/validate_and_ship", response_model=ValidateResp)
def validate_and_ship(req: ValidateReq):
    """
    Validate artifact and deploy
    
    Steps:
    1. Run test suite
    2. Safety verification (Λ‑Safety service)
    3. Create checkpoint
    4. Deploy canary
    5. Monitor (Λ‑Explain)
    6. Promote or rollback
    """
    import hashlib
    import datetime
    
    # Generate deploy ID
    deploy_data = f"{req.artifact_id}:{datetime.datetime.utcnow()}".encode()
    deploy_id = f"deploy-{hashlib.md5(deploy_data).hexdigest()[:12]}"
    
    # Validate
    validation_passed = True  # In production, run actual validation
    
    # Deploy
    deployed = validation_passed
    
    return ValidateResp(
        deploy_id=deploy_id,
        validation_passed=validation_passed,
        deployed=deployed
    )


@app.get("/status")
def get_status():
    """Get Planner status"""
    return {
        "service": "Λ‑Planner",
        "description": "Task & Trajectory Planning Engine",
        "capabilities": [
            "Hierarchical planning (L0-L3)",
            "Task decomposition",
            "Safe code synthesis",
            "Validation & deployment",
            "Integration with Arbiter & Optimize"
        ],
        "safety_levels": ["low", "medium", "high"]
    }


if __name__ == "__main__":
    run(app, 8011)
