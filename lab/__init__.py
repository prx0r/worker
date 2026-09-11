"""Lab intelligence — reflection, promotion, discovery, evaluation, pipeline.

Integration: tries private-lab contracts first (canonical), falls back to local.
"""
import sys
from pathlib import Path

# Ensure private-lab is importable
_private_lab = str(Path("/root/private-lab"))
if _private_lab not in sys.path:
    sys.path.insert(0, _private_lab)

try:
    # Prefer private-lab contracts (canonical, frozen, tested)
    from lab.contracts import (
        EvaluationResult as _PLEvaluationResult,
        ExperimentResult as _PLExperimentResult,
    )
    from lab.evaluation import RunEvaluator, RunMetrics
    from lab.curriculum import CurriculumEngine, CurriculumState
    from lab.ledger import Ledger
    from lab.artifacts import ArtifactStore

    # Re-export private-lab types as the canonical ones
    ExperimentResult = _PLExperimentResult

    # Wrap private-lab EvaluationResult to match workerkit's interface
    class EvaluationResult:
        """Bridge: wraps private-lab EvaluationResult for workerkit compatibility."""
        def __init__(self, **kwargs):
            self._inner = _PLEvaluationResult(**kwargs)
        def __getattr__(self, name):
            return getattr(self._inner, name)

except ImportError:
    # Fall back to workerkit's own lab module
    try:
        from lab.reflection import ReflectionPipeline, CandidateLesson, ExperimentResult
        from lab.discovery import LabDiscovery
        from lab.context import LabContext
        from lab.evaluator import Evaluator, EvaluationResult, DimensionScore, format_report, format_comparison
        from lab.brief import StructuredBrief
        from lab.trajectory import Trajectory, TrajectoryRecord, events_to_trajectory
    except ImportError:
        try:
            from workerkit.lab.reflection import ReflectionPipeline, CandidateLesson, ExperimentResult
            from workerkit.lab.discovery import LabDiscovery
            from workerkit.lab.context import LabContext
            from workerkit.lab.evaluator import Evaluator, EvaluationResult, DimensionScore, format_report, format_comparison
            from workerkit.lab.brief import StructuredBrief
            from workerkit.lab.trajectory import Trajectory, TrajectoryRecord, events_to_trajectory
        except ImportError:
            pass

__all__ = [
    "ReflectionPipeline", "CandidateLesson", "ExperimentResult",
    "LabDiscovery", "LabContext",
    "Evaluator", "EvaluationResult", "DimensionScore", "format_report", "format_comparison",
    "StructuredBrief",
    "Trajectory", "TrajectoryRecord", "events_to_trajectory",
    "RunEvaluator", "RunMetrics", "CurriculumEngine", "CurriculumState",
    "Ledger", "ArtifactStore",
]
