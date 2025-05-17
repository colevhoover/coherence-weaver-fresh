"""
Protocols Package

This package contains specialized protocols for agent-to-agent interactions,
including first contact, collaboration, and trust establishment.
"""

from coherence_weaver.src.protocols.first_contact import FirstContactProtocol
from coherence_weaver.src.protocols.task_orchestration import TaskOrchestration

__all__ = [
    'FirstContactProtocol',
    'TaskOrchestration'
]
