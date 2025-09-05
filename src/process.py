import json, os, argparse

def process_events(raw_dir: str, processed_dir: str):
    os.makedirs(processed_dir, exist_ok=True)
    infile = os.path.join(raw_dir, "events.jsonl")
    outfile = os.path.join(processed_dir, "processed.jsonl")

    with open(infile) as f_in, open(outfile, "w") as f_out:
        for line in f_in:
            evt = json.loads(line)
            # normalize (simple pass-through here)
            evt["risk"] = "high" if evt["rule"] in ["PHISH_URL","MAL_ATTACH","BEC_LIKE"] else "low"
            f_out.write(json.dumps(evt) + "\n")

    print(f"[process] processed events written to {outfile}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_dir", default="data/raw")
    parser.add_argument("--processed_dir", default="data/processed")
    args = parser.parse_args()
    process_events(args.raw_dir, args.processed_dir)
