"""
Flow execution engine for FluxoX.

Coordinates multi-agent pipeline execution with configurable
mock or LangGraph-backed runs.
"""

# Author: theyashdhiman04

from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, Graph
from pydantic import BaseModel
import logging
from datetime import datetime

from app.agents.researcher import ResearcherAgent
from app.agents.processor import ProcessorAgent
from app.agents.approver import ApproverAgent
from app.agents.optimizer import OptimizerAgent
from app.config import config

logging.basicConfig(
    level=getattr(logging, config.logging.level),
    format=config.logging.format
)
logger = logging.getLogger(__name__)


class FlowState(BaseModel):
    """State for a single flow run."""
    workflow_id: str
    current_step: str = "start"
    data: Dict[str, Any] = {}
    history: List[Dict[str, Any]] = []
    error: Optional[str] = None


class FlowEngine:
    """Runs the agent pipeline (research → process → approve → optimize)."""

    def __init__(self, use_mock: Optional[bool] = None):
        self.researcher = ResearcherAgent()
        self.processor = ProcessorAgent()
        self.approver = ApproverAgent()
        self.optimizer = OptimizerAgent()
        self.graph = self._build_graph()
        self.use_mock = use_mock if use_mock is not None else config.workflow.use_mock

        if self.use_mock:
            logger.warning(
                f"Using mock flow execution in {config.environment} environment.")
        else:
            logger.info(
                f"Using LangGraph flow execution in {config.environment} environment.")

    def _build_graph(self) -> Graph:
        """Build the agent graph."""
        flow = StateGraph(FlowState)
        flow.add_node("research", self.researcher.process)
        flow.add_node("process", self.processor.process)
        flow.add_node("approve", self.approver.process)
        flow.add_node("optimize", self.optimizer.process)
        flow.add_edge("research", "process")
        flow.add_edge("process", "approve")

        def approval_router(state: Dict) -> str:
            return "optimize" if state.get("approved", False) else "process"

        flow.add_conditional_edges(
            "approve",
            approval_router,
            {"optimize": "optimize", "process": "process"}
        )
        flow.set_entry_point("research")
        flow.set_finish_point("optimize")
        return flow.compile()

    async def _run_langgraph(self, workflow_id: str, input_data: Dict[str, Any]) -> FlowState:
        """Execute using LangGraph."""
        try:
            initial = FlowState(workflow_id=workflow_id, data=input_data)
            if hasattr(self.graph, 'arun'):
                return await self.graph.arun(initial)
            raise RuntimeError("LangGraph version does not support 'arun' method")
        except Exception as e:
            logger.error(f"LangGraph execution failed: {str(e)}")
            raise

    async def _run_mock(self, workflow_id: str, input_data: Dict[str, Any]) -> FlowState:
        """Simulate full pipeline without LangGraph."""
        logger.info(f"Using mock flow execution for {workflow_id}")
        ts = datetime.now().isoformat()

        research_results = await self.researcher.process(input_data)
        process_input = {
            "task": "Process research findings",
            "research_findings": research_results,
            "parameters": input_data.get("constraints", {})
        }
        process_results = await self.processor.process(process_input)
        approval_input = {
            "result": process_results,
            "criteria": {"quality_threshold": 0.8}
        }
        approval_results = await self.approver.process(approval_input)
        optimization_input = {
            "workflow_results": {
                "research": research_results,
                "process": process_results,
                "approval": approval_results
            },
            "performance_metrics": {"execution_time": 1.5, "success_rate": 1.0}
        }
        optimization_results = await self.optimizer.process(optimization_input)

        mock_data = {
            "research_results": research_results,
            "processed_data": process_results,
            "approval": approval_results,
            "optimization": optimization_results
        }

        return FlowState(
            workflow_id=workflow_id,
            current_step="optimize",
            data=mock_data,
            history=[
                {"step": "research", "timestamp": ts},
                {"step": "process", "timestamp": ts},
                {"step": "approve", "timestamp": ts},
                {"step": "optimize", "timestamp": ts}
            ]
        )

    async def execute_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the flow for the given workflow id and input."""
        initial_state = FlowState(workflow_id=workflow_id, data=input_data)
        try:
            if self.use_mock:
                final_state = await self._run_mock(workflow_id, input_data)
            else:
                try:
                    final_state = await self._run_langgraph(workflow_id, input_data)
                except Exception as e:
                    logger.warning(f"LangGraph failed, falling back to mock: {str(e)}")
                    final_state = await self._run_mock(workflow_id, input_data)

            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "result": final_state.data,
                "history": final_state.history
            }
        except Exception as e:
            logger.error(f"Error executing flow: {str(e)}")
            return {
                "workflow_id": workflow_id,
                "status": "error",
                "error": str(e),
                "history": initial_state.history
            }
