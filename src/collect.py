import json, os, random, datetime, argparse

def collect_mock(raw_dir: str):
    os.makedirs(raw_dir, exist_ok=True)
    events = []
    rules = ["SPF_FAIL", "PHISH_URL", "MAL_ATTACH", "DMARC_FAIL", "BEC_LIKE", "CLEAN"]
    senders = ["badguy@phish.com", "hr@payro1l.example", "it-support@fakecorp.com", "trusted@partner.com"]

    for i in range(100):
        evt = {
            "ts": datetime.datetime.utcnow().isoformat(),
            "from": random.choice(senders),
            "subject": f"Test message {i}",
            "rule": random.choice(rules),
            "action": "quarantined" if random.random() > 0.3 else "delivered"
        }
        events.append(evt)

    out_file = os.path.join(raw_dir, "events.jsonl")
    with open(out_file, "w") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")

    print(f"[collect] {len(events)} mock events written to {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_dir", default="data/raw")
    args = parser.parse_args()
    collect_mock(args.raw_dir)
