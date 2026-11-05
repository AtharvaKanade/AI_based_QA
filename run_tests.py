"""
Convenience test runner script.
Executes database seeding, test generation, and full Pytest execution with HTML report.
"""

import os
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def run_command(cmd_list, description):
    print(f"\n==========================================")
    print(f"[*] {description}")
    print(f"    Command: {' '.join(cmd_list)}")
    print(f"==========================================")
    result = subprocess.run(cmd_list, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"[!] Warning: Step '{description}' exited with code {result.returncode}")
    return result.returncode


def main():
    python_exe = sys.executable

    # 1. Seed database
    run_command([python_exe, "data/seed_data.py"], "Seeding Test Database")

    # 2. Run AI test generator (ensures generated tests are refreshed)
    run_command([python_exe, "ai_engine/test_generator.py"], "Generating AI Test Cases")

    # 3. Run Pytest
    report_path = os.path.join(PROJECT_ROOT, "reports", "report.html")
    pytest_args = [
        python_exe, "-m", "pytest",
        "-v",
        f"--html={report_path}",
        "--self-contained-html"
    ]
    if len(sys.argv) > 1:
        pytest_args.extend(sys.argv[1:])

    code = run_command(pytest_args, "Executing Pytest Automation Suites")

    print(f"\n[+] Execution complete. HTML Report generated at:\n    {report_path}\n")
    sys.exit(code)


if __name__ == "__main__":
    main()

