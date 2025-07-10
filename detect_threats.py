import re
from datetime import datetime

# Define MITRE-mapped threat patterns
SIGNATURES = {
    "SQL Injection (T1505.003)": [
        r"(?i)' OR '1'='1",
        r"(?i)UNION SELECT",
        r"(?i)SLEEP\(\d+\)",
        r"(?i)DROP TABLE",
        r"(\\\\|\\\\\\\\).*attacker\.com",
        r"(?i)xp_dirtree",
        r"(?i)LOAD_FILE"
    ],
    "JWT Forgery (T1606.001)": [
        r"eyJhbGciOiJub25l"
    ],
    "Prompt Injection (T1556.003)": [
        r"(?i)ignore previous instructions",
        r"(?i)list all users"
    ]
}

# Scan one line of log data
def scan_log(log_line):
    for threat, patterns in SIGNATURES.items():
        for pattern in patterns:
            if re.search(pattern, log_line):
                print(f"\n[ALERT] {threat}")
                print(f"Time: {datetime.now()}")
                print(f"Matched Pattern: {pattern}")
                print(f"Log: {log_line.strip()}")

                # Write alert to file (for Splunk or logging)
                with open("output/alerts.log", "a") as f:
                    f.write(f"[{datetime.now()}] ALERT | {threat} | {pattern} | {log_line.strip()}\n")

# Read and scan the test log file
def run():
    with open("logs/test_log.txt", "r") as file:
        for line in file:
            scan_log(line)

# Entry point
if __name__ == "__main__":
    run()
