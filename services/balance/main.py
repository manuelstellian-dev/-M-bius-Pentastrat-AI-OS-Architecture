"""
Λ‑Balance: Homeostasis and SLA maintenance
PID/MPC control, throttling, checkpointing
Avoids oscillations and maintains stable utilization
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from services.common.server import create_app, run

app = create_app("balance")


class PIDParams(BaseModel):
    """PID controller parameters"""
    kp: float = 0.2  # Proportional gain
    ki: float = 0.05  # Integral gain
    kd: float = 0.0  # Derivative gain


class TuneReq(BaseModel):
    """Request to tune SLA parameters"""
    lat_p99: float  # Current p99 latency
    Lmax: float  # Maximum allowed latency
    pid: PIDParams = PIDParams()
    integral: float = 0.0  # Accumulated integral
    prev_error: float = 0.0  # Previous error for derivative


class TuneResp(BaseModel):
    """Response with tuning adjustments"""
    throttle: float  # Throttling factor [0, 1]
    priority: int  # Priority adjustment
    integral: float  # Updated integral
    prev_error: float  # Current error for next iteration
    control_signal: float  # Raw PID output


class CheckpointReq(BaseModel):
    """Request to create checkpoint"""
    component: str
    state: dict


class CheckpointResp(BaseModel):
    """Response with checkpoint ID"""
    checkpoint_id: str
    timestamp: str


@app.post("/tune", response_model=TuneResp)
def tune(req: TuneReq):
    """
    PID control for SLA maintenance
    
    Formula:
    error = Lmax - lat_p99
    integral = integral + error (with anti-windup)
    derivative = error - prev_error
    control = kp·error + ki·integral + kd·derivative
    
    Target: ρ* < 0.7–0.8 (utilization)
    """
    # Calculate error
    error = req.Lmax - req.lat_p99
    
    # Update integral with anti-windup
    integ = req.integral + error
    integ = max(min(integ, 1000.0), -1000.0)  # Clamp
    
    # Calculate derivative
    deriv = error - req.prev_error
    
    # PID control signal
    control = req.pid.kp * error + req.pid.ki * integ + req.pid.kd * deriv
    
    # Convert to throttle [0, 1]
    # Positive control → less throttling (system is under target)
    # Negative control → more throttling (system is over target)
    throttle = max(0.0, min(1.0, 0.5 + control / 100.0))
    
    # Priority adjustment
    priority = 1 if error < 0 else 0  # High priority if over limit
    
    return TuneResp(
        throttle=throttle,
        priority=priority,
        integral=integ,
        prev_error=error,
        control_signal=control
    )


@app.post("/checkpoint", response_model=CheckpointResp)
def checkpoint(req: CheckpointReq):
    """
    Create intelligent checkpoint for component
    
    Used for:
    - Rollback capability
    - State recovery
    - A/B testing reversion
    """
    import datetime
    import hashlib
    
    # Generate checkpoint ID
    timestamp = datetime.datetime.utcnow().isoformat()
    data = f"{req.component}:{timestamp}".encode()
    checkpoint_id = f"ckpt-{hashlib.md5(data).hexdigest()[:12]}"
    
    # In production, save state to persistent storage
    # For now, return checkpoint ID
    return CheckpointResp(
        checkpoint_id=checkpoint_id,
        timestamp=timestamp
    )


@app.get("/status")
def get_status():
    """Get Balance status"""
    return {
        "service": "Λ‑Balance",
        "description": "Homeostasis and SLA maintenance engine",
        "capabilities": [
            "PID/MPC control for SLA",
            "Throttling management",
            "Intelligent checkpointing",
            "Oscillation prevention"
        ],
        "target_utilization": "ρ* < 0.7–0.8"
    }


if __name__ == "__main__":
    run(app, 8003)
