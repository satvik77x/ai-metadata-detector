"""
Generates a comprehensive, publication-grade academic PDF report
for the AI Metadata Detector project and Version Control Systems (VCS) viva.
Course Faculty Guide: Dr. Pooja Batra
Students: Satvik Sureka, Samarth Mahajan, Gourang Jawa, Vedansh Dhawana
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print 'Page X of Y'."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # We don't draw running header/footer on page 1 (cover)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        header_text = "AI Metadata Detector (AIMetaDetect) — Version Control Systems (VCS) Academic Report"
        mentor_text = "Guide: Dr. Pooja Batra"
        self.drawString(54, letter[1] - 34, header_text)
        self.drawRightString(letter[0] - 54, letter[1] - 34, mentor_text)

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 38, letter[0] - 54, letter[1] - 38)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {total_pages}"
        team_str = "Team: Satvik Sureka (2581276) | Samarth Mahajan (2581419) | Gourang Jawa (2581080) | Vedansh Dhawana (2581314)"
        self.drawString(54, 32, team_str)
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.line(54, 42, letter[0] - 54, 42)

        self.restoreState()


def build_pdf(output_filename="AI_Metadata_Detector_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom Palettes
    PRIMARY = colors.HexColor("#0F172A")    # Deep Navy
    SECONDARY = colors.HexColor("#0284C7")  # Tech Blue
    ACCENT_TEAL = colors.HexColor("#0D9488")# Teal
    ACCENT_WARN = colors.HexColor("#D97706")# Amber
    DARK_TEXT = colors.HexColor("#1E293B")  # Slate Dark
    LIGHT_BG = colors.HexColor("#F8FAFC")   # Crisp Background
    BORDER_CLR = colors.HexColor("#CBD5E1")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=SECONDARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=DARK_TEXT,
        spaceAfter=4.5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    qa_q_style = ParagraphStyle(
        'QA_Q',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=13,
        textColor=colors.HexColor("#0369A1"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    qa_a_style = ParagraphStyle(
        'QA_A',
        parent=body_style,
        fontName='Helvetica',
        fontSize=8.6,
        leading=11.8,
        textColor=DARK_TEXT,
        spaceAfter=4.5
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, ACADEMIC METADATA & DOCUMENT ROADMAP
    # =========================================================================
    story.append(Paragraph("AI METADATA DETECTOR (AIMetaDetect)", title_style))
    story.append(Paragraph(
        "Digital Media Forensics & AI Provenance Auditing Framework<br/>"
        "<b>Comprehensive Project Report & Version Control Systems (VCS) Viva Handbook</b>",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=8))

    # Academic Metadata Block (Table)
    meta_table_data = [
        [
            Paragraph("<b>Subject / Course:</b>", body_style),
            Paragraph("Version Control Systems (VCS) Lab (B.Tech CSE - 2nd Year)", body_style),
            Paragraph("<b>Faculty Guide:</b>", body_style),
            Paragraph("<b>Dr. Pooja Batra</b>", ParagraphStyle('Pb', parent=body_style, fontName='Helvetica-Bold', textColor=SECONDARY))
        ],
        [
            Paragraph("<b>Student Team:</b>", body_style),
            Paragraph("1. Satvik Sureka (<b>2581276</b>) — Team Lead & Engine<br/>"
                      "2. Samarth Mahajan (<b>2581419</b>) — Document Forensics<br/>"
                      "3. Gourang Jawa (<b>2581080</b>) — Audio Forensics & Tests<br/>"
                      "4. Vedansh Dhawana (<b>2581314</b>) — GUI / CLI & Docs", body_style),
            Paragraph("<b>Technology Stack:</b>", body_style),
            Paragraph("Python 3.11, Git / GitHub CLI, Pillow, PyPDF, ReportLab, Rich, Tkinter", body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[1.3*inch, 2.6*inch, 1.3*inch, 1.8*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Executive Summary Callout
    summary_box_data = [[
        Paragraph(
            "<b>Executive Purpose & Student Viva Preparation Guide:</b><br/>"
            "This report is tailored for the 4 student contributors (Satvik, Samarth, Gourang, Vedansh) to master every facet "
            "of this project before presenting to <b>Dr. Pooja Batra</b>. It covers two foundational areas: "
            "<b>(1) The AI Metadata Detector</b> (inspecting PNG chunks, EXIF, XMP, C2PA, PDFs, and Audio tags to recover ground-truth prompts), "
            "and <b>(2) Version Control Systems (VCS)</b> (explaining the underlying mechanics of Git, its object store, "
            "staging area index, feature branch isolation, merges, and remote tracking). "
            "Section 5 contains 15 curated viva questions and answers to prepare the team for teacher questioning.",
            callout_style
        )
    ]]
    summary_box = Table(summary_box_data, colWidths=[7.0*inch])
    summary_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E0F2FE")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#38BDF8")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_box)
    story.append(Spacer(1, 8))

    # Document Table of Contents / Roadmap Table
    roadmap_data = [
        [Paragraph("<b>Report Section</b>", body_bold), Paragraph("<b>Key Topics & Concepts Covered</b>", body_bold), Paragraph("<b>Primary Relevance</b>", body_bold)],
        [
            Paragraph("<b>Section 1</b>", body_style),
            Paragraph("What is the AI Metadata Detector? GenAI provenance, PNG chunks, EXIF, XMP, C2PA, PDF & Audio signatures.", body_style),
            Paragraph("Technical Architecture", body_style)
        ],
        [
            Paragraph("<b>Section 2</b>", body_style),
            Paragraph("Codebase Architecture: models.py, image/document/audio detectors, engine.py, CLI, GUI, and unit tests.", body_style),
            Paragraph("Implementation Walkthrough", body_style)
        ],
        [
            Paragraph("<b>Section 3</b>", body_style),
            Paragraph("Mathematical Confidence Scoring Model: Probabilistic union formula vs arithmetic averaging.", body_style),
            Paragraph("Forensic Algorithm", body_style)
        ],
        [
            Paragraph("<b>Section 4</b>", body_style),
            Paragraph("Master Guide to Version Control Systems (VCS): Git Three Trees, Object Database (Blobs/Trees/Commits), Step-by-Step CLI Command Reference.", body_style),
            Paragraph("VCS Curriculum Core", body_style)
        ],
        [
            Paragraph("<b>Section 5</b>", body_style),
            Paragraph("Teacher Q&A Handbook: 15 Anticipated Viva Questions & Comprehensive Model Answers for Dr. Pooja Batra.", body_style),
            Paragraph("Viva / Exam Prep", body_style)
        ],
        [
            Paragraph("<b>Section 6 & 7</b>", body_style),
            Paragraph("Individual Team Member Responsibilities & Speaking Notes (Satvik, Samarth, Gourang, Vedansh), and Acknowledgments.", body_style),
            Paragraph("Presentation Allocation", body_style)
        ]
    ]
    roadmap_table = Table(roadmap_data, colWidths=[1.1*inch, 4.4*inch, 1.5*inch])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(roadmap_table)

    # =========================================================================
    # PAGE 2: SECTION 1 - AI METADATA FORENSICS & SIGNATURES
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("1. Technical Deep-Dive: What is the AI Metadata Detector?", h1_style))
    story.append(Paragraph(
        "Modern Generative Artificial Intelligence (GenAI) models synthesize photorealistic imagery, persuasive academic text, "
        "and studio-quality music. However, distinguishing synthetic media from authentic human creations has become a critical "
        "challenge for digital forensics, misinformation defense, and academic integrity. While deep learning pixel classifiers "
        "often behave as computationally expensive, brittle black boxes, <b>metadata forensic analysis</b> inspects ground-truth "
        "artifacts deterministically in milliseconds.",
        body_style
    ))
    story.append(Paragraph(
        "Almost all major generative AI frameworks automatically inject diagnostic metadata chunks, generation prompts, "
        "or cryptographic provenance manifests into generated media during file creation. <b>AIMetaDetect</b> parses these raw "
        "binary headers directly on the local machine without requiring cloud API tokens or GPU acceleration.",
        body_style
    ))

    # Supported Signatures Table
    sig_table_data = [
        [Paragraph("<b>Target AI Framework</b>", body_bold), Paragraph("<b>Metadata Location & Forensic Signatures</b>", body_bold), Paragraph("<b>Forensic Value Recovered</b>", body_bold)],
        [
            Paragraph("<b>Stable Diffusion</b><br/>(A1111 / WebUI / Forge)", body_style),
            Paragraph("Embedded PNG text chunks (<code>tEXt</code> / <code>iTXt</code>) under key <code>parameters</code>.", body_style),
            Paragraph("Full positive prompt, negative prompt, seed, sampler (Euler, DPM++), CFG scale, steps, model hash.", body_style)
        ],
        [
            Paragraph("<b>ComfyUI</b>", body_style),
            Paragraph("PNG chunks named <code>prompt</code> and <code>workflow</code> storing JSON node graphs.", body_style),
            Paragraph("Complete node graph (KSampler, CLIPTextEncode), model checkpoint name (.safetensors).", body_style)
        ],
        [
            Paragraph("<b>Adobe Firefly & Photoshop GenAI</b>", body_style),
            Paragraph("Raw binary XMP packet containing IPTC DigitalSourceType: <code>trainedAlgorithmicMedia</code>.", body_style),
            Paragraph("Definitive proof of generative synthetic creation under global IPTC photo journalism standards.", body_style)
        ],
        [
            Paragraph("<b>DALL-E 3 & Midjourney</b>", body_style),
            Paragraph("EXIF <code>UserComment</code>, <code>Software</code> tags, and C2PA Content Credentials manifests.", body_style),
            Paragraph("Cryptographic provenance attestations and model identifier tags.", body_style)
        ],
        [
            Paragraph("<b>ChatGPT / Claude / LLM PDFs</b>", body_style),
            Paragraph("PDF Document Info dictionary (<code>Producer</code>, <code>Author</code>) and conversational watermarks.", body_style),
            Paragraph("Producer strings ('ChatGPT', 'OpenAI') and boilerplate phrases ('As an AI language model...').", body_style)
        ],
        [
            Paragraph("<b>Suno & Udio AI Music</b>", body_style),
            Paragraph("ID3v2 text frames and RIFF metadata chunks.", body_style),
            Paragraph("Model encoder versions (e.g. 'Suno v3.5 AI') embedded in MP3 headers.", body_style)
        ]
    ]
    sig_table = Table(sig_table_data, colWidths=[1.8*inch, 2.7*inch, 2.5*inch])
    sig_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. System Architecture & Codebase Walkthrough", h1_style))
    story.append(Paragraph(
        "The project is structured according to modular software engineering principles. Below is a breakdown of all source files:",
        body_style
    ))

    code_modules = [
        ("aimeta/models.py", "Defines the core data structures using Python dataclasses (DetectionResult, MetadataIndicator) and the Verdict enum (AI_GENERATED, LIKELY_AI, SUSPICIOUS, NATURAL_OR_STRIPPED). Decouples data representation from analysis logic."),
        ("aimeta/image_detector.py", "Parses raster images using PIL.Image.info dictionary for PNG chunks, img.getexif() for EXIF tags, and scans the raw binary buffer (first 5MB) using regular expressions to intercept XMP packets and C2PA manifests that standard image libraries overlook."),
        ("aimeta/document_detector.py", "Inspects PDFs using pypdf.PdfReader. Reads the /Producer, /Author, and /Subject dictionary fields, and extracts page text to detect characteristic LLM conversational boilerplate ('As an AI language model', 'Certainly! Here is...')."),
        ("aimeta/audio_detector.py", "Reads binary ID3v1/ID3v2 tags and RIFF metadata headers for generative audio encoder strings from Suno, Udio, ElevenLabs, and OpenAI Whisper."),
        ("aimeta/engine.py", "Acts as the central Factory / Facade pattern. Inspects file extensions and automatically routes target files to the appropriate detector. Provides both scan_file() and scan_directory() batch APIs."),
        ("aimeta/cli.py", "Interactive command-line interface implemented with the Python 'rich' library. Displays styled panels, color-coded verdict badges, metadata tables, and exports batch findings to structured JSON reports."),
        ("gui.py", "Desktop GUI built using standard Python Tkinter. Features file browsing, real-time scanning, verdict cards, and a Treeview table for interactive viva demonstrations."),
        ("sample_generator.py", "Generates authentic synthetic test files (Stable Diffusion PNG with parameter chunk, ComfyUI workflow JSON, Adobe Firefly XMP, natural Canon 5D DSLR photo) for immediate offline verification."),
        ("tests/test_detector.py", "Automated unit test suite utilizing Python's built-in unittest framework. Verifies that all 6 test cases pass with 100% accuracy in 0.036 seconds.")
    ]

    for filename, desc in code_modules:
        p_mod = Paragraph(f"• <b><code>{filename}</code></b>: {desc}", body_style)
        story.append(p_mod)

    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Mathematical Confidence Scoring Model", h1_style))
    story.append(Paragraph(
        "Rather than computing an arbitrary arithmetic mean, AIMetaDetect implements a <b>probabilistic union formula</b> "
        "across all discovered forensic indicators. If multiple independent indicators are identified (e.g., a Stable Diffusion "
        "parameter chunk with weight 0.98 and a keyword signature match with weight 0.92), the combined AI confidence score is calculated as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Confidence = (1 - &prod;<sub>i</sub> (1 - w<sub>i</sub> &times; 0.95)) &times; 100%</b><br/>"
        "This ensures that a single definitive signature immediately yields &gt;95% confidence, while corroborating evidence "
        "pushes certainty toward 99.9%. When only authentic camera hardware tags (Make/Model) are discovered, the score drops to 5.0%, "
        "triggering the <b>NATURAL_OR_STRIPPED</b> verdict.",
        body_style
    ))

    # =========================================================================
    # PAGE 3: SECTION 4 - VERSION CONTROL SYSTEMS & GIT INTERNALS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Master Guide: Version Control Systems (VCS) & Git Internals", h1_style))
    story.append(Paragraph(
        "Because this project is specifically evaluated for the <b>Version Control Systems (VCS)</b> subject, Dr. Pooja Batra "
        "will test your understanding of <b>how Git works under the hood</b>. This section covers Git's core architecture, "
        "its object database, and the exact step-by-step CLI commands executed during our development lifecycle.",
        body_style
    ))

    story.append(Paragraph("Git's Core Architecture: The Three Conceptual Trees", h2_style))
    story.append(Paragraph(
        "Unlike older Centralized VCS (such as SVN or CVS), Git is a <b>Distributed Version Control System (DVCS)</b>. "
        "Every developer maintains an entire cloned repository locally, complete with history and branches. "
        "Git manages file states across three primary conceptual zones:",
        body_style
    ))

    trees_data = [
        [Paragraph("<b>Git Conceptual Area</b>", body_bold), Paragraph("<b>Physical Location</b>", body_bold), Paragraph("<b>Function & Underlying Mechanism</b>", body_bold)],
        [
            Paragraph("<b>1. Working Directory</b>", body_style),
            Paragraph("Local OS File System (e.g. <code>c:\\Users\\...\\VCS presentation group</code>)", body_style),
            Paragraph("The actual sandbox folder where you write code, add images, and modify scripts. Contains uncommitted changes.", body_style)
        ],
        [
            Paragraph("<b>2. Staging Area (Index)</b>", body_style),
            Paragraph("Binary index file inside <code>.git/index</code>", body_style),
            Paragraph("The transit area. Prepares a snapshot of tracked changes before they are committed. Populated via <code>git add</code>.", body_style)
        ],
        [
            Paragraph("<b>3. Git Repository (HEAD)</b>", body_style),
            Paragraph("Object store in <code>.git/objects/</code>", body_style),
            Paragraph("The permanent Directed Acyclic Graph (DAG) of commit objects, tree objects, and blob objects. Updated via <code>git commit</code>.", body_style)
        ]
    ]
    trees_table = Table(trees_data, colWidths=[1.8*inch, 2.2*inch, 3.0*inch])
    trees_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(trees_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Git's Object Database: Blobs, Trees, and Commits", h2_style))
    story.append(Paragraph(
        "Inside the <code>.git/objects/</code> directory, Git stores content addressed by its SHA-1 hash (40 hexadecimal characters). "
        "There are 3 fundamental object types in Git that students must understand:<br/>"
        "• <b>Blob (Binary Large Object):</b> Stores pure raw file content (data only, no file name or permissions).<br/>"
        "• <b>Tree Object:</b> Represents a directory. It lists filenames, file permissions (e.g. 100644), and links each filename to its corresponding Blob SHA-1 hash.<br/>"
        "• <b>Commit Object:</b> Points to a root Tree object, contains author/committer names and timestamps, a commit log message, and the SHA-1 hash of the parent commit (forming a Directed Acyclic Graph).",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Complete Step-by-Step Breakdown of All Git Commands Used:", h2_style))

    git_cmds = [
        ("1. git init",
         "Initializes a new Git repository in the project folder.",
         "Creates the hidden '.git' directory containing subfolders: /objects (stores blobs/trees), /refs (branch pointers), /hooks, and HEAD. Converts a regular directory into a version-controlled repository."),

        ("2. git status",
         "Inspects the state of the Working Directory and Staging Area.",
         "Compares SHA-1 hashes of files on disk with the index file and HEAD commit. Highlights untracked files in red and staged files in green. Running git status frequently prevents committing unwanted files."),

        ("3. git add .  (or git add <file>)",
         "Stages changes from the Working Directory into the Staging Area.",
         "Behind the scenes, Git compresses each staged file using zlib, computes its SHA-1 hash, writes a 'blob' object into '.git/objects/', and updates '.git/index'. Prepares an atomic snapshot."),

        ("4. git commit -m \"message\"",
         "Permanently records staged snapshots into the repository history.",
         "Git creates a 'tree' object referencing the blobs, builds a 'commit' object with metadata (author, timestamp, parent commit), and moves the active branch pointer forward."),

        ("5. git branch -M main",
         "Renames the default branch pointer to 'main'.",
         "Conforms to modern GitHub standards where 'main' is used as the primary production branch instead of the legacy 'master' name."),

        ("6. git checkout -b feature/<name>",
         "Creates a new feature branch and immediately switches HEAD to it.",
         "Essential for multi-developer collaboration (Satvik, Samarth, Gourang, Vedansh). Keeps unfinished experimental code isolated away from the production branch ('main')."),

        ("7. git branch",
         "Lists all local branches in the repository.",
         "Reads reference files inside '.git/refs/heads/'. The active branch is denoted with an asterisk (*) and highlighted in green."),

        ("8. git merge <branch-name>",
         "Integrates commits from a specified branch into the active branch.",
         "If no divergent commits exist on main, Git performs a fast-forward merge (simply sliding the main pointer forward). If divergence exists, Git creates a 3-way merge commit resolving differences."),

        ("9. git remote add origin <url>",
         "Registers a remote repository URL under the short alias 'origin'.",
         "Edits '.git/config' by adding a [remote \"origin\"] section with the fetch and push URLs pointing to GitHub."),

        ("10. git push -u origin main",
         "Uploads local commits to the remote GitHub repository.",
         "Pushes objects over HTTPS/SSH. The '-u' (upstream) flag links the local 'main' branch to 'origin/main', allowing future operations to simply use 'git push' or 'git pull'."),

        ("11. git log --oneline --graph --all",
         "Visualizes the Directed Acyclic Graph (DAG) of all commits and branches.",
         "Renders an ASCII text graph showing branch divergence, merges, and atomic commit history in a concise single-line format.")
    ]

    for title, short_desc, internal_desc in git_cmds:
        cmd_p = Paragraph(f"<b>{title}</b> — <i>{short_desc}</i>", body_bold)
        desc_p = Paragraph(f"<b>Under the Hood:</b> {internal_desc}", body_style)
        story.append(KeepTogether([cmd_p, desc_p, Spacer(1, 2.5)]))

    # Commit History Table of our Project
    story.append(Spacer(1, 4))
    story.append(Paragraph("Actual Commit History of our Repository (from 'git log --oneline'):", h2_style))
    history_data = [
        [Paragraph("<b>Commit SHA</b>", body_bold), Paragraph("<b>Branch / Merge</b>", body_bold), Paragraph("<b>Commit Message & Scope</b>", body_bold)],
        [Paragraph("<code>08b7c96</code>", body_style), Paragraph("main (root)", body_style), Paragraph("<code>chore: initial project structure and data models</code>", body_style)],
        [Paragraph("<code>7b1695e</code>", body_style), Paragraph("feature/metadata-detectors", body_style), Paragraph("<code>feat(detectors): implement image, document, audio parsers and scoring engine</code>", body_style)],
        [Paragraph("<code>d65414f</code>", body_style), Paragraph("feature/ui-and-samples", body_style), Paragraph("<code>feat(ui): add Rich CLI, desktop GUI, sample generator, and unit test suite</code>", body_style)],
        [Paragraph("<code>f860f7e</code>", body_style), Paragraph("main (HEAD)", body_style), Paragraph("<code>docs(presentation): add VCS presentation deck and slide builder script</code>", body_style)]
    ]
    hist_table = Table(history_data, colWidths=[1.1*inch, 2.1*inch, 3.8*inch])
    hist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#334155")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(hist_table)

    # =========================================================================
    # PAGE 4 & 5: SECTION 5 - TEACHER VIVA Q&A HANDBOOK (DR. POOJA BATRA)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Teacher Q&A Handbook: Anticipated Viva Questions & Model Answers", h1_style))
    story.append(Paragraph(
        "During laboratory evaluation, <b>Dr. Pooja Batra</b> is likely to interrogate both your mastery of Git version control "
        "and your technical implementation of the AI Metadata Detector. Below are 15 carefully curated questions with "
        "accurate, impressive model answers.",
        body_style
    ))

    story.append(Paragraph("Part A: Version Control Systems & Git Questions", h2_style))

    vcs_qa = [
        ("Q1: What is the fundamental difference between Git and Centralized VCS like SVN?",
         "In Centralized VCS (SVN), there is a single central server holding the repository history. If the server goes down, developers cannot commit, branch, or view history. In Git (Distributed VCS), every developer's local machine contains a complete clone of the entire repository history. Developers can commit, branch, inspect logs, and merge completely offline. The central server (GitHub) is merely a synchronization hub."),

        ("Q2: What is the Staging Area (Index) in Git, and why doesn't Git just commit directly from the working folder?",
         "The Staging Area acts as a preparatory checkpoint between the working directory and the permanent commit history. It allows developers to craft atomic, logical commits. For example, if a developer edits 5 files but only 2 relate to a bug fix, they can stage (git add) only those 2 files, commit them with an accurate message, and stage the rest later. Direct committing would force all dirty working changes into history together."),

        ("Q3: What actually happens inside the '.git' folder when you run 'git commit'?",
         "Git creates a permanent snapshot consisting of three object types: (1) 'Blob' objects storing file content, (2) 'Tree' objects representing directory hierarchies and file names pointing to blobs, and (3) A 'Commit' object containing author info, committer info, timestamp, commit message, root tree SHA-1 hash, and the parent commit hash. Finally, Git updates the branch ref pointer in .git/refs/heads/ to point to this new commit hash."),

        ("Q4: What is a 'Fast-Forward' merge versus a '3-Way Merge'?",
         "A Fast-Forward merge occurs when the target branch (e.g. main) has had no new commits since the feature branch was branched off. Git simply moves the 'main' branch pointer forward to point to the latest commit of the feature branch without creating a new commit. A 3-Way merge occurs when both branches have diverged (both have new commits). Git compares the two tip commits with their common ancestor and creates a new 'merge commit' with two parent pointers."),

        ("Q5: What is the purpose of the '.gitignore' file in our project?",
         "The .gitignore file specifies intentionally untracked patterns that Git should ignore. In our Python project, we ignored __pycache__/, *.pyc, virtual environment folders (.venv/), and IDE folders (.vscode/, .idea/). If committed, compiled bytecode and IDE settings create unnecessary repository bloat, merge conflicts across different operating systems, and security risks if secrets are cached."),

        ("Q6: What is the difference between 'git pull' and 'git fetch'?",
         "'git fetch' downloads new commits, files, and refs from the remote repository (GitHub) into your local repository without modifying your working files. 'git pull' is a combination of two operations: it runs 'git fetch' followed immediately by 'git merge' to integrate the remote changes into your active local branch."),

        ("Q7: What is the HEAD pointer in Git?",
         "HEAD is a symbolic reference pointer stored in '.git/HEAD' that points to the currently checked-out branch or commit. Usually, it points to a branch reference (e.g. 'ref: refs/heads/main'). If you check out a specific historical commit directly instead of a branch, Git enters a 'detached HEAD' state where new commits are not attached to any named branch."),

        ("Q8: Why did our team use feature branches (e.g., feature/metadata-detectors) instead of committing directly to main?",
         "Using feature branches adheres to professional industry git workflows (such as GitHub Flow). It prevents broken, untested code from polluting the production-ready 'main' branch, enables concurrent development among team members without file conflicts, and allows peer reviews before code is merged.")
    ]

    for q, a in vcs_qa:
        story.append(Paragraph(q, qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Part B: AI Metadata Detector & Technical Questions", h2_style))

    ai_qa = [
        ("Q9: What is the difference between EXIF, XMP, and PNG text chunks?",
         "EXIF (Exchangeable Image File Format) is an older standard primarily used in JPEGs for camera hardware settings (ISO, Shutter, Lens, Make/Model). PNG text chunks (tEXt, iTXt, zTXt) are native key-value metadata blocks defined in the PNG specification, heavily utilized by Stable Diffusion and ComfyUI for generation parameters. XMP (Extensible Metadata Platform) is an XML-based metadata standard developed by Adobe that supports advanced namespaces, including IPTC digital source types and C2PA Content Credentials."),

        ("Q10: What happens if an image is posted to WhatsApp, Instagram, or Twitter? Can our tool still detect it?",
         "Social media platforms automatically recompress images and strip all EXIF, PNG chunks, and XMP metadata to save bandwidth and protect user privacy. In that scenario, AIMetaDetect will correctly return 'NATURAL_OR_STRIPPED' (confidence ~10%) because the metadata has been scrubbed. Our tool explains this transparently in the scan notes rather than guessing. Detecting stripped images requires latent pixel watermarking (like SynthID) or deep neural networks, which is outside the scope of metadata forensics."),

        ("Q11: How does your tool extract the exact generation prompt from Stable Diffusion images?",
         "When Stable Diffusion (via Automatic1111 or WebUI) saves an image, it writes an uncompressed PNG text chunk with the key 'parameters'. Inside this chunk is a plaintext string: the first line is the positive prompt, followed by 'Negative prompt: ...', followed by generation hyperparameters ('Steps: 28, Sampler: DPM++ 2M, Seed: ...'). AIMetaDetect uses regex patterns to extract and isolate the exact prompt string."),

        ("Q12: How does the tool inspect PDFs for ChatGPT or LLM generation?",
         "AIMetaDetect uses 'pypdf' to inspect the PDF trailer dictionary and document metadata block. Many AI PDF converters explicitly record 'ChatGPT' or 'OpenAI' in the /Producer or /Author tags. Additionally, the tool scans the first 5 pages of extracted text for recurring conversational AI tropes ('As an AI language model', 'Certainly! Here is an essay...')."),

        ("Q13: What is C2PA (Content Credentials) and why is it important?",
         "C2PA (Coalition for Content Provenance and Authenticity) is an open industry standard supported by Adobe, Microsoft, OpenAI (DALL-E 3), and Google. Instead of simple editable metadata tags, C2PA embeds cryptographically signed provenance manifests (JUMBF boxes) into media files, attesting to the tool used, author, and whether AI synthesis was involved."),

        ("Q14: Why did we build both a CLI and a Tkinter GUI?",
         "The CLI (built with Python 'rich') is designed for high-throughput batch operations, forensic automation, and headless server environments. The Tkinter desktop GUI was developed for interactive presentations and non-technical evaluators, enabling drag-and-drop file inspection with real-time visual verdict badges and prompt display."),

        ("Q15: How were the sample test files generated in the 'samples/' directory?",
         "We created 'sample_generator.py', which programmatically synthesizes authentic test media: a PNG image with Stable Diffusion parameter chunks, a ComfyUI workflow JSON chunk, a JPEG injected with Adobe Firefly XMP packets, an authentic Canon DSLR camera JPEG with EXIF tags, an AI-authored PDF via ReportLab, and an MP3 with Suno ID3 tags.")
    ]

    for q, a in ai_qa:
        story.append(Paragraph(q, qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    # =========================================================================
    # PAGE 6: SECTION 6 - TEAM ROLES, PRESENTATION ALLOCATION & CONCLUSION
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Team Responsibilities & Presentation Speaking Allocation", h1_style))
    story.append(Paragraph(
        "To ensure all four students perform cohesively and impress <b>Dr. Pooja Batra</b> during the project viva, "
        "divide your speaking responsibilities as follows:",
        body_style
    ))

    team_roles = [
        ("Satvik Sureka (Roll: 2581276) — Team Lead & Engine Architect",
         "Presentation Speaking Points:",
         "• Introduce the project title, problem statement, and motivation for local metadata forensics over black-box cloud AI.\n"
         "• Explain Git repository setup: git init, git config, and the importance of .gitignore in preventing repo bloat.\n"
         "• Explain 'aimeta/image_detector.py': how PNG chunks (tEXt) store Stable Diffusion parameters and prompt extraction regex.\n"
         "• Explain Git commit mechanics: how Git constructs Blob, Tree, and Commit objects."),

        ("Samarth Mahajan (Roll: 2581419) — Document Forensics Engineer",
         "Presentation Speaking Points:",
         "• Explain 'aimeta/document_detector.py': how PDFs store /Producer, /Author, and /Subject dictionary metadata.\n"
         "• Explain linguistic watermark analysis: scanning text bodies for ChatGPT conversational disclaimers.\n"
         "• Explain Git branching strategies: git checkout -b feature/metadata-detectors, branch pointers, and HEAD.\n"
         "• Explain Git merge mechanics: fast-forward merge vs 3-way merge commits when integrating features."),

        ("Gourang Jawa (Roll: 2581080) — Audio Forensics & Scoring Lead",
         "Presentation Speaking Points:",
         "• Explain 'aimeta/audio_detector.py': scanning ID3v1/ID3v2 tags and RIFF metadata headers for Suno/Udio generative music.\n"
         "• Explain the mathematical confidence scoring formula: probabilistic union of independent indicator weights.\n"
         "• Walk through the automated unit test suite in 'tests/test_detector.py' (6 test cases passing in 0.036 seconds).\n"
         "• Explain 'git status' and how Git detects modified vs untracked files by comparing SHA-1 hashes."),

        ("Vedansh Dhawana (Roll: 2581314) — UI/UX & Documentation Specialist",
         "Presentation Speaking Points:",
         "• Demonstrate the interactive CLI interface ('python main.py scan' and 'python main.py batch').\n"
         "• Launch and demonstrate the desktop GUI ('python gui.py') with live file browsing and badge updates.\n"
         "• Walk Dr. Pooja Batra through the 13-slide PowerPoint presentation ('AI_Metadata_Detector_Presentation.pptx').\n"
         "• Explain 'git push -u origin main' and how the local repository synchronizes with the GitHub remote origin.")
    ]

    for name_role, header, bullets in team_roles:
        card_data = [[
            Paragraph(f"<b>{name_role}</b>", body_bold),
        ], [
            Paragraph(f"<b>{header}</b><br/>" + bullets.replace("\n", "<br/>"), body_style)
        ]]
        card_tbl = Table(card_data, colWidths=[7.0*inch])
        card_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 1, BORDER_CLR),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ]))
        story.append(card_tbl)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 6))

    # Formal Conclusion & Acknowledgment
    story.append(Paragraph("7. Conclusion & Formal Acknowledgments", h1_style))
    story.append(Paragraph(
        "Through this project, our team achieved two major milestones: (1) we constructed a robust, modular, "
        "and explainable digital forensics tool capable of exposing hidden generative AI markers across images, "
        "documents, and audio; and (2) we developed hands-on mastery over the complete Version Control System lifecycle, "
        "maintaining atomic commits, clean branching structures, and GitHub remote workflows.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Special Acknowledgment:</b><br/>"
        "We express our heartfelt gratitude to our esteemed faculty mentor, <b>Dr. Pooja Batra</b>, for her inspiring guidance, "
        "valuable academic critique, and high standards throughout the Version Control Systems laboratory course. "
        "Her mentorship has deeply shaped our understanding of software engineering and collaborative software development.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated comprehensive report: {output_filename}")


if __name__ == "__main__":
    build_pdf()
