import os
from typing import List, Optional
from .models import DetectionResult, Verdict
from .image_detector import ImageMetadataDetector
from .document_detector import DocumentMetadataDetector
from .audio_detector import AudioMetadataDetector

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"}
DOC_EXTS = {".pdf", ".txt", ".md", ".docx"}
AUDIO_EXTS = {".mp3", ".wav", ".flac", ".m4a", ".ogg"}


class AIMetadataEngine:
    """Master engine for scanning files and folders for AI metadata signatures."""

    @classmethod
    def scan_file(cls, filepath: str) -> DetectionResult:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        ext = os.path.splitext(filepath)[1].lower()

        if ext in IMAGE_EXTS:
            detector = ImageMetadataDetector(filepath)
            return detector.analyze()
        elif ext in DOC_EXTS:
            detector = DocumentMetadataDetector(filepath)
            return detector.analyze()
        elif ext in AUDIO_EXTS:
            detector = AudioMetadataDetector(filepath)
            return detector.analyze()
        else:
            # Fallback to image detector or generic byte scanner
            detector = ImageMetadataDetector(filepath)
            return detector.analyze()

    @classmethod
    def scan_directory(cls, dirpath: str, recursive: bool = True) -> List[DetectionResult]:
        if not os.path.isdir(dirpath):
            raise NotADirectoryError(f"Directory not found: {dirpath}")

        all_extensions = IMAGE_EXTS | DOC_EXTS | AUDIO_EXTS
        results = []

        if recursive:
            for root, _, files in os.walk(dirpath):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in all_extensions:
                        full_path = os.path.join(root, f)
                        try:
                            results.append(cls.scan_file(full_path))
                        except Exception as e:
                            print(f"[Engine] Error scanning {full_path}: {e}")
        else:
            for f in os.listdir(dirpath):
                full_path = os.path.join(dirpath, f)
                if os.path.isfile(full_path):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in all_extensions:
                        try:
                            results.append(cls.scan_file(full_path))
                        except Exception as e:
                            print(f"[Engine] Error scanning {full_path}: {e}")

        return results
