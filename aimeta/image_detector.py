import os
import re
import json
from typing import Dict, Any, List, Optional
from PIL import Image, ExifTags
from .models import DetectionResult, MetadataIndicator, Verdict

# Known signatures for various AI Generators
AI_APP_SIGNATURES = {
    "Stable Diffusion (A1111/WebUI)": [
        "steps: ", "sampler: ", "cfg scale: ", "seed: ", "model hash: ", 
        "negative prompt: ", "clip skip: ", "ensd: "
    ],
    "ComfyUI": [
        "\"class_type\": \"ksampler\"", "\"class_type\": \"cliptextencode\"", 
        "\"class_type\": \"checkpointloadersimple\"", "\"comfyui\""
    ],
    "NovelAI": [
        "novelai", "nai diffusion", "curated", "anime (full)"
    ],
    "Adobe Firefly / Photoshop GenAI": [
        "adobe firefly", "generative fill", "generative expand",
        "trainedalgorithmicmedia", "compositesynthetic"
    ],
    "Midjourney": [
        "midjourney", "--v 5", "--v 6", "--ar ", "--stylize ", "--chaos "
    ],
    "DALL-E / Bing Image Creator": [
        "dall·e", "dalle", "bing image creator", "openai"
    ],
    "Fooocus": [
        "fooocus", "base model: ", "refiner model: "
    ],
    "Google Imagen / SynthID": [
        "imagen", "synthid", "deepmind"
    ]
}


