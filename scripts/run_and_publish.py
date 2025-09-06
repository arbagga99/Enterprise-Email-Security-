# Runs the mock pipeline and publishes outputs to docs/data for the live dashboard
import os, json, shutil
from datetime import datetime

# Allow imports from src/
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))  # .../scripts
REPO = os.path.abspath(os.path.join(ROOT, ".."))
sys.path.append(os.path.join(REPO, "src"))

from collect import collect_mock
from process import process_events
from summarize import summarize

RAW_DIR        = os.path.join(REPO, "data", "raw")
PROC_DIR       = os.path.join(REPO, "data", "processed")
SUMMARY_JSON   = os.path.join(REPO, "data", "summary.json")
ALERTS_JSON    = os.path.join(REPO, "data", "alerts.json")

DOCS_DIR       = os.path.join(REPO, "docs")
DOCS_DATA_DIR  = os.path.join(DOCS_DIR, "data")
DOCS_SUMMARY   = os.path.join(DOCS_DATA_DIR, "demo_summary.json")
DOCS_ALERTS    = os.path.join(DOCS_DATA_DIR, "demo_alerts.json")

def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROC_DIR, exist_ok=True)
    os.makedirs(DOCS_DATA_DIR, exist_ok=True)

    # 1) Generate mock events → raw
    collect_mock(RAW_DIR)

    # 2) Process → processed
    process_events(RAW_DIR, PROC_DIR)

    # 3) Summarize → data/summary.json + data/alerts.json
    summarize(PROC_DIR, SUMMARY_JSON, ALERTS_JSON)

    # 4) Publish to docs/data (the dashboard reads these)
    shutil.copyfile(SUMMARY_JSON, DOCS_SUMMARY)
    shutil.copyfile(ALERTS_JSON,  DOCS_ALERTS)

    # 5) Add timestamp marker (handy for debugging)
    stamp = {"last_published_at": datetime.utcnow().isoformat() + "Z"}
    with open(os.path.join(DOCS_DATA_DIR, "published.json"), "w") as f:
        json.dump(stamp, f, indent=2)

    print("[publish] Updated:", DOCS_SUMMARY, DOCS_ALERTS)

if __name__ == "__main__":
    main()
