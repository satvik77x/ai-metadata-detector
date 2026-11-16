from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class Verdict(str, Enum):
    AI_GENERATED = "AI_GENERATED"
    LIKELY_AI = "LIKELY_AI"
    SUSPICIOUS = "SUSPICIOUS"
    NATURAL_OR_STRIPPED = "NATURAL_OR_STRIPPED"
    UNKNOWN = "UNKNOWN"


@dataclass
class MetadataIndicator:
    key: str
    value: str
    source: str  # e.g., 'EXIF', 'PNG-chunk', 'XMP', 'PDF-Info', 'ID3'
    app_detected: str  # e.g., 'Stable Diffusion', 'Midjourney', 'DALL-E', 'Adobe Firefly'
    confidence_weight: float  # 0.0 to 1.0
    description: str


@dataclass
class DetectionResult:
    filename: str
    file_type: str
    file_size_bytes: int
    is_ai_generated: bool
    verdict: Verdict
    confidence_score: float  # 0% to 100%
    primary_ai_app: Optional[str] = None
    detected_indicators: List[MetadataIndicator] = field(default_factory=list)
    raw_metadata: Dict[str, Any] = field(default_factory=dict)
    prompt_extracted: Optional[str] = None
    model_name_extracted: Optional[str] = None
    notes: List[str] = field(default_factory=list)
