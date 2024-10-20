"""
yt_flow_params.py

This module defines various parameter classes related to workflows.
It encapsulates options for fetching content, specifying audio paths, and
determining evaluation methods, along with other workflow-related configurations.
"""

from dataclasses import (
    dataclass,
    field
)


@dataclass
class YTFlowParams:
    yt_url: str
    recorded_audio_path: str
    fetch_content: list = field(default_factory=lambda: ["audio", "vtt"])
    use_content: str = "audio"
    evaluation_method: str = "naive"
    output_folder: str = None
