import json, argparse

def render(summary_json: str, dashboard_html: str):
    with open(summary_json) as f:
        summary = json.load(f)

    html = f"""
    <html>
    <head><title>Email Security Dashboard</title></head>
    <body>
        <h1>Enterprise Email Security Digest</h1>
        <p><b>Run at:</b> {summary['run_at']}</p>
        <ul>
            <li>Total scanned: {summary['scanned_messages']}</li>
            <li>Blocked spam: {summary['blocked_spam']}</li>
            <li>Blocked phishing: {summary['blocked_phishing']}</li>
            <li>False positives: {summary['false_positives']}</li>
        </ul>
        <h2>Top Rules</h2>
        <pre>{summary['top_rules']}</pre>
        <h2>Top Senders</h2>
        <pre>{summary['top_senders']}</pre>
    </body>
    </html>
    """
    with open(dashboard_html, "w") as f:
        f.write(html)

    print(f"[render] dashboard written to {dashboard_html}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary_json", default="data/summary.json")
    parser.add_argument("--dashboard_html", default="dashboards/quarantine_digest.html")
    args = parser.parse_args()
    render(args.summary_json, args.dashboard_html)
