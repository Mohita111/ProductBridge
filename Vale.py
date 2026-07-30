import os
import re
import subprocess
import gradio as gr

<<<<<<< HEAD
LOG_FILE_NAME = "vale_output.txt"


def strip_ansi_codes(text):
    """Removes ANSI formatting / terminal color codes."""
    ansi_escape = re.compile(
        r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\d+m|\[0m"
    )
    return ansi_escape.sub("", text)


def run_and_parse_vale():
    """Executes Vale CLI, saves output to LOG_FILE_NAME, and returns rows for the Gradio table."""
    # 1. Execute Vale CLI capturing both STDOUT and STDERR
    try:
        proc = subprocess.run(
            ["vale", "--minAlertLevel=suggestion", "docs"],
=======
LOG_FILE = "vale_output.txt"
DOCS_DIR = "docs"


def parse_vale(text):
    rows = []
    current_file = ""

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        # File path lines don't start with "number:number"
        if not re.match(r"^\d+:\d+", line):
            current_file = os.path.basename(line.replace("\\", "/"))
            continue

        # Alert line: "15:5  error  Message here  Rule.Name"
        m = re.match(r"^(\d+):(\d+)\s+(\w+)\s+(.+?)\s+(\S+)$", line)
        if m:
            rows.append([current_file or "unknown", f"{m[1]}:{m[2]}", m[3], m[4], m[5]])

    return rows


def load():
    if not os.path.exists(LOG_FILE):
        return [["", "", "INFO", f"{LOG_FILE} not found. Click Re-Scan.", ""]]

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        rows = parse_vale(f.read())

    if not rows:
        return [["", "", "INFO", "No issues found. Your docs are clean!", ""]]

    return rows


def scan():
    try:
        r = subprocess.run(
            ["vale", DOCS_DIR],
>>>>>>> 3814434e42a4c9da0084966b612b80a2d7d72da4
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
<<<<<<< HEAD
            shell=True,
        )

        # Merge stdout and stderr content
        cli_output = proc.stdout if proc.stdout.strip() else proc.stderr

        # Save to LOG_FILE_NAME
        with open(LOG_FILE_NAME, "w", encoding="utf-8") as f:
            f.write(cli_output)

    except Exception as e:
        return [["System Setup", "ERROR", f"Failed to execute Vale CLI: {str(e)}"]]

    # 2. Read back from LOG_FILE_NAME
    if not os.path.exists(LOG_FILE_NAME):
        return [["System Setup", "WARNING", f"Could not find '{LOG_FILE_NAME}'."]]

    with open(LOG_FILE_NAME, "r", encoding="utf-8", errors="replace") as f:
        text_lines = f.readlines()

    formatted_rows = []
    current_topic = "General"

    for line in text_lines:
        clean_line = strip_ansi_codes(line).strip()
        if not clean_line:
            continue

        # A) Match File Header (e.g. "docs/intro.md", "\docs\getting-started\Public Portal.md", or "✔ 0 errors in intro.md")
        if (
            "docs" in clean_line.lower()
            or clean_line.endswith(".md")
            or clean_line.endswith(".mdx")
        ) and not re.match(r"^\s*\d+:\d+", clean_line):
            normalized_path = clean_line.replace("\\", "/")
            # Extract only the file name (e.g., 'Public Portal.md')
            extracted_filename = os.path.basename(normalized_path).strip()
            # Clean off any leading status checks or numbers if present
            extracted_filename = re.sub(
                r"^[✔✖✔\s\d]+(?:errors?|warnings?|suggestions?)?\s+(?:in\s+)?",
                "",
                extracted_filename,
                flags=re.IGNORECASE,
            )
            if extracted_filename:
                current_topic = extracted_filename
            continue

        # B) Match Alert Line (e.g., " 12:4 error Use 'backend' instead of 'back-end'. Google.Spelling")
        match_prefix = re.match(r"^\s*\d+:\d+", clean_line)
        if match_prefix:
            line_without_num = clean_line[match_prefix.end() :].strip()

            severity_match = re.match(
                r"^(error|warning|suggestion|info)\b",
                line_without_num,
                re.IGNORECASE,
            )

            if severity_match:
                severity = severity_match.group(1).upper()
                remainder = line_without_num[severity_match.end() :].strip()

                # Separate message text from trailing rule check ID
                remainder_parts = remainder.rsplit(None, 1)
                if len(remainder_parts) == 2:
                    message = f"{remainder_parts[0].strip()} [{remainder_parts[1].strip()}]"
                else:
                    message = remainder

                formatted_rows.append([current_topic, severity, message])

    # 3. Fallback if no issues detected
    if not formatted_rows:
        return [
            [
                "System Status",
                "INFO",
                "No styling issues detected. Your documentation is clean!",
            ]
        ]

    return formatted_rows


# =====================================================================
# GRADIO UI SETUP
# =====================================================================
initial_rows = run_and_parse_vale()

with gr.Blocks(title="Vale Local Report Portal") as demo:
    gr.Markdown("# 📋 Vale Style Guide Audit Report")
    gr.Markdown(
        f"### 📊 Automated View: Displaying **{len(initial_rows)}** record(s) loaded directly from `{LOG_FILE_NAME}`."
    )

    refresh_btn = gr.Button("🔄 Re-Scan Docs", variant="primary")

    interactive_grid = gr.Dataframe(
        value=initial_rows,
        headers=["Topic", "Severity", "Style Guide Recommendation"],
        datatype=["str", "str", "str"],
        row_count=15,
        interactive=False,
        wrap=True,
    )

    refresh_btn.click(fn=run_and_parse_vale, outputs=interactive_grid)

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7890,
        theme=gr.themes.Soft(),
        inbrowser=True,
    )
=======
        )
        # Vale exits with code 1 when it finds issues; that's normal
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(r.stdout)
            if r.stderr:
                f.write("\n" + r.stderr)
    except FileNotFoundError:
        return [["", "", "ERROR", "Vale CLI not found in PATH.", ""]]
    except Exception as e:
        return [["", "", "ERROR", str(e), ""]]

    return load()


with gr.Blocks(title="Vale Report") as demo:
    gr.Markdown("# Vale Style Guide Audit Report")
    gr.Button("Re-Scan Docs").click(scan, outputs=gr.Dataframe(
        value=load,
        headers=["File", "Line:Col", "Severity", "Message", "Rule"],
        interactive=False,
    ))

demo.launch(server_name="127.0.0.1", server_port=7890)
>>>>>>> 3814434e42a4c9da0084966b612b80a2d7d72da4
