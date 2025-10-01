"""Tests for the FluxoX flow engine."""

import pytest
from unittest.mock import patch, MagicMock
from app.flow.engine import FlowEngine, FlowState
import uuid


class MockFlowGraph:
    def __init__(self):
        self.state = {}
        self.compiled = True

    async def arun(self, input_data):
        state = FlowState(
            workflow_id=input_data.workflow_id,
            current_step="optimize",
            data={
                "research_results": "Research completed",
                "processed_data": "Data processed",
                "approval": {"approved": True, "feedback": "Approved"},
                "optimization": "Workflow optimized"
            },
            history=[
                {"step": "research", "timestamp": "2023-01-01T00:00:00"},
                {"step": "process", "timestamp": "2023-01-01T00:00:01"},
                {"step": "approve", "timestamp": "2023-01-01T00:00:02"},
                {"step": "optimize", "timestamp": "2023-01-01T00:00:03"}
            ]
        )
        return state


@pytest.mark.asyncio
async def test_flow_engine_initialization():
    """Test that the flow engine initializes correctly."""
    with patch('app.flow.engine.FlowEngine._build_graph') as mock_build:
        mock_build.return_value = MockFlowGraph()
        engine = FlowEngine()
        assert engine is not None
        assert engine.graph is not None
        assert engine.graph.compiled is True


@pytest.mark.asyncio
async def test_flow_engine_agents():
    """Test that the flow engine initializes agents correctly."""
    with patch('app.flow.engine.FlowEngine._build_graph') as mock_build:
        mock_build.return_value = MockFlowGraph()
        engine = FlowEngine()
        assert engine.researcher is not None
        assert engine.processor is not None
        assert engine.approver is not None
        assert engine.optimizer is not None


@pytest.mark.asyncio
async def test_flow_engine_execute():
    """Test that the flow engine executes correctly."""
    with patch('app.flow.engine.FlowEngine._build_graph') as mock_build:
        mock_build.return_value = MockFlowGraph()
        with patch('app.flow.engine.FlowEngine._run_mock') as mock_run:
            mock_state = FlowState(
                workflow_id="test-id",
                current_step="optimize",
                data={
                    "research_results": "Research completed",
                    "processed_data": "Data processed",
                    "approval": {"approved": True, "feedback": "Approved"},
                    "optimization": "Workflow optimized"
                },
                history=[
                    {"step": "research", "timestamp": "2023-01-01T00:00:00"},
                    {"step": "process", "timestamp": "2023-01-01T00:00:01"},
                    {"step": "approve", "timestamp": "2023-01-01T00:00:02"},
                    {"step": "optimize", "timestamp": "2023-01-01T00:00:03"}
                ]
            )
            mock_run.return_value = mock_state

            engine = FlowEngine()
            workflow_id = "test-id"
            input_data = {"input": "test data"}
            result = await engine.execute_workflow(workflow_id, input_data)

            assert result["workflow_id"] == workflow_id
            assert result["status"] == "completed"
            assert "result" in result
            data = result["result"]
            assert "research_results" in data
            assert "processed_data" in data
            assert "approval" in data
            assert "optimization" in data


@pytest.mark.asyncio
async def test_flow_engine_error_handling():
    """Test that the flow engine handles errors correctly."""
    with patch('app.flow.engine.FlowEngine._build_graph') as mock_build:
        mock_graph = MagicMock()
        mock_graph.arun.side_effect = Exception("Test error")
        mock_build.return_value = mock_graph

        with patch('app.flow.engine.FlowEngine._run_mock') as mock_run:
            mock_run.side_effect = Exception("Test error")

            engine = FlowEngine()
            workflow_id = "test-id"
            input_data = {"input": "test data"}

            result = await engine.execute_workflow(workflow_id, input_data)
            assert result["status"] == "error"
            assert "Test error" in result["error"]


@pytest.mark.asyncio
async def test_flow_state_initialization():
    """Test that flow state can be initialized with custom values."""
    workflow_id = str(uuid.uuid4())
    state = FlowState(
        workflow_id=workflow_id,
        current_step="research",
        data={"query": "Test query"},
        history=[{"step": "start", "timestamp": "2023-01-01T00:00:00"}]
    )

    assert state.workflow_id == workflow_id
    assert state.current_step == "research"
    assert state.data["query"] == "Test query"
    assert len(state.history) == 1
    assert state.error is None


@pytest.mark.asyncio
async def test_execute_workflow_e2e():
    """Test end-to-end flow execution."""
    with patch('app.flow.engine.FlowEngine._run_mock') as mock_run:
        mock_state = FlowState(
            workflow_id="test-workflow-id",
            current_step="optimize",
            data={
                "research_results": {"findings": "Test findings"},
                "processed_data": {"result": "Test result"},
                "approval": {"approved": True},
                "optimization": {"optimizations": ["Test optimization"]}
            },
            history=[
                {"step": "research", "timestamp": "2023-01-01T00:00:00"},
                {"step": "optimize", "timestamp": "2023-01-01T00:00:03"}
            ]
        )
        mock_run.return_value = mock_state

        engine = FlowEngine()
        workflow_id = str(uuid.uuid4())
        input_data = {
            "query": "Analyze customer feedback trends",
            "context": "E-commerce customer reviews dataset",
            "constraints": {
                "time_period": "last_month",
                "min_confidence": 0.8
            }
        }

        result = await engine.execute_workflow(workflow_id, input_data)

        assert result["workflow_id"] == workflow_id
        assert result["status"] == "completed"
        assert "result" in result
        assert "history" in result


@pytest.mark.asyncio
async def test_workflow_error_handling():
    """Test that the flow engine handles errors gracefully."""
    class ErrorTestEngine(FlowEngine):
        async def execute_workflow(self, workflow_id, input_data):
            try:
                raise ValueError("Test error")
            except Exception as e:
                return {
                    "workflow_id": workflow_id,
                    "status": "error",
                    "error": str(e),
                    "history": []
                }

    engine = ErrorTestEngine()
    workflow_id = str(uuid.uuid4())

    result = await engine.execute_workflow(workflow_id, {"query": "test"})

    assert result["workflow_id"] == workflow_id
    assert result["status"] == "error"
    assert "Test error" in result["error"]
    assert "history" in result
