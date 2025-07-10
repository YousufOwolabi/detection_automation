# 🛡️ MITRE-Mapped Threat Detection Script (Python)

This lightweight detection tool scans raw logs for suspicious activity and maps findings to MITRE ATT&CK techniques. It's designed for security analysts, SOC engineers, or home lab users who want to simulate and detect:

- 🧱 SQL Injection (T1505.003)
- 🔐 JWT Forgery (T1606.001)
- 🤖 Prompt Injection (T1556.003)

It writes all detections to an output file, which can be monitored by Splunk or Wazuh for further correlation, alerting, and dashboarding.

---

## 📁 Project Structure

detection_automation/
├── detect_threats.py           # MITRE-mapped detection script
├── logs/
│   └── test_log.txt            # Sample raw logs to simulate detection
├── output/
│   └── alerts.log              # Detection alerts (monitored by Splunk/Wazuh)

---

## 🚀 How to Use

### 1. Clone the repo and enter the directory

```bash
git clone https://github.com/YousufOwolabi/detection_automation.git
cd detection_automation
2. Populate the test log

Add logs to logs/test_log.txt. You can use simulated API calls, endpoint logs, or HTTP request strings.

3. Run the detection script
    python3 detect_threats.py
This scans the log file, matches known threat patterns, and logs any alerts to output/alerts.log.

⸻

**📡 Splunk Integration**

To forward alerts to Splunk:

1. Configure the Universal Forwarder
# /opt/splunkforwarder/etc/system/local/inputs.conf

[monitor:///full/path/to/output/alerts.log]
sourcetype = threat_detection
index = main

Replace the full path with the actual path to alerts.log on your system.

⸻

2. Restart the forwarder
sudo /opt/splunkforwarder/bin/splunk restart

⸻

3. Search in Splunk
index=main sourcetype=threat_detection
| rex "\|\s(?<threat_type>.+?)\s\|\s(?<pattern>.+?)\s\|\s(?<log_entry>.+)$"
| table _time, threat_type, log_entry

This will extract fields from the alerts for dashboarding and investigation.

⸻

**🛡️ Wazuh Integration**

To integrate with Wazuh:

1. Modify the script to also write alerts in JSON

Example JSON:
{
  "timestamp": "2025-07-10T20:00:00Z",
  "rule": "SQL Injection (T1505.003)",
  "pattern": "(?i)UNION SELECT",
  "log_entry": "GET /search?q=UNION SELECT name, email FROM users"
}

Write this file to:
/var/ossec/logs/active-responses/my_script_alerts.json

2. Configure Wazuh to monitor it

In /var/ossec/etc/ossec.conf, add:
xml:
<localfile>
  <log_format>json</log_format>
  <location>/var/ossec/logs/active-responses/my_script_alerts.json</location>
</localfile>

Then restart Wazuh:
sudo systemctl restart wazuh-agent

**🎯 MITRE ATT&CK Mapping**

**Technique**                **Description**
T1505.003                     SQL Injection
T1606.001                     JWT ‘none’ algorithm forgery
T1556.003                     Input validation abuse (Prompt Injection)

⸻

**🔧 Future Improvements**
 • Add severity scoring per detection
 • Export alerts in JSON format for better compatibility
 • Real-time log tailing (like tail -f)
 • Dockerize the lab for fast deployment

⸻

**📄 License**

MIT License © 2025 [Yousuf Owolabi]

⸻

**🙌 Contributions**

PRs welcome! Feel free to contribute new detection patterns, MITRE mappings, or integrations.
