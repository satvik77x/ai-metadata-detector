import os
import re
from typing import Dict, Any, List, Optional
from .models import DetectionResult, MetadataIndicator, Verdict

AUDIO_AI_SIGNATURES = [
    (b"suno", "Suno AI Music", 0.95),
    (b"udio", "Udio AI Music", 0.95),
    (b"elevenlabs", "ElevenLabs AI Voice", 0.98),
    (b"whisper", "OpenAI Whisper / Speech-to-Text", 0.90),
    (b"descript", "Descript Overdub / AI", 0.85),
    (b"synthesizer v", "Dreamtonics Synthesizer V", 0.90),
    (b"vocaloid", "Yamaha Vocaloid", 0.85),
    (b"voicereproducer", "AI Voice Clone", 0.80),
]


class AudioMetadataDetector:
    """Inspects audio files (MP3, WAV, FLAC, M4A) for AI voice and music generator signatures."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filesize = os.path.getsize(filepath)
        self.raw_info: Dict[str, Any] = {}
        self.indicators: List[MetadataIndicator] = []

    def analyze(self) -> DetectionResult:
        ext = os.path.splitext(self.filepath)[1].lower()
        self._scan_audio_headers()

        score, primary_app, verdict = self._evaluate_indicators()

        return DetectionResult(
            filename=os.path.basename(self.filepath),
            file_type=f"Audio ({ext.upper()})",
            file_size_bytes=self.filesize,
            is_ai_generated=(score >= 50.0),
            verdict=verdict,
            confidence_score=round(score, 2),
            primary_ai_app=primary_app,
            detected_indicators=self.indicators,
            raw_metadata=self.raw_info,
            notes=["Scanned ID3v1/ID3v2 tags and RIFF metadata headers for generative audio signatures."]
        )

    def _scan_audio_headers(self):
        try:
            with open(self.filepath, "rb") as f:
                header = f.read(512 * 1024)  # First 512KB
                f.seek(max(0, self.filesize - 128))  # Last 128 bytes for ID3v1
                footer = f.read(128)

            content = header + b" " + footer
            lower_content = content.lower()

            for sig_bytes, app_name, weight in AUDIO_AI_SIGNATURES:
                if sig_bytes in lower_content:
                    self.indicators.append(MetadataIndicator(
                        key=f"AudioTag:{sig_bytes.decode('ascii', errors='ignore')}",
                        value=f"Found signature: {sig_bytes.decode('ascii', errors='ignore')}",
                        source="Audio Metadata / ID3 Frame",
                        app_detected=app_name,
                        confidence_weight=weight,
                        description=f"Audio tag or RIFF comment references '{sig_bytes.decode('ascii', errors='ignore')}'"
                    ))
        except Exception as e:
            self.raw_info["scan_error"] = str(e)

    def _evaluate_indicators(self):
        if not self.indicators:
            return 5.0, None, Verdict.NATURAL_OR_STRIPPED

        weights = [ind.confidence_weight for ind in self.indicators]
        prob = 1.0
        for w in weights:
            prob *= (1.0 - (w * 0.90))
        score = min(max((1.0 - prob) * 100.0, 0.0), 99.0)

        app_counts: Dict[str, float] = {}
        for ind in self.indicators:
            app = ind.app_detected
            app_counts[app] = app_counts.get(app, 0.0) + ind.confidence_weight

        primary_app = max(app_counts.items(), key=lambda x: x[1])[0] if app_counts else "Unknown Audio AI"

        verdict = Verdict.AI_GENERATED if score >= 80.0 else (Verdict.LIKELY_AI if score >= 50.0 else Verdict.NATURAL_OR_STRIPPED)
        return score, primary_app, verdict
