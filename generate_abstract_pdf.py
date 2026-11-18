"""
Generates an elegant, publication-grade 1-PAGE Project Abstract PDF
for submission to Dr. Pooja Batra (10 Marks Evaluation).
Course: Version Control Systems (VCS)
Students: Satvik Sureka, Samarth Mahajan, Gourang Jawa, Vedansh Dhawana
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
import pypdf


def build_abstract_pdf(output_filename="AI_Metadata_Detector_1Page_Abstract.pdf"):
    # Page dimensions: 8.5 x 11 inches = 612 x 792 pt
    # Margins: 30 pt left/right, 28 pt top/bottom -> usable width = 552 pt, usable height = 736 pt
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=26,
        bottomMargin=26
    )

    PRIMARY = colors.HexColor("#0F172A")    # Deep Navy
    SECONDARY = colors.HexColor("#0284C7")  # Tech Blue
    DARK_TEXT = colors.HexColor("#1E293B")  # Slate Dark
    LIGHT_BG = colors.HexColor("#F8FAFC")   # Crisp Light Gray
    BORDER_CLR = colors.HexColor("#CBD5E1") # Border
    ACCENT_GREEN = colors.HexColor("#0D9488")
    ACCENT_RED = colors.HexColor("#DC2626")

    styles = getSampleStyleSheet()

    # Base typography
    title_style = ParagraphStyle(
        'AbTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=PRIMARY,
        alignment=1  # Centered
    )

    subtitle_style = ParagraphStyle(
        'AbSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=SECONDARY,
        alignment=1
    )

    sec_hdr_style = ParagraphStyle(
        'SecHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=PRIMARY,
        spaceBefore=0,
        spaceAfter=2
    )

    sec_hdr_right = ParagraphStyle(
        'SecHdrR',
        parent=sec_hdr_style,
        textColor=SECONDARY
    )

    body_style = ParagraphStyle(
        'AbBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.8,
        textColor=DARK_TEXT,
        spaceAfter=3
    )

    body_bold = ParagraphStyle(
        'AbBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'AbCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.8,
        textColor=PRIMARY
    )

    story = []

    # =========================================================================
    # HEADER BANNER & ACADEMIC CREDENTIALS
    # =========================================================================
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING | B.TECH (2ND YEAR)", subtitle_style))
    story.append(Paragraph("PROJECT ABSTRACT: AI METADATA DETECTOR (AIMetaDetect)", title_style))
    story.append(Paragraph("Digital Media Forensics, Provenance Auditing & Version Control System (VCS) Implementation", subtitle_style))
    story.append(Spacer(1, 4))

    # Academic credentials bar table
    meta_data = [
        [
            Paragraph("<b>Course:</b> Version Control Systems (VCS) Lab", body_style),
            Paragraph("<b>Faculty Mentor / Evaluator:</b> <b>Dr. Pooja Batra</b>", body_style),
            Paragraph("<b>Evaluation Weightage:</b> <b>10 Marks</b>", body_style)
        ],
        [
            Paragraph("<b>Team Lead:</b> Satvik Sureka (<b>2581276</b>)", body_style),
            Paragraph("<b>Members:</b> Samarth Mahajan (<b>2581419</b>), Gourang Jawa (<b>2581080</b>)", body_style),
            Paragraph("<b>Member:</b> Vedansh Dhawana (<b>2581314</b>)", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[184, 218, 150])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_CLR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    # =========================================================================
    # EXECUTIVE ABSTRACT & KEYWORDS BOX
    # =========================================================================
    abstract_text = (
        "<b>Executive Abstract:</b> With the proliferation of generative artificial intelligence (GenAI), distinguishing synthetic "
        "media from authentic human creations is an urgent imperative for academic integrity, copyright attribution, and misinformation deterrence. "
        "<b>AIMetaDetect</b> is a lightweight, zero-network digital forensics tool developed in Python that parses raw multimedia and document binaries "
        "(PNG, JPEG, WebP, PDF, MP3) to uncover embedded generation parameters, prompts, model checkpoint hashes, and cryptographic provenance "
        "manifests (C2PA/IPTC). Concurrently developed as a cornerstone submission for the <b>Version Control Systems (VCS)</b> curriculum, "
        "the project demonstrates end-to-end Git lifecycle management, atomic commit practices, feature-branch isolation, merging, and GitHub remote synchronization."
    )
    keywords_text = "<b>Keywords:</b> Generative AI Forensics, Metadata Auditing, PNG Chunks, C2PA, Distributed VCS, Git CLI, GitHub Workflow."

    abs_box_data = [
        [Paragraph(abstract_text, body_style)],
        [Paragraph(keywords_text, ParagraphStyle('Kw', parent=body_style, textColor=SECONDARY, fontName='Helvetica-Bold'))]
    ]
    abs_box = Table(abs_box_data, colWidths=[552])
    abs_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F9FF")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#38BDF8")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(abs_box)
    story.append(Spacer(1, 5))

    # =========================================================================
    # 2-COLUMN CORE BODY (Left: Project Forensics | Right: VCS Implementation)
    # =========================================================================
    # LEFT COLUMN: Technical Forensics
    left_flowables = [
        Paragraph("1. PROBLEM STATEMENT & OBJECTIVES", sec_hdr_style),
        Paragraph(
            "Deepfake visual classifiers suffer from significant computational latency, high false-positive rates on natural images, "
            "and act as unexplainable black boxes. <b>Objective:</b> Construct a deterministic, explainable, and local forensic analyzer "
            "that inspects standard file header chunks (EXIF, XMP, PNG metadata) without sending private user data to third-party cloud APIs.",
            body_style
        ),
        Spacer(1, 2),

        Paragraph("2. TARGET AI ECOSYSTEM & FORENSIC SIGNATURES", sec_hdr_style),
    ]

    # Signature mini-table
    sig_mini_data = [
        [Paragraph("<b>Target Framework</b>", body_bold), Paragraph("<b>Metadata Header / Chunk</b>", body_bold), Paragraph("<b>Forensic Evidence Recovered</b>", body_bold)],
        [
            Paragraph("Stable Diffusion (A1111)", body_style),
            Paragraph("PNG <code>tEXt:parameters</code>", code_style),
            Paragraph("Prompts, seed, sampler, steps, model hash", body_style)
        ],
        [
            Paragraph("ComfyUI Graphs", body_style),
            Paragraph("PNG <code>prompt/workflow</code>", code_style),
            Paragraph("JSON node graph (KSampler, CLIP encoders)", body_style)
        ],
        [
            Paragraph("Adobe Firefly / GenAI", body_style),
            Paragraph("XMP <code>IPTC:DigitalSourceType</code>", code_style),
            Paragraph("<code>trainedAlgorithmicMedia</code> assertion", body_style)
        ],
        [
            Paragraph("DALL-E 3 / Midjourney", body_style),
            Paragraph("EXIF / <code>urn:c2pa</code> box", code_style),
            Paragraph("Cryptographic Content Credentials manifest", body_style)
        ],
        [
            Paragraph("ChatGPT / Claude PDFs", body_style),
            Paragraph("PDF <code>/Producer</code> & text", code_style),
            Paragraph("Software tags & conversational disclaimers", body_style)
        ],
        [
            Paragraph("Suno / Udio AI Music", body_style),
            Paragraph("ID3v2 & RIFF chunks", code_style),
            Paragraph("AI audio encoder tags (e.g. 'Suno v3.5 AI')", body_style)
        ]
    ]
    sig_mini_table = Table(sig_mini_data, colWidths=[80, 85, 103])
    sig_mini_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER_CLR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.8),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    left_flowables.append(sig_mini_table)
    left_flowables.append(Spacer(1, 3))

    left_flowables.extend([
        Paragraph("3. SYSTEM ARCHITECTURE & SCORING ALGORITHM", sec_hdr_style),
        Paragraph(
            "The architecture applies the <b>Factory / Facade Design Pattern</b> (<code>aimeta/engine.py</code>) routing inputs to specialized "
            "detectors (<code>image_detector.py</code>, <code>document_detector.py</code>, <code>audio_detector.py</code>). "
            "Confidence is computed via independent probabilistic union:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Confidence = (1 - &prod;<sub>i</sub> (1 - w<sub>i</sub> &times; 0.95)) &times; 100%</b><br/>"
            "Verdicts: <b>AI_GENERATED</b> (&ge;80%), <b>LIKELY_AI</b> (&ge;60%), <b>SUSPICIOUS</b> (&ge;35%), or <b>NATURAL_OR_STRIPPED</b> (&lt;35%).",
            body_style
        ),
        Spacer(1, 2),
        Paragraph("4. DUAL USER INTERFACES", sec_hdr_style),
        Paragraph(
            "• <b>Rich CLI:</b> Formatted tables, colored badges, JSON exports (<code>python main.py scan/batch</code>).<br/>"
            "• <b>Tkinter GUI:</b> Desktop interface for interactive file browsing & live demo (<code>python gui.py</code>).",
            body_style
        )
    ])

    # RIGHT COLUMN: VCS & Git Implementation
    right_flowables = [
        Paragraph("5. VERSION CONTROL SYSTEMS (VCS) IMPLEMENTATION", sec_hdr_right),
        Paragraph(
            "To model professional multi-contributor engineering standards, the project strictly utilized <b>basic Git CLI commands</b> "
            "and a trunk-based feature-branching workflow on GitHub:",
            body_style
        ),
    ]

    git_table_data = [
        [Paragraph("<b>Git CLI Command</b>", body_bold), Paragraph("<b>Operational Function & Git Internals</b>", body_bold)],
        [
            Paragraph("<code>git init</code>", code_style),
            Paragraph("Initializes local repository, creating <code>.git</code> object database.", body_style)
        ],
        [
            Paragraph("<code>git status</code>", code_style),
            Paragraph("Compares Working Tree vs Staging Index via SHA-1 file hashes.", body_style)
        ],
        [
            Paragraph("<code>git add .</code>", code_style),
            Paragraph("Compresses files into zlib 'blob' objects and updates <code>.git/index</code>.", body_style)
        ],
        [
            Paragraph("<code>git commit -m</code>", code_style),
            Paragraph("Creates atomic 'commit' & 'tree' objects, advancing branch ref.", body_style)
        ],
        [
            Paragraph("<code>git branch -M main</code>", code_style),
            Paragraph("Establishes 'main' as the primary production-ready branch.", body_style)
        ],
        [
            Paragraph("<code>git checkout -b &lt;f&gt;</code>", code_style),
            Paragraph("Isolates development into feature branches (e.g. <code>feature/detectors</code>).", body_style)
        ],
        [
            Paragraph("<code>git merge &lt;f&gt;</code>", code_style),
            Paragraph("Integrates verified feature branch commits back into main.", body_style)
        ],
        [
            Paragraph("<code>git remote add</code>", code_style),
            Paragraph("Binds local repo to GitHub origin: <code>satvik77x/ai-metadata-detector</code>.", body_style)
        ],
        [
            Paragraph("<code>git push -u origin</code>", code_style),
            Paragraph("Transfers commit packfiles to GitHub and sets upstream tracking.", body_style)
        ],
        [
            Paragraph("<code>git log --oneline</code>", code_style),
            Paragraph("Visualizes Directed Acyclic Graph (DAG) commit history.", body_style)
        ]
    ]
    git_mini_table = Table(git_table_data, colWidths=[90, 178])
    git_mini_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284C7")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER_CLR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    right_flowables.append(git_mini_table)
    right_flowables.append(Spacer(1, 3))

    right_flowables.extend([
        Paragraph("6. EXPERIMENTAL RESULTS & TEST VERIFICATION", sec_hdr_right),
        Paragraph(
            "<b>Automated Unit Tests (tests/test_detector.py):</b> 6/6 tests passed in <b>0.036 seconds</b>.<br/>"
            "• <i>Stable Diffusion PNG:</i> <b>99.13%</b> Confidence | Extracted Prompt: 'cyberpunk street...'<br/>"
            "• <i>Adobe Firefly JPEG:</i> <b>99.90%</b> Confidence | IPTC algorithmic media detected.<br/>"
            "• <i>ChatGPT PDF:</i> <b>99.00%</b> Confidence | Producer tag & conversational tropes matched.<br/>"
            "• <i>Natural Canon DSLR:</i> <b>5.00%</b> Confidence | Correctly classified as NATURAL.",
            body_style
        ),
        Spacer(1, 2),
        Paragraph("7. REPOSITORY & SUBMISSION DELIVERABLES", sec_hdr_right),
        Paragraph(
            "<b>GitHub Repository:</b> <code>https://github.com/satvik77x/ai-metadata-detector</code><br/>"
            "<b>Deliverables:</b> Complete Python source code, Tkinter GUI, 13-slide PPTX presentation, 8-page comprehensive report, and this 1-page executive abstract.",
            body_style
        )
    ])

    # Package into 2-column layout table
    two_col_table = Table([[left_flowables, right_flowables]], colWidths=[271, 271])
    two_col_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (0, 0), (0, 0), 4),
        ('LEFTPADDING', (1, 0), (1, 0), 4),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(two_col_table)
    story.append(Spacer(1, 3))

    # =========================================================================
    # FOOTER / ACKNOWLEDGMENT BAR
    # =========================================================================
    ack_data = [[
        Paragraph(
            "<b>Faculty Guide:</b> Dr. Pooja Batra  |  <b>Team:</b> Satvik Sureka (2581276), Samarth Mahajan (2581419), Gourang Jawa (2581080), Vedansh Dhawana (2581314)  |  <b>B.Tech CSE (2nd Year)</b>",
            ParagraphStyle('Ack', parent=body_style, fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=colors.HexColor("#475569"), alignment=1)
        )
    ]]
    ack_table = Table(ack_data, colWidths=[552])
    ack_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(ack_table)

    # Build PDF
    doc.build(story)
    print(f"[+] Successfully generated: {output_filename}")

    # Check page count
    reader = pypdf.PdfReader(output_filename)
    page_count = len(reader.pages)
    print(f"[+] Total Pages in PDF: {page_count}")
    return page_count


if __name__ == "__main__":
    count = build_abstract_pdf()
    if count != 1:
        print(f"[!] WARNING: Expected 1 page but got {count} pages!")
    else:
        print("[✓] EXACTLY 1 PAGE CONFIRMED!")
