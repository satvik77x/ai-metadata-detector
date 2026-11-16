#!/usr/bin/env python3
"""
AI Metadata Detector - Desktop GUI Application
Subject: Version Control Systems (VCS)
Faculty Mentor: Dr. Pooja Batra
Students: Satvik Sureka, Samarth Mahajan, Gourang Jawa, Vedansh Dhawana
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from aimeta.engine import AIMetadataEngine
from aimeta.models import Verdict


class AIMetadataGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AI Metadata Detector - VCS Academic Project")
        self.root.geometry("880x680")
        self.root.configure(bg="#0f172a")

        self._setup_styles()
        self._build_header()
        self._build_file_picker()
        self._build_results_panel()
        self._build_footer()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#1e293b", 
                        foreground="#f8fafc", 
                        fieldbackground="#1e293b", 
                        rowheight=26,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading", 
                        background="#334155", 
                        foreground="#38bdf8", 
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#0284c7")])

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=12)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(header_frame, text="🛡️ AI Metadata Detector", font=("Segoe UI", 18, "bold"), fg="#38bdf8", bg="#1e293b")
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(header_frame, 
                           text="Version Control Systems Project  |  Guide: Dr. Pooja Batra  |  B.Tech 2nd Year",
                           font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b")
        sub_lbl.pack(anchor="w", pady=(2, 0))

    def _build_file_picker(self):
        picker_frame = tk.Frame(self.root, bg="#0f172a", padx=20, pady=15)
        picker_frame.pack(fill=tk.X)

        lbl = tk.Label(picker_frame, text="Select Target File (PNG, JPG, PDF, MP3):", font=("Segoe UI", 10, "bold"), fg="#e2e8f0", bg="#0f172a")
        lbl.pack(anchor="w", pady=(0, 5))

        row = tk.Frame(picker_frame, bg="#0f172a")
        row.pack(fill=tk.X)

        self.path_var = tk.StringVar()
        self.entry = tk.Entry(row, textvariable=self.path_var, font=("Segoe UI", 10), bg="#1e293b", fg="#f8fafc", insertbackground="#38bdf8", relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 10))

        browse_btn = tk.Button(row, text="📁 Browse", font=("Segoe UI", 10, "bold"), bg="#334155", fg="#f8fafc", activebackground="#475569", relief=tk.FLAT, padx=15, command=self._browse_file)
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))

        scan_btn = tk.Button(row, text="⚡ Scan File", font=("Segoe UI", 10, "bold"), bg="#0284c7", fg="#ffffff", activebackground="#0369a1", relief=tk.FLAT, padx=18, command=self._scan_file)
        scan_btn.pack(side=tk.LEFT)

    def _build_results_panel(self):
        res_frame = tk.Frame(self.root, bg="#0f172a", padx=20, pady=5)
        res_frame.pack(fill=tk.BOTH, expand=True)

        # Status badge cards
        card_row = tk.Frame(res_frame, bg="#0f172a")
        card_row.pack(fill=tk.X, pady=(0, 10))

        self.verdict_card = tk.Label(card_row, text="Awaiting scan...", font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#94a3b8", padx=16, pady=8)
        self.verdict_card.pack(side=tk.LEFT, padx=(0, 10))

        self.confidence_card = tk.Label(card_row, text="Confidence: --%", font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#94a3b8", padx=16, pady=8)
        self.confidence_card.pack(side=tk.LEFT, padx=(0, 10))

        self.app_card = tk.Label(card_row, text="Platform: None", font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#94a3b8", padx=16, pady=8)
        self.app_card.pack(side=tk.LEFT)

        # Prompt card
        self.prompt_label = tk.Label(res_frame, text="", font=("Segoe UI", 9, "italic"), fg="#facc15", bg="#0f172a", wraplength=800, justify=tk.LEFT)
        self.prompt_label.pack(anchor="w", pady=(0, 8))

        # Metadata table
        table_frame = tk.Frame(res_frame, bg="#1e293b")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("source", "key", "app", "desc")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("source", text="Source Chunk")
        self.tree.heading("key", text="Tag / Header")
        self.tree.heading("app", text="AI Tool")
        self.tree.heading("desc", text="Description")

        self.tree.column("source", width=140, anchor="w")
        self.tree.column("key", width=160, anchor="w")
        self.tree.column("app", width=150, anchor="w")
        self.tree.column("desc", width=360, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_footer(self):
        footer = tk.Frame(self.root, bg="#1e293b", padx=20, pady=8)
        footer.pack(fill=tk.X)

        team_text = "Team: Satvik Sureka (2581276) | Samarth Mahajan (2581419) | Gourang Jawa (2581080) | Vedansh Dhawana (2581314)"
        lbl = tk.Label(footer, text=team_text, font=("Segoe UI", 8), fg="#64748b", bg="#1e293b")
        lbl.pack(side=tk.LEFT)

    def _browse_file(self):
        f = filedialog.askopenfilename(
            title="Select media file to inspect",
            filetypes=[
                ("Supported Files", "*.png *.jpg *.jpeg *.webp *.pdf *.txt *.mp3 *.wav"),
                ("Images", "*.png *.jpg *.jpeg *.webp"),
                ("Documents", "*.pdf *.txt"),
                ("All Files", "*.*")
            ]
        )
        if f:
            self.path_var.set(f)
            self._scan_file()

    def _scan_file(self):
        path = self.path_var.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("File Error", "Please select a valid existing file!")
            return

        # Clear existing table rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            res = AIMetadataEngine.scan_file(path)
            
            # Update verdict card
            if res.verdict == Verdict.AI_GENERATED:
                self.verdict_card.config(text="🚨 AI GENERATED", bg="#ef4444", fg="#ffffff")
            elif res.verdict == Verdict.LIKELY_AI:
                self.verdict_card.config(text="⚠️ LIKELY AI", bg="#f59e0b", fg="#ffffff")
            elif res.verdict == Verdict.SUSPICIOUS:
                self.verdict_card.config(text="❓ SUSPICIOUS", bg="#d97706", fg="#ffffff")
            else:
                self.verdict_card.config(text="✔ AUTHENTIC / STRIPPED", bg="#10b981", fg="#ffffff")

            self.confidence_card.config(text=f"Confidence: {res.confidence_score}%", fg="#38bdf8")
            self.app_card.config(text=f"Platform: {res.primary_ai_app or 'None detected'}", fg="#e2e8f0")

            if res.prompt_extracted:
                self.prompt_label.config(text=f"📝 Extracted Prompt: {res.prompt_extracted}")
            else:
                self.prompt_label.config(text="")

            for ind in res.detected_indicators:
                self.tree.insert("", tk.END, values=(ind.source, ind.key, ind.app_detected, ind.description))

        except Exception as e:
            messagebox.showerror("Scan Error", f"An error occurred while scanning: {e}")


def main():
    root = tk.Tk()
    app = AIMetadataGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
