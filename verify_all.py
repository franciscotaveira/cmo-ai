import os
import sys
import subprocess


def run_check(name, command):
    print(f"🚀 Running {name}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {name} passed.")
            return True
        else:
            print(f"❌ {name} failed.")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"💥 Error running {name}: {e}")
        return False


def main():
    print("🛡️ SOVEREIGN HIVE HEALTH-CHECK (v14.0)")
    print("-" * 40)

    checks = [
        (
            "LUNA Frontend Directive Audit",
            "grep -q '\"use client\";' '/Users/franciscotaveira.ads/LUNA OS/frontend/app/page.tsx'",
        ),
        (
            "LUNA Backend Root Health",
            "curl -s http://localhost:8000/api | grep -q 'online'",
        ),
        (
            "LUNA Dashboard Analytics Data",
            'curl -s http://localhost:8000/api/analytics/dashboard | grep -q \'"conversations":{"total":[1-9]\'',
        ),
        (
            "Memory Integrity (CODEBASE)",
            "ls '/Users/franciscotaveira.ads/LUNA OS/CODEBASE.md'",
        ),
    ]

    results = []
    for name, command in checks:
        results.append(run_check(name, command))

    if all(results):
        print("\n🏆 HIVE is in PEAK PERFORMANCE - READY FOR MISSION.")
    else:
        print("\n⚠️ HIVE needs HARDENING. Some components failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
