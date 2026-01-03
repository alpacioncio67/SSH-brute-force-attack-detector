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

