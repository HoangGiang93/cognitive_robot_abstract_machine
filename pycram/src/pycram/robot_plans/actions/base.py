from __future__ import annotations

import abc
import logging
from abc import ABC
from dataclasses import dataclass

from typing_extensions import Any, Optional, Callable

from pycram.failures import PlanFailure

logger = logging.getLogger(__name__)


@dataclass
class ActionDescription:

    def perform(self) -> Any:
        """
        Full execution: pre-check, plan, post-check
        """
        logger.info(f"Performing action {self.__class__.__name__}")

        for pre_cb in self._pre_perform_callbacks:
            pre_cb(self)

        self.validate_precondition()

        result = None
        try:
            result = self.execute()
        except PlanFailure as e:
            raise e
        finally:
            for post_cb in self._post_perform_callbacks:
                post_cb(self)

            self.validate_postcondition(result)

        return result

    @abc.abstractmethod
    def execute(self) -> Any:
        """
        Symbolic plan. Should only call motions or sub-actions.
        """
        pass

    @abc.abstractmethod
    def validate_precondition(self):
        """
        Symbolic/world state precondition validation.
        """
        pass

    @abc.abstractmethod
    def validate_postcondition(self, result: Optional[Any] = None):
        """
        Symbolic/world state postcondition validation.
        """
        pass

    @classmethod
    def pre_perform(cls, func) -> Callable:
        cls._pre_perform_callbacks.append(func)
        return func

    @classmethod
    def post_perform(cls, func) -> Callable:
        cls._post_perform_callbacks.append(func)
        return func
