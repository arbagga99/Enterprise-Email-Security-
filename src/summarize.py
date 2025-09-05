import json, os, argparse, datetime
from collections import Counter

def summarize(processed_dir: str, summary_json: str, alerts_json: str):
    events = []
    infile = os.path.join(processed_dir, "processed.jsonl")
    with open(infile) as f:
        for line in f:
            events.append(json.loads(line))

    total = len(events)
    blocked_spam = sum(1 for e in events if e["rule"] == "SPF_FAIL")
    blocked_phish = sum(1 for e in events if e["rule"] == "PHISH_URL")
    false_pos = sum(1 for e in events if e["from"].endswith("partner.com"))

    rules_count = Counter([e["rule"] for e in events])
    senders_count = Counter([e["from"] for e in events])

    summary = {
        "run_at": datetime.datetime.utcnow().isoformat(),
        "scanned_messages": total,
        "blocked_spam": blocked_spam,
        "blocked_phishing": blocked_phish,
        "false_positives": false_pos,
        "top_rules": rules_count.most_common(5),
        "top_senders": senders_count.most_common(5)
    }

    alerts = [e for e in events if e["risk"] == "high"]

    with open(summary_json, "w") as f: json.dump(summary, f, indent=2)
    with open(alerts_json, "w") as f: json.dump(alerts, f, indent=2)

    print(f"[summarize] summary -> {summary_json}, alerts -> {alerts_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed_dir", default="data/processed")
    parser.add_argument("--summary_json", default="data/summary.json")
    parser.add_argument("--alerts_json", default="data/alerts.json")
    args = parser.parse_args()
    summarize(args.processed_dir, args.summary_json, args.alerts_json)
