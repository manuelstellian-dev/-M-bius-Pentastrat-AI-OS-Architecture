"""
Λ‑Econ: Resource & Value Engine
Cost/benefit accounting, budget management, ROI calculation
Feeds Reinvest with measurable ROI
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from services.common.server import create_app, run

app = create_app("econ")


class ROIReq(BaseModel):
    """Request to calculate ROI"""
    action_id: str
    deltaU: float  # Utility gain
    deltaCost: float  # Cost delta
    deltaRisk: float  # Risk delta
    invest: float  # Investment amount


class ROIResp(BaseModel):
    """Response with ROI"""
    action_id: str
    roi: float
    roi_category: str  # excellent, good, fair, poor


class InvestReq(BaseModel):
    """Request to allocate investment budget"""
    total_budget: float
    candidates: List[Dict[str, float]]  # List of {id, ask, expected_roi}


class InvestResp(BaseModel):
    """Response with allocation plan"""
    allocations: Dict[str, float]
    total_allocated: float
    expected_return: float


class BudgetReq(BaseModel):
    """Request budget information"""
    component: str


class BudgetResp(BaseModel):
    """Response with budget"""
    component: str
    allocated: float
    spent: float
    remaining: float


# Budget tracking
BUDGETS = {
    "entropy": {"allocated": 0.05, "spent": 0.0},
    "regen": {"allocated": 0.10, "spent": 0.0},
    "optimize": {"allocated": 0.15, "spent": 0.0},
}


@app.post("/roi", response_model=ROIResp)
def calculate_roi(req: ROIReq):
    """
    Calculate Return on Investment
    
    Formula:
    ROI = (ΔU − ΔCost − λ_risk·ΔRisk) / Invest
    
    Where:
    - ΔU: Utility improvement
    - ΔCost: Cost increase (negative for savings)
    - ΔRisk: Risk increase (negative for risk reduction)
    - λ_risk: Risk weight (typically 0.5)
    """
    lambda_risk = 0.5
    
    numerator = req.deltaU - req.deltaCost - lambda_risk * req.deltaRisk
    denominator = max(1e-6, req.invest)  # Avoid division by zero
    
    roi = numerator / denominator
    
    # Categorize ROI
    if roi >= 2.0:
        category = "excellent"
    elif roi >= 1.0:
        category = "good"
    elif roi >= 0.5:
        category = "fair"
    else:
        category = "poor"
    
    return ROIResp(
        action_id=req.action_id,
        roi=roi,
        roi_category=category
    )


@app.post("/invest", response_model=InvestResp)
def allocate_investment(req: InvestReq):
    """
    Allocate investment budget using ROI-based prioritization
    
    Strategy:
    - Sort candidates by expected ROI (descending)
    - Allocate to highest ROI actions first
    - Stop when budget exhausted
    
    This is a greedy bandit approach:
    argmax_a E[ROI(a)] subject to budget constraint
    """
    # Sort candidates by expected ROI
    sorted_candidates = sorted(
        req.candidates,
        key=lambda c: c.get("expected_roi", 0.0),
        reverse=True
    )
    
    allocations = {}
    remaining_budget = req.total_budget
    expected_return = 0.0
    
    for candidate in sorted_candidates:
        if remaining_budget <= 0:
            break
        
        cid = candidate.get("id", "unknown")
        ask = candidate.get("ask", 0.0)
        expected_roi = candidate.get("expected_roi", 0.0)
        
        # Allocate up to what's requested or what's available
        allocation = min(ask, remaining_budget)
        allocations[cid] = allocation
        remaining_budget -= allocation
        expected_return += allocation * expected_roi
    
    total_allocated = req.total_budget - remaining_budget
    
    return InvestResp(
        allocations=allocations,
        total_allocated=total_allocated,
        expected_return=expected_return
    )


@app.post("/budget", response_model=BudgetResp)
def get_budget(req: BudgetReq):
    """
    Get budget information for component
    """
    budget_info = BUDGETS.get(req.component, {"allocated": 0.0, "spent": 0.0})
    
    allocated = budget_info["allocated"]
    spent = budget_info["spent"]
    remaining = allocated - spent
    
    return BudgetResp(
        component=req.component,
        allocated=allocated,
        spent=spent,
        remaining=remaining
    )


@app.post("/spend")
def record_spend(component: str, amount: float):
    """Record spending for a component"""
    if component not in BUDGETS:
        BUDGETS[component] = {"allocated": 0.0, "spent": 0.0}
    
    BUDGETS[component]["spent"] += amount
    
    return {
        "component": component,
        "spent": amount,
        "total_spent": BUDGETS[component]["spent"]
    }


@app.get("/status")
def get_status():
    """Get Econ status"""
    total_allocated = sum(b["allocated"] for b in BUDGETS.values())
    total_spent = sum(b["spent"] for b in BUDGETS.values())
    
    return {
        "service": "Λ‑Econ",
        "description": "Resource & Value Engine for ROI-driven reinvestment",
        "capabilities": [
            "ROI calculation",
            "Budget allocation (greedy bandit)",
            "Spend tracking",
            "Investment optimization"
        ],
        "total_budget_allocated": total_allocated,
        "total_spent": total_spent,
        "remaining": total_allocated - total_spent
    }


if __name__ == "__main__":
    run(app, 8009)
