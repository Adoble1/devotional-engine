from dataclasses import dataclass, field

from .agents import AgentAdapter
from .config import ROLE_CONFIG
from .exceptions import AgentOutputError


@dataclass
class ExternalModelAdapterConfig:
    provider: str
    model_by_role: dict[str, str]
    timeout_seconds: float = 30.0
    max_retries: int = 2
    role_config: dict = field(default_factory=lambda: ROLE_CONFIG.copy())


class UnconfiguredExternalModelAdapter(AgentAdapter):
    def __init__(self, config: ExternalModelAdapterConfig):
        self.config = config

    def call(self, role: str, payload: dict) -> dict:
        raise AgentOutputError(
            f"External model adapter for {self.config.provider!r} is not configured for role {role!r}"
        )


def validate_external_adapter_config(config: ExternalModelAdapterConfig) -> list[str]:
    failures = []
    if not config.provider.strip():
        failures.append("provider is required")
    if config.timeout_seconds <= 0:
        failures.append("timeout_seconds must be positive")
    if config.max_retries < 0:
        failures.append("max_retries cannot be negative")
    missing_roles = sorted(set(ROLE_CONFIG) - set(config.model_by_role))
    if missing_roles:
        failures.append("model_by_role missing roles: " + ", ".join(missing_roles))
    return failures
