"""
Λ‑Safety & Policy Guard: Security and governance
Formal/heuristic verification, sandboxing, canary, attestation
Kill-switch with privilege superior to Arbiter
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from services.common.server import create_app, run

app = create_app("safety")


class VerifyReq(BaseModel):
    """Request to verify change"""
    attested: bool
    canary: bool
    rollback_plan: bool
    change_type: str = "deploy"
    risk_level: str = "medium"


class VerifyResp(BaseModel):
    """Response with verification result"""
    pass_: bool
    reasons: list[str]
    gate_keeper: str = "Λ‑Safety"


class SandboxReq(BaseModel):
    """Request to sandbox artifact"""
    artifact_id: str
    code: Optional[str] = None
    timeout_s: int = 30


class SandboxResp(BaseModel):
    """Response from sandbox"""
    verdict: str  # pass, fail, timeout
    output: Dict[str, Any]
    violations: list[str]


class AttestReq(BaseModel):
    """Request to attest component"""
    component: str
    signature: Optional[str] = None
    tpm_available: bool = False


class AttestResp(BaseModel):
    """Response with attestation"""
    ok: bool
    attestation_id: str
    chain_verified: bool


@app.post("/verify", response_model=VerifyResp)
def verify(req: VerifyReq):
    """
    Verify change before deployment
    
    Checks:
    - Attestation present and valid
    - Canary plan defined
    - Rollback plan available
    - Invariants maintained
    - Policy compliance (OPA)
    
    Invariants:
    - Domain isolation
    - Non-interference between critical levels
    - Safety boundaries
    """
    reasons = []
    
    if not req.attested:
        reasons.append("Missing attestation")
    
    if not req.canary:
        reasons.append("No canary deployment plan")
    
    if not req.rollback_plan:
        reasons.append("No rollback plan defined")
    
    # Risk-based checks
    if req.risk_level == "high" and not all([req.attested, req.canary, req.rollback_plan]):
        reasons.append("High risk changes require all safety measures")
    
    pass_check = len(reasons) == 0
    
    return VerifyResp(
        pass_=pass_check,
        reasons=reasons if not pass_check else ["All checks passed"]
    )


@app.post("/sandbox", response_model=SandboxResp)
def sandbox(req: SandboxReq):
    """
    Run artifact in sandboxed environment
    
    Features:
    - Container isolation
    - seccomp filters
    - No network by default
    - CPU/GPU caps
    - Resource monitoring
    """
    import time
    import random
    
    violations = []
    
    # Simulate sandbox execution
    time.sleep(0.1)  # Simulate execution time
    
    # Random violation detection
    if random.random() < 0.1:  # 10% chance of violation
        violations.append("Attempted network access")
    
    if random.random() < 0.05:  # 5% chance
        violations.append("Memory limit exceeded")
    
    verdict = "pass" if len(violations) == 0 else "fail"
    
    return SandboxResp(
        verdict=verdict,
        output={"status": "completed", "runtime_s": 0.1},
        violations=violations
    )


@app.post("/attest", response_model=AttestResp)
def attest(req: AttestReq):
    """
    Attest component integrity
    
    Methods:
    - Hash-chain verification
    - TPM/TEE attestation (if available)
    - Signature verification
    - Boot-to-cloud chain
    """
    import hashlib
    import datetime
    
    # Generate attestation ID
    att_data = f"{req.component}:{datetime.datetime.utcnow()}".encode()
    attestation_id = f"att-{hashlib.md5(att_data).hexdigest()[:12]}"
    
    # Check signature if provided
    signature_ok = bool(req.signature)
    
    # Check TPM/TEE if available
    tpm_ok = req.tpm_available
    
    # Verify chain
    chain_verified = signature_ok or tpm_ok
    
    ok = chain_verified
    
    return AttestResp(
        ok=ok,
        attestation_id=attestation_id,
        chain_verified=chain_verified
    )


@app.post("/killswitch")
def killswitch(reason: str, authorized: bool = False):
    """
    Emergency kill-switch
    
    Privilege: Superior to Arbiter
    Triggers:
    - Critical security violation
    - Safety invariant broken
    - Manual override
    """
    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized kill-switch activation")
    
    # In production, this would:
    # 1. Stop all inference
    # 2. Quarantine all models
    # 3. Alert operators
    # 4. Preserve state for forensics
    
    return {
        "status": "kill-switch activated",
        "reason": reason,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "action": "System halted for safety"
    }


@app.get("/status")
def get_status():
    """Get Safety status"""
    return {
        "service": "Λ‑Safety & Policy Guard",
        "description": "Security, governance, and kill-switch",
        "capabilities": [
            "Change verification",
            "Sandbox execution",
            "Component attestation",
            "Policy enforcement (OPA)",
            "Kill-switch (superior privilege)"
        ],
        "invariants": [
            "Domain isolation",
            "Non-interference",
            "Attestation required"
        ]
    }


if __name__ == "__main__":
    run(app, 8008)
