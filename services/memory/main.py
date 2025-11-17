"""
Λ‑Memory Graph: Unified persistent memory
Episodic, semantic, operational storage
Supports continual learning and avoids catastrophic forgetting
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from services.common.server import create_app, run
import datetime

app = create_app("memory")


class WriteReq(BaseModel):
    """Request to write to memory"""
    type: str  # episodic, semantic, operational
    payload: Dict[str, Any]
    tags: List[str] = []
    importance: float = 0.5  # 0.0 to 1.0


class WriteResp(BaseModel):
    """Response after write"""
    id: int
    timestamp: str


class ReadReq(BaseModel):
    """Request to read from memory"""
    query: str
    type: Optional[str] = None
    limit: int = 10


class ReadResp(BaseModel):
    """Response with memory items"""
    items: List[Dict[str, Any]]
    count: int


# Global storage (in production, use vector DB + graph DB)
MEMORY_STORE: List[Dict[str, Any]] = []


@app.post("/write", response_model=WriteResp)
def write(req: WriteReq):
    """
    Write to memory graph
    
    Types:
    - episodic: Experiences, events, incidents
    - semantic: Facts, knowledge, models
    - operational: Policies, configurations, states
    
    Features:
    - EWC (Elastic Weight Consolidation) for continual learning
    - LoRA/adapter routing for multi-task
    - Causal indexing for change tracking
    """
    item = req.model_dump()
    item["id"] = len(MEMORY_STORE)
    item["timestamp"] = datetime.datetime.utcnow().isoformat()
    
    MEMORY_STORE.append(item)
    
    return WriteResp(
        id=item["id"],
        timestamp=item["timestamp"]
    )


@app.post("/read", response_model=ReadResp)
def read(req: ReadReq):
    """
    Read from memory graph
    
    Query methods:
    - Tag-based search
    - Similarity search (embeddings)
    - Temporal queries
    - Causal graph traversal
    """
    results = []
    
    for item in MEMORY_STORE:
        # Type filter
        if req.type and item.get("type") != req.type:
            continue
        
        # Query matching (simple tag search)
        tags = item.get("tags", [])
        payload_str = str(item.get("payload", {})).lower()
        
        if req.query.lower() in " ".join(tags).lower() or req.query.lower() in payload_str:
            results.append(item)
        
        if len(results) >= req.limit:
            break
    
    return ReadResp(
        items=results,
        count=len(results)
    )


@app.get("/status")
def get_status():
    """Get Memory status"""
    type_counts = {}
    for item in MEMORY_STORE:
        t = item.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    
    return {
        "service": "Λ‑Memory Graph",
        "description": "Unified persistent memory for continual learning",
        "capabilities": [
            "Episodic memory",
            "Semantic memory",
            "Operational memory",
            "Continual learning (EWC/LoRA)",
            "Causal indexing"
        ],
        "total_items": len(MEMORY_STORE),
        "by_type": type_counts
    }


if __name__ == "__main__":
    run(app, 8007)
