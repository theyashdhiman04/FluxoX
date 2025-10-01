"""Flow management API for FluxoX."""

from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.schemas.workflow import WorkflowList, WorkflowDetail
import json
from typing import List, Dict, Any

router = APIRouter()


@router.get("/", response_model=List[WorkflowList])
async def list_flows():
    """List all flows."""
    async with get_db() as db:
        workflows = await db.fetch_all("SELECT * FROM workflows")
        return [
            {
                "id": w["id"],
                "name": w["name"],
                "description": w["description"],
                "status": w["status"],
                "created_at": w["created_at"],
                "updated_at": w["updated_at"]
            }
            for w in workflows
        ]


@router.get("/templates", response_model=List[Dict[str, Any]])
async def list_flow_templates():
    """List available flow templates."""
    return [
        {
            "id": "data-analysis",
            "name": "Data Analysis Flow",
            "description": "Analyze data sets and generate insights",
            "steps": [
                {"name": "Research", "agent": "Researcher", "description": "Gather relevant data"},
                {"name": "Process", "agent": "Processor", "description": "Process and analyze data"},
                {"name": "Approve", "agent": "Approver", "description": "Validate analysis results"},
                {"name": "Optimize", "agent": "Optimizer", "description": "Suggest improvements"}
            ]
        },
        {
            "id": "content-generation",
            "name": "Content Generation Flow",
            "description": "Generate and optimize content based on requirements",
            "steps": [
                {"name": "Research", "agent": "Researcher", "description": "Research topic and gather information"},
                {"name": "Process", "agent": "Processor", "description": "Generate initial content draft"},
                {"name": "Approve", "agent": "Approver", "description": "Review and approve content"},
                {"name": "Optimize", "agent": "Optimizer", "description": "Optimize content for engagement"}
            ]
        },
        {
            "id": "customer-support",
            "name": "Customer Support Flow",
            "description": "Handle customer inquiries and support tickets",
            "steps": [
                {"name": "Research", "agent": "Researcher", "description": "Research customer history and issue"},
                {"name": "Process", "agent": "Processor", "description": "Generate response or solution"},
                {"name": "Approve", "agent": "Approver", "description": "Review and approve response"},
                {"name": "Optimize", "agent": "Optimizer", "description": "Suggest improvements to process"}
            ]
        }
    ]


@router.get("/{flow_id}", response_model=WorkflowDetail)
async def get_flow(flow_id: str):
    """Get a flow by ID."""
    async with get_db() as db:
        workflow = await db.fetch_one(
            "SELECT * FROM workflows WHERE id = ?",
            (flow_id,)
        )
        if not workflow:
            raise HTTPException(status_code=404, detail="Flow not found")
        result = None
        if workflow.get("result"):
            try:
                result = json.loads(workflow["result"])
            except json.JSONDecodeError:
                result = {"data": workflow["result"]}
        return {
            "id": workflow["id"],
            "name": workflow["name"],
            "description": workflow["description"],
            "status": workflow["status"],
            "result": result,
            "error": workflow.get("error"),
            "created_at": workflow["created_at"],
            "updated_at": workflow["updated_at"]
        }


@router.delete("/{flow_id}", status_code=204)
async def delete_flow(flow_id: str):
    """Delete a flow by ID."""
    async with get_db() as db:
        workflow = await db.fetch_one(
            "SELECT id FROM workflows WHERE id = ?",
            (flow_id,)
        )
        if not workflow:
            raise HTTPException(status_code=404, detail="Flow not found")
        await db.execute(
            "DELETE FROM workflows WHERE id = ?",
            (flow_id,)
        )
        return None
