import unittest
import os
from aimeta.engine import AIMetadataEngine
from aimeta.models import Verdict


class TestAIMetadataDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure sample files exist
        if not os.path.exists("samples/sample_stable_diffusion.png"):
            from sample_generator import create_sample_files
            create_sample_files("samples")

    def test_stable_diffusion_detection(self):
        res = AIMetadataEngine.scan_file("samples/sample_stable_diffusion.png")
        self.assertTrue(res.is_ai_generated)
        self.assertEqual(res.verdict, Verdict.AI_GENERATED)
        self.assertGreater(res.confidence_score, 80.0)
        self.assertIn("Stable Diffusion", res.primary_ai_app)
        self.assertIsNotNone(res.prompt_extracted)
        self.assertIn("cyberpunk", res.prompt_extracted.lower())

    def test_comfyui_detection(self):
        res = AIMetadataEngine.scan_file("samples/sample_comfyui.png")
        self.assertTrue(res.is_ai_generated)
        self.assertEqual(res.verdict, Verdict.AI_GENERATED)
        self.assertIn("ComfyUI", res.primary_ai_app)

    def test_natural_camera_negative(self):
        res = AIMetadataEngine.scan_file("samples/sample_natural_camera.jpg")
        self.assertFalse(res.is_ai_generated)
        self.assertEqual(res.verdict, Verdict.NATURAL_OR_STRIPPED)
        self.assertLess(res.confidence_score, 30.0)

    def test_adobe_firefly_xmp(self):
        res = AIMetadataEngine.scan_file("samples/sample_adobe_firefly.jpg")
        self.assertTrue(res.is_ai_generated)
        self.assertGreater(res.confidence_score, 80.0)

    def test_pdf_chatgpt_detection(self):
        res = AIMetadataEngine.scan_file("samples/sample_chatgpt_document.pdf")
        self.assertTrue(res.is_ai_generated)
        self.assertGreater(res.confidence_score, 80.0)

    def test_audio_suno_detection(self):
        res = AIMetadataEngine.scan_file("samples/sample_suno_ai.mp3")
        self.assertTrue(res.is_ai_generated)
        self.assertIn("Suno", res.primary_ai_app)


if __name__ == "__main__":
    unittest.main()
