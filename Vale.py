import os
import re
import subprocess
import gradio as gr

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
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
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