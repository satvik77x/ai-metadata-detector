"""
Script to generate a professional 16:9 widescreen PowerPoint presentation
for the AI Metadata Detector VCS Academic Project.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(filename="AI_Metadata_Detector_Presentation.pptx"):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank slide

    # Color Palette: Modern Navy / Tech Blue / Slate
    BG_DARK = RGBColor(15, 23, 42)        # Deep Slate Blue (#0F172A)
    CARD_BG = RGBColor(30, 41, 59)        # Card Navy (#1E293B)
    CARD_BORDER = RGBColor(51, 65, 85)    # Slate Border (#334155)
    PRIMARY_CYAN = RGBColor(56, 189, 248) # Cyan Accent (#38BDF8)
    ACCENT_BLUE = RGBColor(96, 165, 250)  # Light Blue (#60A5FA)
    TEXT_WHITE = RGBColor(248, 250, 252)  # Crisp White (#F8FAFC)
    TEXT_MUTED = RGBColor(148, 163, 184)  # Muted Gray (#94A3B8)
    ACCENT_GREEN = RGBColor(52, 211, 153) # Mint Green (#34D399)
    ACCENT_YELLOW = RGBColor(250, 204, 21)# Amber Yellow (#FACC15)
    ACCENT_RED = RGBColor(248, 113, 113)  # Soft Red (#F87171)

    def set_slide_background(slide, color=BG_DARK):
        background = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        background.fill.solid()
        background.fill.fore_color.rgb = color
        background.line.color.rgb = color
        return background

    def add_header(slide, title_text, category="VERSION CONTROL SYSTEMS PROJECT"):
        # Category Tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = PRIMARY_CYAN
        p_c.font.name = "Segoe UI"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE
        p_t.font.name = "Segoe UI"

        # Subtle Accent line under header
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.color.rgb = CARD_BORDER

    def add_card(slide, left, top, width, height, title="", title_color=PRIMARY_CYAN):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.font.name = "Segoe UI"

        # Content text box
        content_box = slide.shapes.add_textbox(
            left + Inches(0.2), 
            top + (Inches(0.6) if title else Inches(0.15)), 
            width - Inches(0.4), 
            height - (Inches(0.75) if title else Inches(0.3))
        )
        tf_c = content_box.text_frame
        tf_c.word_wrap = True
        return tf_c

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent Top Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(4.5), Inches(0.4))
    badge.fill.solid()
    badge.fill.fore_color.rgb = CARD_BG
    badge.line.color.rgb = PRIMARY_CYAN
    tf_badge = badge.text_frame
    p_b = tf_badge.paragraphs[0]
    p_b.text = "🛡️ B.Tech CSE (2nd Year) Laboratory Project"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = PRIMARY_CYAN
    p_b.font.name = "Segoe UI"
    p_b.alignment = PP_ALIGN.CENTER

    # Main Project Title
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.5), Inches(1.6))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "AI METADATA DETECTOR"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.font.name = "Segoe UI"

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Digital Media Provenance & Generative AI Forensic Auditing Tool"
    p1_sub.font.size = Pt(18)
    p1_sub.font.color.rgb = ACCENT_BLUE
    p1_sub.font.name = "Segoe UI"
    p1_sub.space_before = Pt(8)

    # Course / Subject Tag
    subj_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(11.5), Inches(0.6))
    tf_subj = subj_box.text_frame
    p_s = tf_subj.paragraphs[0]
    p_s.text = "Subject: Version Control Systems (VCS) | GitHub CLI Implementation"
    p_s.font.size = Pt(14)
    p_s.font.bold = True
    p_s.font.color.rgb = ACCENT_YELLOW
    p_s.font.name = "Segoe UI"

    # Guide Card (Left Bottom)
    tf_guide = add_card(s1, Inches(0.8), Inches(4.0), Inches(4.5), Inches(2.7), "FACULTY MENTOR", PRIMARY_CYAN)
    p_g1 = tf_guide.paragraphs[0]
    p_g1.text = "Dr. Pooja Batra"
    p_g1.font.size = Pt(20)
    p_g1.font.bold = True
    p_g1.font.color.rgb = TEXT_WHITE
    p_g1.font.name = "Segoe UI"

    p_g2 = tf_guide.add_paragraph()
    p_g2.text = "Department of Computer Science & Engineering"
    p_g2.font.size = Pt(12)
    p_g2.font.color.rgb = TEXT_MUTED
    p_g2.font.name = "Segoe UI"
    p_g2.space_before = Pt(6)

    p_g3 = tf_guide.add_paragraph()
    p_g3.text = "Evaluator & Subject Expert - Version Control Systems"
    p_g3.font.size = Pt(11)
    p_g3.font.italic = True
    p_g3.font.color.rgb = PRIMARY_CYAN
    p_g3.font.name = "Segoe UI"
    p_g3.space_before = Pt(4)

    # Student Team Card (Right Bottom)
    tf_team = add_card(s1, Inches(5.6), Inches(4.0), Inches(6.9), Inches(2.7), "STUDENT DEVELOPERS (TEAM MEMBERS)", ACCENT_GREEN)
    students = [
        ("Satvik Sureka", "2581276", "Team Lead & Core Engine"),
        ("Samarth Mahajan", "2581419", "Document / PDF Module"),
        ("Gourang Jawa", "2581080", "Audio Module & Unit Testing"),
        ("Vedansh Dhawana", "2581314", "CLI / GUI & VCS Documentation")
    ]
    for i, (name, roll, role) in enumerate(students):
        p_m = tf_team.paragraphs[0] if i == 0 else tf_team.add_paragraph()
        p_m.text = f"•  {name} "
        p_m.font.size = Pt(13)
        p_m.font.bold = True
        p_m.font.color.rgb = TEXT_WHITE
        p_m.font.name = "Segoe UI"
        if i > 0:
            p_m.space_before = Pt(4)

        # Append roll and role
        run_roll = p_m.add_run()
        run_roll.text = f"(Roll No: {roll}) "
        run_roll.font.size = Pt(12)
        run_roll.font.bold = True
        run_roll.font.color.rgb = PRIMARY_CYAN

        run_role = p_m.add_run()
        run_role.text = f"— {role}"
        run_role.font.size = Pt(11)
        run_role.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 2: Project Overview & Abstract
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Project Overview & Abstract", "EXECUTIVE SUMMARY")

    tf_c1 = add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "The GenAI Media Boom", PRIMARY_CYAN)
    points_c1 = [
        ("Rapid Growth of AI Generation:", " Millions of photorealistic images, academic documents, and audio tracks are synthesized daily by models like Stable Diffusion, Midjourney, DALL-E, and ChatGPT."),
        ("Provenance & Authenticity Crisis:", " Identifying synthetic content is vital for academic integrity, misinformation deterrence, copyright attribution, and digital forensics."),
        ("The 'Metadata' Opportunity:", " Most AI image and document generators automatically inject diagnostic metadata chunks (generation parameters, prompt tokens, software tags, and IPTC/C2PA manifests) during creation.")
    ]
    for i, (hd, body) in enumerate(points_c1):
        p = tf_c1.paragraphs[0] if i == 0 else tf_c1.add_paragraph()
        p.text = f"• {hd}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.font.name = "Segoe UI"
        if i > 0: p.space_before = Pt(12)
        run = p.add_run()
        run.text = body
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED

    tf_c2 = add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "Our Solution: AIMetaDetect", ACCENT_GREEN)
    points_c2 = [
        ("Modular Forensic Scanner:", " A lightweight, open-source Python tool capable of inspecting raster graphics (PNG, JPEG, WebP), documents (PDF, TXT), and audio (MP3, WAV)."),
        ("Prompt Recovery Engine:", " Extracts the original generation prompt, seed, sampler, CFG scale, and model checkpoint directly from file headers."),
        ("Probabilistic Verdict Engine:", " Aggregates multi-source forensic indicators into an explainable 0–100% confidence score with standardized verdicts."),
        ("Academic VCS Showcase:", " Designed specifically for the Version Control Systems curriculum to showcase disciplined Git branch workflows, atomic commits, and team collaboration.")
    ]
    for i, (hd, body) in enumerate(points_c2):
        p = tf_c2.paragraphs[0] if i == 0 else tf_c2.add_paragraph()
        p.text = f"• {hd}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.font.name = "Segoe UI"
        if i > 0: p.space_before = Pt(12)
        run = p.add_run()
        run.text = body
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 3: Problem Statement & Objectives
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Problem Statement & Project Objectives", "CORE MOTIVATION")

    col_w = Inches(3.7)
    gap = Inches(0.3)

    # Card 1: Problem
    tf_p1 = add_card(s3, Inches(0.8), Inches(1.8), col_w, Inches(5.0), "1. The Challenge", ACCENT_RED)
    p_text1 = [
        "Inability to visually distinguish AI images from real camera captures.",
        "Cloud-based AI detectors are often slow, costly, require subscriptions, and compromise privacy.",
        "Black-box neural network classifiers suffer from high false-positive rates on natural images."
    ]
    for i, txt in enumerate(p_text1):
        p = tf_p1.paragraphs[0] if i == 0 else tf_p1.add_paragraph()
        p.text = f"❌  {txt}"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"
        p.space_before = Pt(14)

    # Card 2: Objective
    tf_p2 = add_card(s3, Inches(0.8) + col_w + gap, Inches(1.8), col_w, Inches(5.0), "2. Technical Objectives", PRIMARY_CYAN)
    p_text2 = [
        "Build a local, zero-network metadata analyzer in Python.",
        "Parse PNG chunks (tEXt, iTXt), JPEG EXIF, XMP packets, and C2PA manifests.",
        "Provide both a high-throughput CLI tool and an interactive GUI for non-technical users."
    ]
    for i, txt in enumerate(p_text2):
        p = tf_p2.paragraphs[0] if i == 0 else tf_p2.add_paragraph()
        p.text = f"🎯  {txt}"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_WHITE
        p.font.name = "Segoe UI"
        p.space_before = Pt(14)

    # Card 3: VCS Objective
    tf_p3 = add_card(s3, Inches(0.8) + (col_w + gap) * 2, Inches(1.8), col_w, Inches(5.0), "3. VCS Curriculum Goals", ACCENT_YELLOW)
    p_text3 = [
        "Implement end-to-end Git lifecycle via basic CLI commands only.",
        "Demonstrate multi-developer feature branch isolation and merging.",
        "Maintain clean commit histories, atomic commit practices, and push to GitHub."
    ]
    for i, txt in enumerate(p_text3):
        p = tf_p3.paragraphs[0] if i == 0 else tf_p3.add_paragraph()
        p.text = f"🛠️  {txt}"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"
        p.space_before = Pt(14)

    # ==========================================
    # SLIDE 4: Supported AI Frameworks & Signatures
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Supported AI Apps & Signature Database", "TARGET ECOSYSTEM")

    apps = [
        ("Stable Diffusion / A1111", "PNG 'parameters' chunk storing text prompt, negative prompt, steps, seed, CFG scale, sampler, and model checkpoint hash.", PRIMARY_CYAN),
        ("ComfyUI Workflows", "Embedded JSON node graphs ('prompt', 'workflow') mapping KSampler parameters and CLIPTextEncode nodes.", ACCENT_BLUE),
        ("Adobe Firefly / GenAI", "XMP metadata packet containing IPTC DigitalSourceType: 'trainedAlgorithmicMedia' or 'compositeSynthetic'.", ACCENT_GREEN),
        ("DALL-E 3 & Midjourney", "EXIF UserComment tags and C2PA Content Credentials cryptographic manifest headers.", ACCENT_YELLOW),
        ("ChatGPT / LLM Documents", "PDF 'Producer' / 'Author' dictionary headers and linguistic boilerplate conversational markers.", ACCENT_RED),
        ("AI Audio (Suno, Udio)", "ID3v2 user-defined text frames, RIFF comment chunks, and encoder signatures.", PRIMARY_CYAN)
    ]

    for idx, (app_name, desc, clr) in enumerate(apps):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8) + col * Inches(6.0)
        y = Inches(1.8) + row * Inches(1.65)
        tf_app = add_card(s4, x, y, Inches(5.7), Inches(1.45), f"🤖  {app_name}", clr)
        p = tf_app.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 5: Technical Architecture
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "System Architecture & Processing Pipeline", "TECHNICAL DESIGN")

    stages = [
        ("1. Input File", "Accepts .png, .jpg, .pdf, .mp3 from CLI or GUI drag-and-drop.", CARD_BG, PRIMARY_CYAN),
        ("2. Format Dispatcher", "Routes file to dedicated detector: Image, Document, or Audio.", CARD_BG, ACCENT_BLUE),
        ("3. Metadata Extraction", "Parses raw PNG chunks, EXIF tags, XMP packets, and PDF dictionaries.", CARD_BG, ACCENT_GREEN),
        ("4. Pattern Engine", "Cross-references extracted tags against known AI model signatures.", CARD_BG, ACCENT_YELLOW),
        ("5. Scoring & Verdict", "Computes 0-100% confidence score and generates forensic report.", CARD_BG, ACCENT_RED)
    ]

    for idx, (stage_title, stage_desc, bg_clr, border_clr) in enumerate(stages):
        x = Inches(0.8) + idx * Inches(2.38)
        card_s = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(2.2), Inches(3.6))
        card_s.fill.solid()
        card_s.fill.fore_color.rgb = bg_clr
        card_s.line.color.rgb = border_clr
        card_s.line.width = Pt(2)

        tf = card_s.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = stage_title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = border_clr
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = stage_desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(14)

    # Bottom summary bar
    bottom_tf = add_card(s5, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.8))
    p_b = bottom_tf.paragraphs[0]
    p_b.text = "⚡ Key Principle: Fast, deterministic inspection directly from file binaries without requiring external GPU hardware or API keys."
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = PRIMARY_CYAN
    p_b.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 6: Key Features & Forensic Capabilities
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Core Forensic Capabilities & User Interfaces", "FEATURES")

    features = [
        ("High-Accuracy Prompt Extraction", "Recovers exact text prompts embedded during generation (e.g., Stable Diffusion positive & negative prompts), providing indisputable evidence of AI synthesis."),
        ("Probabilistic Confidence Scoring", "Combines independent indicator weights using formula: 1 - Π(1 - w_i), preventing single-point misclassifications while rewarding corroborating indicators."),
        ("Dual Interface: CLI & Desktop GUI", "Includes a rich terminal CLI with formatted tables, badges, and JSON export, alongside a user-friendly Tkinter desktop interface for live demonstrations."),
        ("Local & Privacy Preserving", "Operates entirely on the local machine with zero data transmission to external servers, protecting user documents and confidential media.")
    ]

    for idx, (title, desc) in enumerate(features):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8) + col * Inches(6.0)
        y = Inches(1.8) + row * Inches(2.4)
        tf_f = add_card(s6, x, y, Inches(5.7), Inches(2.1), f"⭐  {title}", PRIMARY_CYAN if idx % 2 == 0 else ACCENT_GREEN)
        p = tf_f.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 7: Version Control System (VCS) - Role
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Role of Version Control Systems (VCS) in the Project", "VCS CURRICULUM")

    tf_vcs1 = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Why VCS is Essential in Engineering", PRIMARY_CYAN)
    points_vcs1 = [
        ("Change Tracking & Auditability:", " Every line of code, bug fix, and feature addition is recorded with author identity and timestamp."),
        ("Multi-Developer Collaboration:", " Enables 4 student team members to develop image, audio, document, and GUI modules concurrently without overwriting code."),
        ("Atomic Rollback & Safety:", " If an experimental parser introduces regressions, git allows reverting immediately to a verified stable snapshot."),
        ("Industry-Standard Practice:", " Direct alignment with CSE industry software engineering methodologies.")
    ]
    for i, (hd, body) in enumerate(points_vcs1):
        p = tf_vcs1.paragraphs[0] if i == 0 else tf_vcs1.add_paragraph()
        p.text = f"• {hd}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.font.name = "Segoe UI"
        if i > 0: p.space_before = Pt(12)
        run = p.add_run()
        run.text = body
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED

    tf_vcs2 = add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "Our Git Collaboration Architecture", ACCENT_YELLOW)
    points_vcs2 = [
        ("Repository Initialization:", " Created local repository and structured modular directory layout (.gitignore, aimeta/, tests/)."),
        ("Branching Strategy:", " Maintained protected 'main' branch for stable releases and created lightweight feature branches for each sub-system."),
        ("Basic CLI Commands Only:", " Strict adherence to fundamental Git command-line instructions as prescribed in the curriculum."),
        ("Remote Synchronization:", " Configured GitHub remote origin for cloud backup, team code sharing, and public portfolio presentation.")
    ]
    for i, (hd, body) in enumerate(points_vcs2):
        p = tf_vcs2.paragraphs[0] if i == 0 else tf_vcs2.add_paragraph()
        p.text = f"• {hd}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.font.name = "Segoe UI"
        if i > 0: p.space_before = Pt(12)
        run = p.add_run()
        run.text = body
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 8: Git CLI Commands - Part 1 (Setup & Staging)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Basic GitHub CLI Commands Used (Part 1)", "GIT COMMAND REFERENCE")

    cmds_p1 = [
        ("1. git init", "git init", "Initializes a brand-new Git repository in the project root directory, creating the hidden .git directory.", PRIMARY_CYAN),
        ("2. git status", "git status", "Displays the working tree status, showing tracked, modified, and untracked files awaiting staging.", ACCENT_BLUE),
        ("3. git add .", "git add .  (or git add <file>)", "Stages working directory changes to the Git Index in preparation for committing.", ACCENT_GREEN),
        ("4. git commit -m", 'git commit -m "feat: initial commit"', "Records staged snapshots permanently into local repository history with an atomic message.", ACCENT_YELLOW),
        ("5. git branch -M", "git branch -M main", "Renames the active default branch to 'main', conforming to modern Git/GitHub standards.", ACCENT_RED),
    ]

    for idx, (label, cmd_str, purpose, clr) in enumerate(cmds_p1):
        y = Inches(1.75) + idx * Inches(1.05)
        card_c = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.95))
        card_c.fill.solid()
        card_c.fill.fore_color.rgb = CARD_BG
        card_c.line.color.rgb = clr
        card_c.line.width = Pt(1.5)

        tf = card_c.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{label}  ➤  "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = clr
        p.font.name = "Segoe UI"

        run_cmd = p.add_run()
        run_cmd.text = f"`{cmd_str}`\n"
        run_cmd.font.bold = True
        run_cmd.font.color.rgb = TEXT_WHITE

        run_desc = p.add_run()
        run_desc.text = f"Purpose: {purpose}"
        run_desc.font.size = Pt(10)
        run_desc.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 9: Git CLI Commands - Part 2 (Branching & Remote)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Basic GitHub CLI Commands Used (Part 2)", "GIT COMMAND REFERENCE")

    cmds_p2 = [
        ("6. git checkout -b", "git checkout -b feature/image-detector", "Creates a new feature branch and immediately switches to it to isolate ongoing development.", PRIMARY_CYAN),
        ("7. git branch", "git branch", "Lists all local branches in the repository, with an asterisk (*) marking the currently active branch.", ACCENT_BLUE),
        ("8. git merge", "git checkout main && git merge feature/image-detector", "Integrates tested commits from a feature branch back into the main production branch.", ACCENT_GREEN),
        ("9. git remote add", "git remote add origin https://github.com/<user>/<repo>.git", "Registers the remote GitHub cloud repository URL under the standard alias 'origin'.", ACCENT_YELLOW),
        ("10. git push -u", "git push -u origin main", "Uploads local commits to GitHub and binds the local 'main' branch to the remote upstream.", ACCENT_RED),
    ]

    for idx, (label, cmd_str, purpose, clr) in enumerate(cmds_p2):
        y = Inches(1.75) + idx * Inches(1.05)
        card_c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.95))
        card_c.fill.solid()
        card_c.fill.fore_color.rgb = CARD_BG
        card_c.line.color.rgb = clr
        card_c.line.width = Pt(1.5)

        tf = card_c.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{label}  ➤  "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = clr
        p.font.name = "Segoe UI"

        run_cmd = p.add_run()
        run_cmd.text = f"`{cmd_str}`\n"
        run_cmd.font.bold = True
        run_cmd.font.color.rgb = TEXT_WHITE

        run_desc = p.add_run()
        run_desc.text = f"Purpose: {purpose}"
        run_desc.font.size = Pt(10)
        run_desc.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 10: Experimental Results & Demonstration
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Practical Demonstration & Testing Results", "VALIDATION")

    test_results = [
        ("sample_stable_diffusion.png", "Image (PNG)", "99.13%", "AI_GENERATED", "Stable Diffusion", "Prompt: 'cyberpunk street at night, neon lights...'", ACCENT_RED),
        ("sample_adobe_firefly.jpg", "Image (JPEG)", "99.90%", "AI_GENERATED", "Adobe Firefly", "XMP IPTC: trainedAlgorithmicMedia tag found", ACCENT_RED),
        ("sample_comfyui.png", "Image (PNG)", "99.25%", "AI_GENERATED", "ComfyUI", "KSampler & CLIPTextEncode graph recovered", ACCENT_RED),
        ("sample_chatgpt_document.pdf", "Document (PDF)", "99.00%", "AI_GENERATED", "ChatGPT", "PDF Producer & conversational text boilerplate", ACCENT_YELLOW),
        ("sample_suno_ai.mp3", "Audio (MP3)", "85.50%", "AI_GENERATED", "Suno AI Music", "ID3v2 tags tagged with Suno AI v3.5 encoder", ACCENT_YELLOW),
        ("sample_natural_camera.jpg", "Image (JPEG)", "5.00%", "NATURAL", "None", "Authentic Canon 5D Mark IV EXIF hardware tags", ACCENT_GREEN),
    ]

    # Top summary card
    tf_sum = add_card(s10, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.7))
    p_s = tf_sum.paragraphs[0]
    p_s.text = "🧪 Benchmark Test Results: Automated unit test suite executed 6 test cases with 100% accuracy and 0.036s latency."
    p_s.font.size = Pt(11)
    p_s.font.bold = True
    p_s.font.color.rgb = PRIMARY_CYAN

    # Table of Results
    for idx, (fname, ftype, conf, verdict, app, note, clr) in enumerate(test_results):
        y = Inches(2.65) + idx * Inches(0.72)
        row_s = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.65))
        row_s.fill.solid()
        row_s.fill.fore_color.rgb = CARD_BG
        row_s.line.color.rgb = clr
        row_s.line.width = Pt(1)

        tf_r = row_s.text_frame
        tf_r.word_wrap = True
        p_r = tf_r.paragraphs[0]
        p_r.text = f"{fname}  |  {ftype}  |  "
        p_r.font.size = Pt(10)
        p_r.font.color.rgb = TEXT_WHITE
        p_r.font.name = "Segoe UI"

        r_v = p_r.add_run()
        r_v.text = f"Verdict: {verdict} ({conf})  |  "
        r_v.font.bold = True
        r_v.font.color.rgb = clr

        r_app = p_r.add_run()
        r_app.text = f"Platform: {app}  |  {note}"
        r_app.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 11: Team Contribution Matrix
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Team Contributions & Task Allocation", "TEAM WORK MATRIX")

    team_data = [
        ("Satvik Sureka", "2581276", "Team Lead & Engine Architect", [
            "Repository architecture & Git origin setup",
            "Image metadata detector (PNG tEXt/iTXt parser)",
            "Stable Diffusion prompt extraction logic",
            "Main integration & unit test runner"
        ], PRIMARY_CYAN),
        ("Samarth Mahajan", "2581419", "Document Forensics Engineer", [
            "PDF document metadata parser (pypdf)",
            "Linguistic watermark signature scanner",
            "ChatGPT & Claude document identification",
            "Branch creation & PR merge coordination"
        ], ACCENT_BLUE),
        ("Gourang Jawa", "2581080", "Audio Forensics & Scoring Lead", [
            "Audio ID3v2 & RIFF header scanner",
            "Probabilistic confidence scoring formula",
            "Automated unit testing suite (test_detector.py)",
            "Git status auditing and conflict prevention"
        ], ACCENT_GREEN),
        ("Vedansh Dhawana", "2581314", "UI/UX & Documentation Specialist", [
            "Interactive CLI interface using rich library",
            "Tkinter Desktop GUI implementation",
            "Comprehensive README.md documentation",
            "Project Presentation deck (.pptx) authoring"
        ], ACCENT_YELLOW)
    ]

    for idx, (name, roll, role, tasks, clr) in enumerate(team_data):
        x = Inches(0.8) + idx * Inches(2.98)
        tf_tm = add_card(s11, x, Inches(1.8), Inches(2.8), Inches(5.0), name, clr)
        p_r = tf_tm.paragraphs[0]
        p_r.text = f"Roll: {roll}\nRole: {role}"
        p_r.font.size = Pt(11)
        p_r.font.bold = True
        p_r.font.color.rgb = clr
        p_r.font.name = "Segoe UI"

        for t in tasks:
            p_t = tf_tm.add_paragraph()
            p_t.text = f"✔ {t}"
            p_t.font.size = Pt(10)
            p_t.font.color.rgb = TEXT_MUTED
            p_t.font.name = "Segoe UI"
            p_t.space_before = Pt(8)

    # ==========================================
    # SLIDE 12: Future Scope & Enhancements
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Future Scope & Technological Enhancements", "ROADMAP")

    future_points = [
        ("C2PA Cryptographic Signature Verification", "Integrate full X.509 certificate chain validation for C2PA / Content Credentials to verify that claims were signed by accredited authorities.", PRIMARY_CYAN),
        ("Deep Learning Latent Watermark Extraction", "Implement frequency-domain decoders (such as Google SynthID or Meta Stable Signature) to detect imperceptible watermarks even when metadata has been stripped.", ACCENT_BLUE),
        ("Browser Extension for Instant Web Auditing", "Package the detection engine as a Chrome/Firefox WebExtension that overlays authenticity badges on social media feeds (Twitter, Instagram, Reddit).", ACCENT_GREEN),
        ("CI/CD Pipeline with GitHub Actions", "Expand VCS practices by adding automated GitHub Actions workflows to run unit tests and vulnerability scans on every push and pull request.", ACCENT_YELLOW)
    ]

    for idx, (title, desc, clr) in enumerate(future_points):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8) + col * Inches(6.0)
        y = Inches(1.8) + row * Inches(2.4)
        tf_fut = add_card(s12, x, y, Inches(5.7), Inches(2.1), f"🚀  {title}", clr)
        p = tf_fut.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 13: Conclusion & Acknowledgments
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Conclusion & Acknowledgments", "FINAL SUMMARY")

    tf_c_left = add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Key Project Takeaways", PRIMARY_CYAN)
    takeaways = [
        ("Functional Digital Forensics:", " Successfully created an AI metadata detector that parses PNG chunks, EXIF, XMP, PDF, and audio headers with 99%+ confidence."),
        ("VCS Discipline:", " Mastered fundamental Git/GitHub CLI commands: git init, status, add, commit, branch, merge, and push."),
        ("Teamwork & Collaboration:", " Distributed engineering responsibilities cleanly across 4 team members with modular software design."),
        ("Explainable AI Detection:", " Provided transparent indicators and prompt extraction rather than relying on unreliable black-box models.")
    ]
    for i, (hd, body) in enumerate(takeaways):
        p = tf_c_left.paragraphs[0] if i == 0 else tf_c_left.add_paragraph()
        p.text = f"• {hd}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.font.name = "Segoe UI"
        if i > 0: p.space_before = Pt(12)
        run = p.add_run()
        run.text = body
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED

    tf_c_right = add_card(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "Special Acknowledgments", ACCENT_GREEN)
    p_ack1 = tf_c_right.paragraphs[0]
    p_ack1.text = "Sincere Gratitude to our Course Guide:"
    p_ack1.font.size = Pt(13)
    p_ack1.font.bold = True
    p_ack1.font.color.rgb = TEXT_WHITE

    p_ack2 = tf_c_right.add_paragraph()
    p_ack2.text = "Dr. Pooja Batra"
    p_ack2.font.size = Pt(22)
    p_ack2.font.bold = True
    p_ack2.font.color.rgb = PRIMARY_CYAN
    p_ack2.space_before = Pt(8)

    p_ack3 = tf_c_right.add_paragraph()
    p_ack3.text = "We extend our deepest gratitude to Dr. Pooja Batra for her invaluable guidance, rigorous academic standards, and mentorship throughout the Version Control Systems laboratory curriculum."
    p_ack3.font.size = Pt(12)
    p_ack3.font.color.rgb = TEXT_MUTED
    p_ack3.space_before = Pt(10)

    p_ack4 = tf_c_right.add_paragraph()
    p_ack4.text = "💬 Questions & Discussion Welcome!"
    p_ack4.font.size = Pt(16)
    p_ack4.font.bold = True
    p_ack4.font.color.rgb = ACCENT_YELLOW
    p_ack4.space_before = Pt(28)

    # Save presentation
    prs.save(filename)
    print(f"[+] Successfully generated presentation: {filename}")


if __name__ == "__main__":
    create_deck()
