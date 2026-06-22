class DevotionalEngineError(Exception):
    """Base engine error."""


class AgentOutputError(DevotionalEngineError):
    """Raised when an adapter output is missing or malformed."""


class ValidationError(DevotionalEngineError):
    """Raised when structured data violates a contract."""