class ImageMetadataDetector:
    """Inspects EXIF, PNG chunks, and XMP packets in raster images."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filesize = os.path.getsize(filepath)
        self.raw_info: Dict[str, Any] = {}
        self.indicators: List[MetadataIndicator] = []
        self.extracted_prompt: Optional[str] = None
        self.extracted_model: Optional[str] = None

    def analyze(self) -> DetectionResult:
        with Image.open(self.filepath) as img:
            file_format = img.format or "IMAGE"
            # 1. Inspect PIL info dict (contains PNG text chunks, etc.)
            self._inspect_image_info(img)
            # 2. Inspect EXIF
            self._inspect_exif(img)
            # 3. Inspect Raw Binary for XMP and C2PA markers
            self._inspect_raw_bytes()

        # Compute overall confidence score and verdict
        score, primary_app, verdict = self._evaluate_indicators()

        return DetectionResult(
            filename=os.path.basename(self.filepath),
            file_type=f"Image ({file_format})",
            file_size_bytes=self.filesize,
            is_ai_generated=(score >= 50.0),
            verdict=verdict,
            confidence_score=round(score, 2),
            primary_ai_app=primary_app,
            detected_indicators=self.indicators,
            raw_metadata=self.raw_info,
            prompt_extracted=self.extracted_prompt,
            model_name_extracted=self.extracted_model,
            notes=self._generate_summary_notes(verdict, primary_app)
        )

    def _inspect_image_info(self, img: Image.Image):
        """Inspects PNG chunks (tEXt, zTXt, iTXt) and other dictionary info."""
        for key, val in img.info.items():
            if isinstance(val, (bytes, bytearray)):
                try:
                    val_str = val.decode("utf-8", errors="ignore")
                except Exception:
                    val_str = repr(val)
            else:
                val_str = str(val)

            self.raw_info[f"info:{key}"] = val_str

            # Check for Stable Diffusion 'parameters' chunk
            if key.lower() == "parameters":
                self.indicators.append(MetadataIndicator(
                    key="PNG:parameters",
                    value=val_str[:300] + ("..." if len(val_str) > 300 else ""),
                    source="PNG Text Chunk",
                    app_detected="Stable Diffusion (Automatic1111 / WebUI)",
                    confidence_weight=0.98,
                    description="Standard Automatic1111 generation parameters including prompt, seed, and sampler"
                ))
                self._parse_sd_parameters(val_str)

            # Check for ComfyUI workflow / prompt chunks
            elif key.lower() in ("prompt", "workflow"):
                if "ksampler" in val_str.lower() or "cliptextencode" in val_str.lower() or "comfyui" in val_str.lower():
                    self.indicators.append(MetadataIndicator(
                        key=f"PNG:{key}",
                        value=val_str[:250] + "...",
                        source="PNG Text Chunk",
                        app_detected="ComfyUI",
                        confidence_weight=0.99,
                        description="ComfyUI node execution graph embedded in PNG chunk"
                    ))
                    self._parse_comfyui_json(val_str)

            # Check for NovelAI Comment
            elif key.lower() == "comment" and ("novelai" in val_str.lower() or "steps" in val_str.lower()):
                self.indicators.append(MetadataIndicator(
                    key="PNG:Comment",
                    value=val_str[:200],
                    source="PNG Comment Chunk",
                    app_detected="NovelAI / Anime Diffusion",
                    confidence_weight=0.95,
                    description="NovelAI generation metadata stored in PNG Comment chunk"
                ))

            # General substring search on any chunk
            self._scan_text_for_ai_signatures(val_str, source=f"PNG chunk '{key}'")

    def _inspect_exif(self, img: Image.Image):
        """Inspects EXIF tags if present in JPEG/TIFF/PNG."""
        try:
            exif_data = img.getexif()
            if not exif_data:
                return

            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                val_str = str(value)
                self.raw_info[f"exif:{tag_name}"] = val_str

                # Check specific EXIF tags often modified or written by AI tools
                if tag_name.lower() in ("software", "artist", "usercomment", "imagedescription", "copyright"):
                    self._scan_text_for_ai_signatures(val_str, source=f"EXIF:{tag_name}")

                # Check if camera make/model is present (camera presence lowers AI likelihood unless overridden)
                if tag_name.lower() in ("make", "model"):
                    self.raw_info["camera_hardware"] = f"{tag_name}: {val_str}"

        except Exception as e:
            self.raw_info["exif_error"] = str(e)

    def _inspect_raw_bytes(self):
        """Scans raw file bytes for XMP packets, C2PA manifests, and IPTC AI assertions."""
        try:
            with open(self.filepath, "rb") as f:
                content = f.read(5 * 1024 * 1024)  # Scan first 5MB

            # 1. Search for XMP metadata packet
            xmp_match = re.search(rb"<x:xmpmeta[\s\S]*?</x:xmpmeta>", content)
            if xmp_match:
                xmp_text = xmp_match.group(0).decode("utf-8", errors="ignore")
                self.raw_info["xmp_packet_found"] = True

                # Check IPTC DigitalSourceType for AI indicators
                if "trainedAlgorithmicMedia" in xmp_text:
                    self.indicators.append(MetadataIndicator(
                        key="XMP:DigitalSourceType",
                        value="trainedAlgorithmicMedia",
                        source="XMP / IPTC Photo Metadata",
                        app_detected="Generative AI (IPTC Standard)",
                        confidence_weight=0.99,
                        description="Official IPTC Digital Source Type indicating content was synthesized using trained AI models"
                    ))
                elif "compositeSynthetic" in xmp_text:
                    self.indicators.append(MetadataIndicator(
                        key="XMP:DigitalSourceType",
                        value="compositeSynthetic",
                        source="XMP / IPTC Photo Metadata",
                        app_detected="Generative AI (Synthetic Composite)",
                        confidence_weight=0.85,
                        description="IPTC tag indicating image contains synthetic composite elements"
                    ))

                # Check Adobe Firefly markers in XMP
                if "firefly" in xmp_text.lower() or "generative fill" in xmp_text.lower():
                    self.indicators.append(MetadataIndicator(
                        key="XMP:CreatorTool",
                        value="Adobe Firefly / Photoshop GenAI",
                        source="XMP Packet",
                        app_detected="Adobe Firefly",
                        confidence_weight=0.96,
                        description="Adobe Photoshop Generative Fill or Adobe Firefly signature in XMP stream"
                    ))

                # Scan XMP text generally
                self._scan_text_for_ai_signatures(xmp_text, source="XMP Packet")

            # 2. Check for C2PA (Coalition for Content Provenance and Authenticity) signatures
            if b"c2pa" in content or b"urn:c2pa" in content:
                self.indicators.append(MetadataIndicator(
                    key="Binary:C2PA_Manifest",
                    value="urn:c2pa signature present",
                    source="C2PA / CAI Manifest Box",
                    app_detected="Content Credentials (C2PA)",
                    confidence_weight=0.90,
                    description="Cryptographic provenance manifest found (used by DALL-E 3, Adobe, Leica, Truepic)"
                ))

        except Exception as e:
            self.raw_info["raw_scan_error"] = str(e)

    def _scan_text_for_ai_signatures(self, text: str, source: str):
        """Scans arbitrary metadata string against known signatures."""
        lower_text = text.lower()
        for app, signatures in AI_APP_SIGNATURES.items():
            matches = [sig for sig in signatures if sig in lower_text]
            if len(matches) >= 2 or (len(matches) == 1 and len(matches[0]) > 6):
                self.indicators.append(MetadataIndicator(
                    key=f"SignatureMatch({matches[0]})",
                    value=f"Matched: {', '.join(matches[:3])}",
                    source=source,
                    app_detected=app,
                    confidence_weight=0.92,
                    description=f"Matched recurring keyword pattern typical for {app}"
                ))

    def _parse_sd_parameters(self, params_text: str):
        """Extracts prompt and model parameters from Automatic1111 format."""
        lines = params_text.strip().split("\n")
        if lines:
            self.extracted_prompt = lines[0].strip()

        # Check for model name
        model_match = re.search(r"Model:\s*([^,\n]+)", params_text)
        if model_match:
            self.extracted_model = model_match.group(1).strip()

    def _parse_comfyui_json(self, json_text: str):
        """Parses ComfyUI workflow JSON to retrieve prompt and model if possible."""
        try:
            data = json.loads(json_text)
            if isinstance(data, dict):
                # Search for CLIPTextEncode text
                for node_id, node_data in data.items():
                    if isinstance(node_data, dict):
                        inputs = node_data.get("inputs", {})
                        if "text" in inputs and isinstance(inputs["text"], str):
                            if len(inputs["text"].strip()) > 5 and not self.extracted_prompt:
                                self.extracted_prompt = inputs["text"].strip()
                        if "ckpt_name" in inputs:
                            self.extracted_model = inputs["ckpt_name"]
        except Exception:
            pass

    def _evaluate_indicators(self):
        """Calculates combined confidence score, primary app, and final verdict."""
        if not self.indicators:
            # Check if camera hardware tags are present
            if "camera_hardware" in self.raw_info:
                return 5.0, None, Verdict.NATURAL_OR_STRIPPED
            return 10.0, None, Verdict.NATURAL_OR_STRIPPED

        # Weight calculation
        weights = [ind.confidence_weight for ind in self.indicators]
        # Independent probability combination formula: 1 - prod(1 - w)
        prob = 1.0
        for w in weights:
            prob *= (1.0 - (w * 0.95))
        score = (1.0 - prob) * 100.0
        score = min(max(score, 0.0), 99.9)

        # Primary application votes
        app_counts: Dict[str, float] = {}
        for ind in self.indicators:
            app = ind.app_detected
            app_counts[app] = app_counts.get(app, 0.0) + ind.confidence_weight

        primary_app = max(app_counts.items(), key=lambda x: x[1])[0] if app_counts else "Unknown AI"

        if score >= 85.0:
            verdict = Verdict.AI_GENERATED
        elif score >= 60.0:
            verdict = Verdict.LIKELY_AI
        elif score >= 35.0:
            verdict = Verdict.SUSPICIOUS
        else:
            verdict = Verdict.NATURAL_OR_STRIPPED

        return score, primary_app, verdict

    def _generate_summary_notes(self, verdict: Verdict, primary_app: Optional[str]) -> List[str]:
        notes = []
        if verdict == Verdict.AI_GENERATED:
            notes.append(f"Strong cryptographic or metadata signatures identify this file as generated by {primary_app}.")
            if self.extracted_prompt:
                notes.append("Original generation prompt was successfully extracted from embedded metadata.")
            if self.extracted_model:
                notes.append(f"AI Checkpoint/Model identified: {self.extracted_model}")
        elif verdict == Verdict.NATURAL_OR_STRIPPED:
            notes.append("No explicit AI generator metadata chunks found.")
            notes.append("Note: Modern social media platforms (Twitter, Instagram, WhatsApp) often strip all EXIF/metadata.")
        return notes
