# SSH Brute Force Detection using Log Analysis (Kali Linux Version)

## 📌 Overview
This project detects SSH brute force attacks by analyzing authentication logs generated during real attack simulations performed with Kali Linux tools.

The goal is to simulate a realistic Blue Team scenario where an analyst receives system logs and must identify suspicious activity using Python-based data analysis.

This is the **Version 2** of the project, improving upon a previous version that used simulated logs.

---

## 🎯 Objectives
- Generate real SSH authentication logs using Kali Linux
- Detect brute force attacks based on failed login attempts
- Allow analysis of both real and external log files
- Validate detection logic through controlled attack testing

---

## 🛠️ Technologies Used
- Python 3
- Kali Linux
- OpenSSH
- Hydra (attack simulation)
- pandas / collections.Counter
- Regular Expressions (regex)

---

## 🧪 Attack Simulation (Kali Linux)

To generate realistic logs, SSH brute force attacks were simulated using Kali Linux.

### Example attack command:
```bash
hydra -l root -P rockyou.txt ssh://<TARGET_IP>
```

The system logs the authentication attempts in:
/var/log/auth.log
⚠️ All attacks were performed in a controlled lab environment for educational purposes only.

⚙️ How the Analyzer Works

1. Reads SSH authentication logs
2. Filters failed login attempts
3. Extracts source IP addresses using regex
4. Counts failed attempts per IP
5. Flags IPs exceeding a defined limit
6. Outputs results to a CSV file

▶️ How to Run the Project

1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Place your log file

Copy your SSH authentication log into:
data/auth.log
You can use:
Logs generated via Kali Linux
Logs from another Linux system
Sample logs for testing

3️⃣ Run the analyzer

python src/analyzer.py
4️⃣ View results

Suspicious IPs will be saved in:
results/suspicious_ips.csv
