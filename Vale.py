import os
import re
import json
import subprocess
import gradio as gr
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import pandas as pd


# ─── Configuration ───────────────────────────────────────────────────────────
DEFAULT_LOG_FILE = "vale_output.txt"
DEFAULT_CONFIG_FILE = "vale.ini"
DOCS_DIR = "docs"  # Adjust to your docs folder


@dataclass
class ValeAlert:
    file: str
    line: int
    col: int
    severity: str
    message: str
    rule: str
    raw: str = ""

    @property
    def topic(self) -> str:
        return Path(self.file).name

    @property
    def severity_color(self) -> str:
        return {
            "error": "#EF4444",
            "warning": "#F59E0B",
            "suggestion": "#3B82F6",
        }.get(self.severity.lower(), "#6B7280")


class ValeParser:
    """Robust parser for Vale CLI text output."""

    SEVERITY_PATTERN = re.compile(
        r"^\s*(\d+):(\d+)\s+(error|warning|suggestion)\s+(.+?)\s+(\S+)$",
        re.IGNORECASE,
    )

    @staticmethod
    def strip_ansi(text: str) -> str:
        ansi_escape = re.compile(
            r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
        )
        return ansi_escape.sub('', text)

    @classmethod
    def parse_text_output(cls, raw_text: str) -> List[ValeAlert]:
        alerts = []
        current_file = "unknown.md"
        lines = raw_text.splitlines()

        for line in lines:
            clean = cls.strip_ansi(line).rstrip()
            if not clean:
                continue

            # Detect file header: path ending in .md or containing docs/
            if clean.endswith(('.md', '.mdx', '.rst', '.adoc')) or (
                os.path.sep in clean and not re.match(r"^\d+:\d+", clean.strip())
            ):
                current_file = clean.strip().replace("\\", "/")
                continue

            # Parse alert line: "15:5 error Message text RuleName"
            match = cls.SEVERITY_PATTERN.match(clean)
            if match:
                line_num, col_num, severity, message, rule = match.groups()
                alerts.append(ValeAlert(
                    file=current_file,
                    line=int(line_num),
                    col=int(col_num),
                    severity=severity.lower(),
                    message=message.strip(),
                    rule=rule.strip(),
                    raw=clean,
                ))
        return alerts

    @classmethod
    def parse_json_output(cls, raw_text: str) -> List[ValeAlert]:
        """Parse Vale's --output=JSON format (preferred)."""
        alerts = []
        try:
            data = json.loads(raw_text)
            for file_path, file_alerts in data.items():
                for alert in file_alerts:
                    alerts.append(ValeAlert(
                        file=file_path,
                        line=alert.get("Line", 0),
                        col=alert.get("Span", [0, 0])[0],
                        severity=alert.get("Severity", "unknown").lower(),
                        message=alert.get("Message", ""),
                        rule=alert.get("Check", ""),
                    ))
        except json.JSONDecodeError:
            pass
        return alerts


