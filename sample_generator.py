"""
Sample Generator for AIMetaDetect
Creates authentic test media samples with various metadata headers (AI vs Natural).
"""

import os
from PIL import Image, PngImagePlugin
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_sample_files(output_dir: str = "samples"):
    os.makedirs(output_dir, exist_ok=True)

    # 1. Stable Diffusion Sample (PNG with 'parameters' chunk)
    sd_img = Image.new("RGB", (256, 256), color=(45, 85, 125))
    meta_png = PngImagePlugin.PngInfo()
    sd_prompt_meta = (
        "cyberpunk street at night, neon lights, ultra realistic 8k octane render, cinematic lighting\n"
        "Negative prompt: low quality, blurry, distorted, watermark\n"
        "Steps: 28, Sampler: DPM++ 2M Karras, CFG scale: 7.5, Seed: 384729104, Size: 512x512, "
        "Model hash: a9f84b61, Model: v1-5-pruned-emaonly"
    )
    meta_png.add_text("parameters", sd_prompt_meta)
    sd_path = os.path.join(output_dir, "sample_stable_diffusion.png")
    sd_img.save(sd_path, "PNG", pnginfo=meta_png)
    print(f"[+] Created: {sd_path}")

    # 2. ComfyUI Sample (PNG with 'prompt' / 'workflow' chunk)
    comfy_img = Image.new("RGB", (256, 256), color=(80, 50, 110))
    meta_comfy = PngImagePlugin.PngInfo()
    comfy_json = """{
        "3": {"class_type": "KSampler", "inputs": {"seed": 847291, "steps": 20, "cfg": 8.0, "sampler_name": "euler"}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "A futuristic robotic companion in an enchanted forest", "clip": ["4", 1]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}}
    }"""
    meta_comfy.add_text("prompt", comfy_json)
    comfy_path = os.path.join(output_dir, "sample_comfyui.png")
    comfy_img.save(comfy_path, "PNG", pnginfo=meta_comfy)
    print(f"[+] Created: {comfy_path}")

    # 3. Adobe Firefly / C2PA Sample with XMP packet
    firefly_img = Image.new("RGB", (256, 256), color=(200, 70, 50))
    firefly_path = os.path.join(output_dir, "sample_adobe_firefly.jpg")
    firefly_img.save(firefly_path, "JPEG")
    # Append XMP packet with IPTC trainedAlgorithmicMedia tag
    xmp_packet = (
        b'<x:xmpmeta xmlns:x="adobe:ns:meta/">'
        b'<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
        b'<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" '
        b'xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/" '
        b'xmlns:xmp="http://ns.adobe.com/xap/1.0/">'
        b'<xmp:CreatorTool>Adobe Firefly 2.0</xmp:CreatorTool>'
        b'<Iptc4xmpExt:DigitalSourceType>http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia</Iptc4xmpExt:DigitalSourceType>'
        b'</rdf:Description></rdf:RDF></x:xmpmeta>'
    )
    with open(firefly_path, "ab") as f:
        f.write(xmp_packet)
    print(f"[+] Created: {firefly_path}")

    # 4. Natural Camera Image Sample
    natural_img = Image.new("RGB", (256, 256), color=(30, 150, 80))
    natural_path = os.path.join(output_dir, "sample_natural_camera.jpg")
    exif = natural_img.getexif()
    exif[0x010F] = "Canon"  # Make
    exif[0x0110] = "Canon EOS 5D Mark IV"  # Model
    exif[0x0131] = "Firmware Version 1.3.3"  # Software
    natural_img.save(natural_path, "JPEG", exif=exif)
    print(f"[+] Created: {natural_path}")

    # 5. ChatGPT Document Sample (PDF)
    pdf_path = os.path.join(output_dir, "sample_chatgpt_document.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setTitle("Essay on Artificial Intelligence Ethics")
    c.setAuthor("OpenAI / ChatGPT")
    c.setSubject("AI Ethics")
    c.drawString(100, 720, "Ethics of Generative AI")
    c.drawString(100, 690, "Certainly! Here is an essay exploring ethical considerations in modern machine learning.")
    c.drawString(100, 660, "As an AI language model, I do not possess personal consciousness or agency,")
    c.drawString(100, 630, "yet the impact of synthetic media on societal discourse requires careful analysis.")
    c.save()
    print(f"[+] Created: {pdf_path}")

    # 6. Suno AI Music Sample (Dummy MP3 with ID3 header)
    mp3_path = os.path.join(output_dir, "sample_suno_ai.mp3")
    id3_header = b"ID3\x03\x00\x00\x00\x00\x01\x00TIT2\x00\x00\x00\x1f\x00\x00\x03Suno AI Cybernetic SymphonyTPE1\x00\x00\x00\x0e\x00\x00\x03Suno v3.5 AI"
    dummy_audio_bytes = b"\xff\xfb\x90\x00" * 200
    with open(mp3_path, "wb") as f:
        f.write(id3_header + dummy_audio_bytes)
    print(f"[+] Created: {mp3_path}")


if __name__ == "__main__":
    create_sample_files()
