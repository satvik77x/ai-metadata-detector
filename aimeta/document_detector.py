import os
import re
from typing import Dict, Any, List, Optional
from pypdf import PdfReader
from .models import DetectionResult, MetadataIndicator, Verdict

TEXT_AI_SIGNATURES = [
    ("as an ai language model", "Generic LLM (ChatGPT / OpenAI)", 0.95),
    ("as a large language model", "Generic LLM", 0.95),
    ("i don't have personal opinions", "ChatGPT / Claude", 0.85),
    ("certainly! here is", "ChatGPT / LLM Response boilerplate", 0.70),
    ("sure thing! here is", "ChatGPT boilerplate", 0.70),
    ("in conclusion, it is important to remember that", "LLM Standard Formatter", 0.60),
    ("delve into the multifaceted", "Classic LLM vocabulary trope", 0.65),
    ("it is crucial to consider the nuances", "Classic LLM vocabulary trope", 0.60),
]

PRODUCER_AI_SIGNATURES = [
    ("chatgpt", "ChatGPT Export", 0.98),
    ("openai", "OpenAI Services", 0.95),
    ("anthropic", "Anthropic Claude", 0.95),
    ("claude", "Anthropic Claude", 0.95),
    ("jasper.ai", "Jasper AI", 0.95),
    ("copy.ai", "Copy.ai", 0.95),
    ("notion ai", "Notion AI", 0.92),
    ("gemini", "Google Gemini", 0.95),
]


class DocumentMetadataDetector:
    """Inspects PDF and text documents for AI generator metadata, author tags, and synthetic artifacts."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filesize = os.path.getsize(filepath)
        self.raw_info: Dict[str, Any] = {}
        self.indicators: List[MetadataIndicator] = []
        self.extracted_author: Optional[str] = None
        self.extracted_producer: Optional[str] = None

    def analyze(self) -> DetectionResult:
        ext = os.path.splitext(self.filepath)[1].lower()

        if ext == ".pdf":
            self._analyze_pdf()
        else:
            self._analyze_text_document()

        score, primary_app, verdict = self._evaluate_indicators()

        return DetectionResult(
            filename=os.path.basename(self.filepath),
            file_type=f"Document ({ext.upper()})",
            file_size_bytes=self.filesize,
            is_ai_generated=(score >= 50.0),
            verdict=verdict,
            confidence_score=round(score, 2),
            primary_ai_app=primary_app,
            detected_indicators=self.indicators,
            raw_metadata=self.raw_info,
            prompt_extracted=None,
            model_name_extracted=self.extracted_producer,
            notes=self._generate_notes(verdict, primary_app)
        )

    def _analyze_pdf(self):
        try:
            reader = PdfReader(self.filepath)
            meta = reader.metadata or {}
            
            for key, val in meta.items():
                clean_key = str(key).lstrip("/")
                val_str = str(val)
                self.raw_info[f"pdf:{clean_key}"] = val_str

                if clean_key.lower() == "producer":
                    self.extracted_producer = val_str
                if clean_key.lower() == "author":
                    self.extracted_author = val_str

                # Scan metadata fields against known producers
                lower_val = val_str.lower()
                for sig, app_name, weight in PRODUCER_AI_SIGNATURES:
                    if sig in lower_val:
                        self.indicators.append(MetadataIndicator(
                            key=f"PDF:{clean_key}",
                            value=val_str,
                            source="PDF Metadata Header",
                            app_detected=app_name,
                            confidence_weight=weight,
                            description=f"PDF {clean_key} tag explicitly references '{sig}'"
                        ))

            # Scan first 5 pages of document text for boilerplate AI disclaimer artifacts
            num_pages_to_scan = min(len(reader.pages), 5)
            extracted_sample = ""
            for i in range(num_pages_to_scan):
                extracted_sample += " " + (reader.pages[i].extract_text() or "")

            self._scan_text_body(extracted_sample[:10000])

        except Exception as e:
            self.raw_info["pdf_parse_error"] = str(e)

    def _analyze_text_document(self):
        try:
            with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(15000)
            self._scan_text_body(content)
        except Exception as e:
            self.raw_info["text_read_error"] = str(e)

    def _scan_text_body(self, text: str):
        lower_text = text.lower()
        for phrase, app_name, weight in TEXT_AI_SIGNATURES:
            if phrase in lower_text:
                self.indicators.append(MetadataIndicator(
                    key="TextWatermark",
                    value=f"Found phrase: '{phrase}'",
                    source="Document Body",
                    app_detected=app_name,
                    confidence_weight=weight,
                    description=f"Found explicit AI conversational reflex or phrase: '{phrase}'"
                ))

    def _evaluate_indicators(self):
        if not self.indicators:
            return 5.0, None, Verdict.NATURAL_OR_STRIPPED

        weights = [ind.confidence_weight for ind in self.indicators]
        prob = 1.0
        for w in weights:
            prob *= (1.0 - (w * 0.90))
        score = (1.0 - prob) * 100.0
        score = min(max(score, 0.0), 99.0)

        app_counts: Dict[str, float] = {}
        for ind in self.indicators:
            app = ind.app_detected
            app_counts[app] = app_counts.get(app, 0.0) + ind.confidence_weight

        primary_app = max(app_counts.items(), key=lambda x: x[1])[0] if app_counts else "Unknown LLM"

        if score >= 80.0:
            verdict = Verdict.AI_GENERATED
        elif score >= 55.0:
            verdict = Verdict.LIKELY_AI
        elif score >= 30.0:
            verdict = Verdict.SUSPICIOUS
        else:
            verdict = Verdict.NATURAL_OR_STRIPPED

        return score, primary_app, verdict

    def _generate_notes(self, verdict: Verdict, primary_app: Optional[str]) -> List[str]:
        notes = []
        if verdict in (Verdict.AI_GENERATED, Verdict.LIKELY_AI):
            notes.append(f"Document exhibits characteristic AI metadata or conversational boilerplate associated with {primary_app}.")
        else:
            notes.append("No explicit AI conversational markers or generator software tags discovered.")
        return notes
