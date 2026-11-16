import argparse
import sys
import os
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from .engine import AIMetadataEngine
from .models import Verdict, DetectionResult

console = Console()

PROJECT_INFO = """
[bold cyan]AI Metadata Detector (AIMetaDetect)[/bold cyan]
[yellow]Subject:[/yellow] Version Control Systems (VCS) Laboratory Project
[yellow]Faculty Guide:[/yellow] [bold white]Dr. Pooja Batra[/bold white]

[bold green]Student Contributors (B.Tech 2nd Year):[/bold green]
  • [white]Satvik Sureka[/white]  (Roll: [cyan]2581276[/cyan])
  • [white]Samarth Mahajan[/white] (Roll: [cyan]2581419[/cyan])
  • [white]Gourang Jawa[/white]   (Roll: [cyan]2581080[/cyan])
  • [white]Vedansh Dhawana[/white] (Roll: [cyan]2581314[/cyan])
"""


def render_single_result(res: DetectionResult):
    verdict_colors = {
        Verdict.AI_GENERATED: "bold red",
        Verdict.LIKELY_AI: "bold yellow",
        Verdict.SUSPICIOUS: "yellow",
        Verdict.NATURAL_OR_STRIPPED: "bold green",
        Verdict.UNKNOWN: "dim",
    }
    v_style = verdict_colors.get(res.verdict, "white")

    header_text = Text()
    header_text.append(f"File: {res.filename}\n", style="bold white")
    header_text.append(f"Type: {res.file_type} | Size: {res.file_size_bytes:,} bytes\n", style="dim")
    header_text.append(f"Verdict: {res.verdict.value} ", style=v_style)
    header_text.append(f"({res.confidence_score}% Confidence)\n", style=v_style)

    if res.primary_ai_app:
        header_text.append(f"Detected Platform: {res.primary_ai_app}\n", style="bold magenta")
    if res.model_name_extracted:
        header_text.append(f"Model/Checkpoint: {res.model_name_extracted}\n", style="cyan")

    console.print(Panel(header_text, title="🔍 Scan Summary", border_style="cyan"))

    if res.prompt_extracted:
        console.print(Panel(f"[italic]{res.prompt_extracted}[/italic]", title="📝 Extracted Generation Prompt", border_style="yellow"))

    if res.detected_indicators:
        table = Table(title="📌 Detected AI Indicators & Metadata Chunks", box=box.ROUNDED)
        table.add_column("Source", style="cyan", no_wrap=True)
        table.add_column("Tag / Key", style="yellow")
        table.add_column("Detected Tool", style="magenta")
        table.add_column("Details", style="white")

        for ind in res.detected_indicators:
            table.add_row(ind.source, ind.key, ind.app_detected, ind.description)
        console.print(table)
    else:
        console.print("[dim green]✔ No explicit AI generator metadata chunks found.[/dim green]\n")


def render_batch_results(results):
    table = Table(title=f"📊 Batch Scan Results ({len(results)} files)", box=box.HEAVY_EDGE)
    table.add_column("Filename", style="bold cyan")
    table.add_column("Type", style="dim")
    table.add_column("AI Detected?", justify="center")
    table.add_column("Confidence", justify="right")
    table.add_column("Platform / Tool", style="magenta")

    for res in results:
        status = "[red]YES[/red]" if res.is_ai_generated else "[green]NO[/green]"
        conf_style = "red" if res.confidence_score > 60 else "green"
        table.add_row(
            res.filename,
            res.file_type,
            status,
            f"[{conf_style}]{res.confidence_score}%[/{conf_style}]",
            res.primary_ai_app or "[dim]N/A[/dim]"
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description="AIMetaDetect - AI Metadata Detector for Multimedia & Documents"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: scan
    scan_p = subparsers.add_parser("scan", help="Scan a single file for AI metadata")
    scan_p.add_argument("file", help="Path to image, PDF, or audio file")

    # Command: batch
    batch_p = subparsers.add_parser("batch", help="Scan an entire folder")
    batch_p.add_argument("directory", help="Folder containing media files")
    batch_p.add_argument("--json", help="Optional path to export JSON results")

    # Command: info
    subparsers.add_parser("info", help="Show project and VCS academic details")

    # Command: vcs-guide
    subparsers.add_parser("vcs-guide", help="Show Git commands used in project lifecycle")

    args = parser.parse_args()

    if args.command == "info" or not args.command:
        console.print(Panel(PROJECT_INFO, border_style="blue", title="🎓 VCS Project Header"))
        if not args.command:
            parser.print_help()
        sys.exit(0)

    elif args.command == "vcs-guide":
        guide_text = """
[bold yellow]Basic Git/GitHub CLI Commands Used for this Project:[/bold yellow]

1. [bold cyan]git init[/bold cyan]
   Initializes the local repository in this project directory.

2. [bold cyan]git status[/bold cyan]
   Inspects tracked and untracked files in the working directory.

3. [bold cyan]git add .[/bold cyan]
   Stages all source code, tests, and presentation assets.

4. [bold cyan]git commit -m "feat: initial commit of AI Metadata Detector engine"[/bold cyan]
   Records staged changes into the local git commit history.

5. [bold cyan]git branch -M main[/bold cyan]
   Renames default branch to 'main'.

6. [bold cyan]git checkout -b feature/image-detector[/bold cyan]
   Creates and switches to a dedicated feature branch for modular development.

7. [bold cyan]git checkout main && git merge feature/image-detector[/bold cyan]
   Integrates completed feature branches back into the production branch.

8. [bold cyan]git remote add origin https://github.com/<username>/<repo>.git[/bold cyan]
   Links the local repository to the GitHub remote repository.

9. [bold cyan]git push -u origin main[/bold cyan]
   Pushes the commits to GitHub and sets upstream tracking.
"""
        console.print(Panel(guide_text, title="💻 VCS Command Reference", border_style="green"))
        sys.exit(0)

    elif args.command == "scan":
        if not os.path.exists(args.file):
            console.print(f"[bold red]Error:[/bold red] File not found: {args.file}")
            sys.exit(1)
        with console.status("[bold green]Scanning file metadata..."):
            res = AIMetadataEngine.scan_file(args.file)
        render_single_result(res)

    elif args.command == "batch":
        if not os.path.isdir(args.directory):
            console.print(f"[bold red]Error:[/bold red] Directory not found: {args.directory}")
            sys.exit(1)
        with console.status("[bold green]Scanning folder files..."):
            results = AIMetadataEngine.scan_directory(args.directory)
        render_batch_results(results)

        if args.json:
            export_data = []
            for r in results:
                export_data.append({
                    "filename": r.filename,
                    "file_type": r.file_type,
                    "is_ai_generated": r.is_ai_generated,
                    "confidence_score": r.confidence_score,
                    "primary_ai_app": r.primary_ai_app,
                    "prompt_extracted": r.prompt_extracted,
                    "model_name": r.model_name_extracted,
                    "indicators_count": len(r.detected_indicators)
                })
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2)
            console.print(f"[bold green]✔ Results saved to {args.json}[/bold green]")


if __name__ == "__main__":
    main()