class ValeRunner:
    """Handles live execution of Vale CLI."""

    @staticmethod
    def is_available() -> bool:
        try:
            subprocess.run(
                ["vale", "--version"],
                capture_output=True,
                check=True,
                timeout=5,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @classmethod
    def scan(cls, target_dir: str = DOCS_DIR, config: str = DEFAULT_CONFIG_FILE) -> str:
        if not cls.is_available():
            raise RuntimeError("Vale CLI not found in PATH. Install from https://vale.sh")

        cmd = [
            "vale",
            "--config", config,
            "--no-exit",
            target_dir,
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        # Vale returns non-zero when alerts exist; that's expected
        return result.stdout + result.stderr


# ─── UI Helpers ──────────────────────────────────────────────────────────────

def severity_badge(sev: str) -> str:
    colors = {
        "error": ("#FEE2E2", "#DC2626", "#EF4444"),
        "warning": ("#FEF3C7", "#D97706", "#F59E0B"),
        "suggestion": ("#DBEAFE", "#2563EB", "#3B82F6"),
    }
    bg, text, border = colors.get(sev.lower(), ("#F3F4F6", "#4B5563", "#6B7280"))
    return (
        f'<span style="display:inline-block;padding:2px 10px;border-radius:999px;'
        f'background:{bg};color:{text};border:1px solid {border};font-size:12px;'
        f'font-weight:600;text-transform:uppercase;">{sev}</span>'
    )


def make_dataframe(alerts: List[ValeAlert]) -> pd.DataFrame:
    if not alerts:
        return pd.DataFrame(columns=["File", "Line", "Severity", "Rule", "Message"])

    rows = []
    for a in alerts:
        rows.append({
            "File": a.topic,
            "Line": a.line,
            "Severity": severity_badge(a.severity),
            "Rule": f"`{a.rule}`",
            "Message": a.message,
        })
    return pd.DataFrame(rows)


def get_stats(alerts: List[ValeAlert]) -> dict:
    total = len(alerts)
    errors = sum(1 for a in alerts if a.severity == "error")
    warnings = sum(1 for a in alerts if a.severity == "warning")
    suggestions = sum(1 for a in alerts if a.severity == "suggestion")
    files = len(set(a.file for a in alerts))
    return {
        "total": total,
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions,
        "files": files,
    }


# ─── Event Handlers ───────────────────────────────────────────────────────────

def load_from_file(file_path: str = DEFAULT_LOG_FILE) -> tuple:
    if not os.path.exists(file_path):
        empty_df = make_dataframe([])
        return (
            empty_df,
            "0",
            "0",
            "0",
            "0",
            "0",
            f"⚠️ File not found: `{file_path}`. Run Vale first or upload output.",
        )

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    # Try JSON first, fall back to text
    alerts = ValeParser.parse_json_output(raw) or ValeParser.parse_text_output(raw)
    df = make_dataframe(alerts)
    stats = get_stats(alerts)

    status = (
        f"✅ Loaded {stats['total']} alerts from `{file_path}`"
        if alerts
        else f"ℹ️ No alerts found in `{file_path}`. Your docs are clean!"
    )

    return (
        df,
        str(stats["total"]),
        str(stats["errors"]),
        str(stats["warnings"]),
        str(stats["suggestions"]),
        str(stats["files"]),
        status,
    )


def run_live_scan() -> tuple:
    try:
        raw = ValeRunner.scan()
        # Save for future reference
        with open(DEFAULT_LOG_FILE, "w", encoding="utf-8") as f:
            f.write(raw)
        alerts = ValeParser.parse_text_output(raw)
        df = make_dataframe(alerts)
        stats = get_stats(alerts)
        status = f"🔄 Live scan complete: {stats['total']} alerts detected."
        return (
            df,
            str(stats["total"]),
            str(stats["errors"]),
            str(stats["warnings"]),
            str(stats["suggestions"]),
            str(stats["files"]),
            status,
        )
    except Exception as e:
        empty_df = make_dataframe([])
        return (
            empty_df, "0", "0", "0", "0", "0",
            f"❌ Scan failed: {str(e)}",
        )


def upload_and_parse(file) -> tuple:
    if file is None:
        return load_from_file()
    # Gradio file object has .name path
    return load_from_file(file.name)


def filter_results(df: pd.DataFrame, severity_filter: List[str], search: str) -> pd.DataFrame:
    if df.empty:
        return df

    # Severity filter uses the HTML badge text, so we parse the raw severity back
    # Actually easier: keep alerts in state. But for simplicity with Gradio,
    # we'll re-parse from the stored file or accept that filtering is limited.
    # Better approach: store alerts in a global or use gr.State.

    # Since DataFrame has HTML in Severity, we filter on File/Line/Message
    mask = pd.Series([True] * len(df), index=df.index)
    if search:
        mask &= df.astype(str).apply(
            lambda row: search.lower() in row.to_string().lower(), axis=1
        )
    return df[mask]


# ─── Gradio Interface ────────────────────────────────────────────────────────

custom_css = """
.stat-box {
    text-align: center;
    padding: 16px;
    border-radius: 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}
.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
}
.stat-label {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.error-box .stat-number { color: #dc2626; }
.warning-box .stat-number { color: #d97706; }
.suggestion-box .stat-number { color: #2563eb; }
.gr-dataframe th {
    background: #1e293b !important;
    color: white !important;
}
"""

with gr.Blocks(title="Vale Audit Dashboard", css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 📋 Vale Style Guide Audit Dashboard
        <p style="color:#64748b;margin-top:-10px;">
        Professional documentation linting reports — parse files, scan live, or upload output.
        </p>
        """
    )

    # ── Stats Row ──────────────────────────────────────────────────────────
    with gr.Row():
        with gr.Column(min_width=100):
            total_box = gr.Textbox(
                label="Total", value="0", interactive=False,
                container=False, elem_classes=["stat-box"]
            )
        with gr.Column(min_width=100):
            err_box = gr.Textbox(
                label="Errors", value="0", interactive=False,
                container=False, elem_classes=["stat-box", "error-box"]
            )
        with gr.Column(min_width=100):
            warn_box = gr.Textbox(
                label="Warnings", value="0", interactive=False,
                container=False, elem_classes=["stat-box", "warning-box"]
            )
        with gr.Column(min_width=100):
            sug_box = gr.Textbox(
                label="Suggestions", value="0", interactive=False,
                container=False, elem_classes=["stat-box", "suggestion-box"]
            )
        with gr.Column(min_width=100):
            file_box = gr.Textbox(
                label="Files", value="0", interactive=False,
                container=False, elem_classes=["stat-box"]
            )

    # ── Controls ───────────────────────────────────────────────────────────
    with gr.Row():
        with gr.Column(scale=2):
            status_text = gr.Textbox(
                label="Status",
                value="Ready. Load a file or run a live scan.",
                interactive=False,
            )
        with gr.Column(scale=1):
            with gr.Row():
                load_btn = gr.Button("📁 Load vale_output.txt", variant="secondary")
                scan_btn = gr.Button("🔄 Re-Scan Docs", variant="primary")
                upload_btn = gr.UploadButton("📤 Upload Vale Output", file_types=[".txt"])

    # ── Filters ────────────────────────────────────────────────────────────
    with gr.Row():
        search_box = gr.Textbox(
            label="Search",
            placeholder="Filter by message, rule, or filename...",
            interactive=True,
        )

    # ── Data Table ─────────────────────────────────────────────────────────
    results_table = gr.Dataframe(
        value=make_dataframe([]),
        headers=["File", "Line", "Severity", "Rule", "Message"],
        datatype=["str", "number", "html", "str", "str"],
        interactive=False,
        wrap=True,
        column_widths=["20%", "10%", "15%", "20%", "35%"],
    )

    # ── Config Viewer ──────────────────────────────────────────────────────
    with gr.Accordion("⚙️ View vale.ini Configuration", open=False):
        config_text = gr.Code(
            language="ini",
            label="vale.ini",
            value="; Configuration will load here...",
            interactive=False,
        )

    # ── Event Wiring ───────────────────────────────────────────────────────
    def update_all(source: str = "file", file_obj=None):
        if source == "upload" and file_obj:
            df, tot, err, warn, sug, fil, stat = upload_and_parse(file_obj)
        elif source == "live":
            df, tot, err, warn, sug, fil, stat = run_live_scan()
        else:
            df, tot, err, warn, sug, fil, stat = load_from_file()

        # Load config if exists
        cfg = "; vale.ini not found"
        if os.path.exists(DEFAULT_CONFIG_FILE):
            with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = f.read()

        return df, tot, err, warn, sug, fil, stat, cfg

    load_btn.click(
        fn=lambda: update_all("file"),
        outputs=[results_table, total_box, err_box, warn_box, sug_box, file_box, status_text, config_text],
    )
    scan_btn.click(
        fn=lambda: update_all("live"),
        outputs=[results_table, total_box, err_box, warn_box, sug_box, file_box, status_text, config_text],
    )
    upload_btn.upload(
        fn=lambda f: update_all("upload", f),
        inputs=upload_btn,
        outputs=[results_table, total_box, err_box, warn_box, sug_box, file_box, status_text, config_text],
    )

    # Auto-load on startup
    demo.load(
        fn=lambda: update_all("file"),
        outputs=[results_table, total_box, err_box, warn_box, sug_box, file_box, status_text, config_text],
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7890)