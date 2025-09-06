# Enterprise Email Security Implementation

A practical, portfolio-ready project that showcases how to design and operate an email security pipeline (inspired by Libraesva-style controls) with a live, auto-published quarantine digest dashboard.

Live dashboard: https://arbagga99.github.io/Enterprise-Email-Security-Implementation/quarantine_digest.html

Repository: https://github.com/arbagga99/Enterprise-Email-Security-Implementation

How the pipeline works ?
The pipeline generates synthetic quarantine events, then normalizes and risk-scores them. It aggregates the results into KPIs (spam, phishing, malware, false positives) and extracts a list of high-risk alerts. A small publisher script copies these JSON outputs into docs/data/ so the live dashboard can read them. A GitHub Actions workflow runs the pipeline on demand (and/or on a schedule) and commits updated JSON files back to the repo. GitHub Pages serves docs/quarantine_digest.html, which loads the published JSON and renders the KPIs, top rules/senders, and the alerts table.
