"""Abstract base class for Command pattern."""

from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """Abstract base class for all commands.

    Each command encapsulates a single operation that can be executed.
    Commands receive the storage instance via dependency injection.
    """

    @abstractmethod
    def execute(self) -> Any:
        """Execute the command and return result.

        Returns:
            Result of the command execution (varies by command type)
        """
        pass
