import subprocess
import json
import os
import sys

# PINEOT SENTINEL - Automated Smart Contract Security Scanner
# Usage: python sentinel.py <contract_file.sol>

def run_security_scan(contract_path):
    print(f"[*] Initializing PineOT Sentinel scan for: {contract_path}...")
    
    # 1. Run Slither (The Engine) and output as JSON
    try:
        # We use subprocess to call the slither command line tool
        cmd = f"slither {contract_path} --json results.json"
        # Suppress the massive wall of text in the terminal
        subprocess.run(cmd, shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[!] Error running Slither: {e}")
        return

    # 2. Parse the Results
    if not os.path.exists("results.json"):
        print("[!] Scan Failed. No results generated. (Check if the .sol file compiles)")
        return

    with open("results.json", "r") as f:
        data = json.load(f)

    # 3. Filter for "Rug Pull" Signals (High/Medium Severity)
    detectors = data.get('results', {}).get('detectors', [])
    
    critical_issues = []
    medium_issues = []

    print("\n" + "="*40)
    print("      PINEOT INTELLIGENCE REPORT      ")
    print("="*40)

    found_issues = False
    
    for issue in detectors:
        impact = issue.get('impact', 'Low')
        check = issue.get('check', 'Unknown')
        description = issue.get('description', 'No description')
        
        if impact == 'High':
            critical_issues.append(f"[CRITICAL] {check}: {description}")
            found_issues = True
        elif impact == 'Medium':
            medium_issues.append(f"[MEDIUM] {check}: {description}")
            found_issues = True

    # 4. Generate the Verdict
    if not found_issues:
        print("\n[VERDICT]: ✅ SAFE (PASSED)")
        print("Status: Eligible for PineOT Verified Badge")
    else:
        print(f"\n[VERDICT]: ⚠ RISKY ({len(critical_issues)} Critical Issues Found)")
        print("Status: FAILED")
        
        print("\n--- VULNERABILITIES DETECTED ---")
        for err in critical_issues:
            print(err)

    # Cleanup
    if os.path.exists("results.json"):
        os.remove("results.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sentinel.py <contract.sol>")
    else:
        run_security_scan(sys.argv[1])