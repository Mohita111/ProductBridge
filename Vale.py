import os
import re
import subprocess
import gradio as gr

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
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
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