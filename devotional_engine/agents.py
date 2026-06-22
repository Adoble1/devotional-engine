from typing import Protocol
from .exceptions import AgentOutputError


class AgentAdapter(Protocol):
    def call(self, role: str, payload: dict) -> dict: ...


class MockAgentAdapter:
    def __init__(self, outputs: dict):
        self.outputs = outputs

    def call(self, role: str, payload: dict) -> dict:
        if role not in self.outputs:
            raise AgentOutputError(f"Missing mock output for role: {role}")
        output = self.outputs[role]
        result = output(payload) if callable(output) else output
        if not isinstance(result, dict):
            raise AgentOutputError(f"Output for {role} must be a dictionary")
        return result.copy()
