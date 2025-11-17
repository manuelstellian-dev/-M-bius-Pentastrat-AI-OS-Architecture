"""
Basic tests for Λ‑Möbius services
"""
import pytest
import sys
import os

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.arbiter.main import decide_mode, DecideReq, DecideResp
from services.timewrap.main import lambda_time, LambdaTimeReq, LambdaTimeResp
import math


class TestArbiter:
    """Test Λ‑Arbiter Core"""
    
    def test_decide_mode_wrap(self):
        """Test Wrap mode decision (high resilience)"""
        req = DecideReq(theta=0.85, low=0.55, high=0.80)
        resp = decide_mode(req)
        # Response is a dict from FastAPI endpoint
        assert resp["state"] == 1
        assert "Wrap" in resp["mode_name"]
    
    def test_decide_mode_steady(self):
        """Test Steady mode decision (medium resilience)"""
        req = DecideReq(theta=0.65, low=0.55, high=0.80)
        resp = decide_mode(req)
        assert resp["state"] == 0
        assert "Steady" in resp["mode_name"]
    
    def test_decide_mode_unwrap(self):
        """Test Unwrap mode decision (low resilience)"""
        req = DecideReq(theta=0.45, low=0.55, high=0.80)
        resp = decide_mode(req)
        assert resp["state"] == -1
        assert "Unwrap" in resp["mode_name"]


class TestTimeWrap:
    """Test Λ‑TimeWrap"""
    
    def test_lambda_time_wrap(self):
        """Test Λ‑Time Wrap calculation"""
        req = LambdaTimeReq(mode=1, T1=10.0, k=2.0, P=1.2, U=8.0)
        resp = lambda_time(req)
        
        # Verify it's positive and makes sense
        assert resp.value > 0
        assert resp.convergent is True
        assert "Wrap" in resp.mode_name
        
        # Manual calculation check
        kP = req.k * req.P
        expected = req.T1 * math.log(req.U) / (1 - 1/kP)
        assert abs(resp.value - expected) < 0.01
    
    def test_lambda_time_steady(self):
        """Test Λ‑Time Steady calculation"""
        req = LambdaTimeReq(mode=0, T1=10.0, k=1.5, P=1.0, U=8.0)
        resp = lambda_time(req)
        
        # Verify
        assert resp.value > 0
        assert resp.convergent is True
        assert "Steady" in resp.mode_name
        
        # Manual calculation
        expected = req.T1 * math.log(req.U)
        assert abs(resp.value - expected) < 0.01
    
    def test_lambda_time_unwrap_convergent(self):
        """Test Λ‑Time Unwrap calculation (convergent)"""
        req = LambdaTimeReq(mode=-1, T1=10.0, k=0.5, P=1.0, U=8.0)
        resp = lambda_time(req)
        
        # Verify
        assert resp.value > 0
        assert resp.convergent is True
        assert "Unwrap" in resp.mode_name
        
        # Manual calculation
        kP = req.k * req.P
        expected = req.T1 * math.log(req.U) / (1 - kP)
        assert abs(resp.value - expected) < 0.01
    
    def test_lambda_time_wrap_requires_kP_greater_than_1(self):
        """Test that Wrap mode requires k·P > 1"""
        req = LambdaTimeReq(mode=1, T1=10.0, k=0.5, P=1.0, U=8.0)
        
        with pytest.raises(Exception):
            lambda_time(req)


class TestIntegration:
    """Integration tests"""
    
    def test_arbiter_and_timewrap_integration(self):
        """Test Arbiter decision feeds into TimeWrap"""
        # High resilience → Wrap mode
        arbiter_req = DecideReq(theta=0.85)
        arbiter_resp = decide_mode(arbiter_req)
        
        assert arbiter_resp["state"] == 1  # Wrap
        
        # Use Wrap mode in TimeWrap
        timewrap_req = LambdaTimeReq(
            mode=arbiter_resp["state"],
            T1=10.0,
            k=2.0,
            P=1.2,
            U=8.0
        )
        timewrap_resp = lambda_time(timewrap_req)
        
        # Should get valid Λ‑Time
        assert timewrap_resp.value > 0
        assert timewrap_resp.convergent is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
