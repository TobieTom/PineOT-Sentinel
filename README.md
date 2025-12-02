# 🛡️ PineOT Sentinel

**PineOT Sentinel** is an automated smart contract security analysis tool designed to bridge the gap between expensive manual audits and rapid development cycles. 

Built on top of **Slither** (Static Analyzer), this Python-based wrapper automates the detection of critical vulnerabilities in Solidity contracts, focusing on "Rug Pull" vectors and high-severity logic errors.

## 🚀 Features

- **Automated Static Analysis:** Instantly scans `.sol` files using industry-standard detectors.
- **Rug Pull Detection:** Specifically flags `High` and `Medium` severity issues related to ownership privileges and unchecked external calls.
- **JSON & CLI Reporting:** Parses raw data into a human-readable "Pass/Fail" verdict for rapid deployment decisions.
- **CI/CD Integration Ready:** Lightweight architecture designed to run as a pre-commit hook or GitHub Action.

## 🛠️ Tech Stack

- **Python 3.10+**: Core logic and parsing engine.
- **Slither**: Underlying static analysis framework.
- **Solc-Select**: Automated Solidity compiler version management.

## ⚡ Installation

```bash
# 1. Install Dependencies
pip install slither-analyzer solc-select

# 2. Install Solidity Compiler
solc-select install 0.8.20
solc-select use 0.8.20
```
📖 Usage

Run the sentinel against any Solidity contract:
```
python sentinel.py contracts/MyToken.sol
```

Sample Output:
```
[*] Initializing PineOT Sentinel scan...

========================================
      PINEOT INTELLIGENCE REPORT      
========================================

[VERDICT]: ⚠ RISKY (2 Critical Issues Found)

--- VULNERABILITIES DETECTED ---
[CRITICAL] suicidal: emergencyWithdraw() allows anyone to destroy the contract.
[CRITICAL] arbitrary-send: owner can steal funds via updateSettings().
```
⚠️ Disclaimer

This tool is for educational and pre-audit purposes only. It does not replace a manual audit by a professional security firm.

Built by [TobieTom] for PineOT Intelligence.


---

### **3. The Updated Push Commands**
Since you added the `README.md`, you need to include it in your upload.

**Run these commands in your Windsurf terminal to push EVERYTHING:**

```powershell
# 1. Add both files
git add sentinel.py README.md

# 2. Save them
git commit -m "Added Sentinel Logic and Documentation"

# 3. Push to GitHub (If you already ran the 'remote add' command)
git push -u origin main
