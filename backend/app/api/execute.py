from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

from app.flow.engine import FlowEngine

router = APIRouter()
flow_engine = FlowEngine()


class ExecuteRequest(BaseModel):
    """Request model for workflow execution."""
    workflow_id: str
    input_data: Dict[str, Any]


@router.post("/")
async def execute_flow(request: ExecuteRequest):
    """Execute a flow with the given input data (integrated execute endpoint)."""
    try:
        result = await flow_engine.execute_workflow(
            workflow_id=request.workflow_id,
            input_data=request.input_data
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Flow execution failed: {str(e)}"
        )


@router.post("/test")
async def test_flow():
    """Test flow execution with sample data."""
    test_data = {
        "workflow_id": "test-flow",
        "input_data": {
            "query": "Analyze customer feedback trends",
            "context": "E-commerce customer reviews dataset",
            "constraints": {
                "time_period": "last_month",
                "min_confidence": 0.8
            }
        }
    }
    return await execute_flow(ExecuteRequest(**test_data))
