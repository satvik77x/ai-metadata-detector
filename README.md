# 🛡️ AI Metadata Detector (AIMetaDetect)
### Academic Laboratory Project for **Version Control Systems (VCS)**
**Department of Computer Science & Engineering | B.Tech 2nd Year**

---

## 👨‍🏫 Academic Information
* **Faculty Mentor / Course Guide:** **Dr. Pooja Batra**
* **Course:** Version Control Systems (VCS)
* **Team Members & Student Credentials:**
  1. **Satvik Sureka** — Roll No: `2581276`
  2. **Samarth Mahajan** — Roll No: `2581419`
  3. **Gourang Jawa** — Roll No: `2581080`
  4. **Vedansh Dhawana** — Roll No: `2581314`

---

## 📌 Project Overview
With the meteoric proliferation of Generative Artificial Intelligence (GenAI), distinguishing synthetic media from authentic human creations has become a paramount challenge in digital forensics, academic integrity, intellectual property protection, and cybersecurity.

**AIMetaDetect** is an open-source, modular digital forensics tool developed in Python. It inspects multimedia and document formats (`.png`, `.jpg`, `.pdf`, `.mp3`) to uncover hidden generative AI metadata signatures, embedded prompt sequences, generator hyperparameters, and cryptographic provenance manifests (C2PA/CAI) left behind by mainstream AI models.

### Supported AI Frameworks & Signatures:
* **Stable Diffusion (Automatic1111, WebUI, Forge):** Parses raw PNG `tEXt`/`iTXt` parameter chunks containing positive/negative prompts, seed, sampler, steps, CFG scale, and checkpoint hash.
* **ComfyUI:** Reconstructs and inspects embedded JSON execution graphs (`KSampler`, `CLIPTextEncode`, checkpoint names).
* **NovelAI:** Identifies anime diffusion tags and generation comment fields.
* **Adobe Firefly / Photoshop GenAI:** Extracts XMP packets containing IPTC Digital Source Type (`trainedAlgorithmicMedia`, `compositeSynthetic`) and `CreatorTool` tags.
* **Midjourney / DALL-E 3:** Scans EXIF UserComments and C2PA Content Credentials (`c2pa` JUMBF boxes).
* **LLM & PDF Generators (ChatGPT, Claude, Gemini):** Analyzes PDF document metadata (`Producer`, `Author`, `Subject`) and detects linguistic watermark signatures and prompt injection disclaimers.
* **AI Audio & Voice Cloning (Suno, Udio, ElevenLabs):** Inspects ID3v2 frames and RIFF metadata chunks.

---

## 🚀 Key Features
1. **Multi-Format Parsing Engine:** Supports PNG chunks, EXIF, XMP packets, C2PA manifests, PDF dictionaries, and ID3 tags.
2. **Confidence Scoring & Verdict:** Calculates weighted probabilistic AI likelihood ($0.0\% - 99.9\%$) and assigns standard forensic verdicts (`AI_GENERATED`, `LIKELY_AI`, `SUSPICIOUS`, `NATURAL_OR_STRIPPED`).
3. **Prompt & Model Extraction:** Automatically recovers the original text prompt used to synthesize the media whenever stored in the metadata.
4. **Rich Terminal CLI:** Interactive, colored status indicators, detailed tables, and batch scanning summaries using the Python `rich` library.
5. **Modern Desktop GUI:** Built-in Tkinter interface for interactive drag-and-drop demonstrations and presentations.
6. **Built-in Sample Generator & Unit Testing:** Comes with a synthetic test-asset generator and automated test suite.

---

## 💻 Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** and **Git** installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/<your-username>/ai-metadata-detector.git
cd ai-metadata-detector
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📖 Usage Instructions

### 1. Generate Test Assets
Generate sample images, PDFs, and audio files with authentic metadata:
```bash
python sample_generator.py
```

### 2. Scan a Single File (CLI)
```bash
python main.py scan samples/sample_stable_diffusion.png
```

### 3. Batch Scan an Entire Directory
```bash
python main.py batch samples
```
To export the batch results to a JSON report:
```bash
python main.py batch samples --json results.json
```

### 4. Launch Desktop GUI
```bash
python gui.py
```

### 5. Run Automated Unit Tests
```bash
python -m unittest tests/test_detector.py
```

---

## 🛠️ Version Control System (VCS) — Step-by-Step CLI Commands Used

This project was built from the ground up using **Git** and **GitHub** to apply professional industry VCS workflows. Below are the basic CLI commands utilized throughout our project lifecycle:

### Step 1: Local Repository Initialization
```bash
# Check installed Git version
git --version

# Configure global developer identity
git config --global user.name "Satvik Sureka"
git config --global user.email "satviksureka35@gmail.com"

# Initialize local git repository
git init
```

### Step 2: Checking Working Tree Status
```bash
# Inspect tracked, untracked, and modified files
git status
```

### Step 3: Staging Project Files
```bash
# Stage specific file
git add requirements.txt

# Or stage all project files and directories
git add .
```

### Step 4: Committing Changes
```bash
# Record staged snapshots into repository history with clear message
git commit -m "feat: initial commit of AI Metadata Detector engine"
```

### Step 5: Branch Management & Feature Isolation
To simulate a multi-contributor workflow among team members (Satvik, Samarth, Gourang, Vedansh):
```bash
# Create and switch to a feature branch for image detection module
git checkout -b feature/image-detector

# Verify active branches
git branch

# After developing and staging image detector changes:
git commit -m "feat(image): add PNG chunk parser and SD prompt extractor"

# Switch back to the main branch
git checkout main

# Merge feature branch into main
git merge feature/image-detector
```

### Step 6: Setting the Primary Branch
```bash
# Rename the default branch to 'main'
git branch -M main
```

### Step 7: Linking with GitHub Remote Repository
```bash
# Link local repository to remote GitHub repository
git remote add origin https://github.com/<github-username>/ai-metadata-detector.git

# Verify remote configuration
git remote -v
```

### Step 8: Pushing Changes to GitHub
```bash
# Push commits to remote origin and set upstream tracking
git push -u origin main
```

### Step 9: History and Log Inspection
```bash
# View concise commit history graph
git log --oneline --graph --decorate
```

---

## 👥 Team Work & Responsibility Matrix

| Member | Roll Number | Key Responsibilities & VCS Commits |
| :--- | :--- | :--- |
| **Satvik Sureka** | `2581276` | Project Lead, Git Repository Setup, Image Metadata Detector (PNG/EXIF/XMP). |
| **Samarth Mahajan** | `2581419` | Document Detector (PDF/TXT), LLM prompt marker identification, Branch merges. |
| **Gourang Jawa** | `2581080` | Audio Detector (ID3/RIFF), Confidence scoring engine, Unit test suite. |
| **Vedansh Dhawana** | `2581314` | CLI Interface (`rich`), Tkinter Desktop GUI, Documentation & Presentation PPT. |

---

## 📜 License
This project is licensed under the **MIT License** for academic and research purposes.
