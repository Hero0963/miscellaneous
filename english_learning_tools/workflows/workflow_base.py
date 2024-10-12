"""
workflow_base.py

This module defines the abstract WorkflowBase class, which serves as a base class
for different workflow implementations.
"""

import logging
from abc import ABC, abstractmethod


class WorkflowBase(ABC):
    def __init__(self):
        logging.debug("Initializing base workflow")

    @abstractmethod
    def execute(self):
        pass
