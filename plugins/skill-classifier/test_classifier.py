#!/usr/bin/env python3
"""Manual test harness for skill_classifier.py.

Run: python test_classifier.py
"""

import json
import subprocess
import sys
import time
from pathlib import Path

SCRIPT = Path(__file__).parent / "scripts" / "skill_classifier.py"
MOCK_INPUT = Path(__file__).parent / "mock_input.json"
MOCK_TRANSCRIPT = Path(__file__).parent / "mock_transcript.jsonl"


def run_classifier(input_data: dict, label: str) -> dict | None:
    """Run the classifier with given input and return parsed output."""
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    print(f"{'='*60}")
    print(f"  Prompt: {input_data.get('prompt', '')[:80]}...")

    start = time.time()
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        timeout=30,
    )
    elapsed = time.time() - start

    print(f"  Latency: {elapsed:.2f}s")
    print(f"  Return code: {result.returncode}")

    if result.stderr.strip():
        print(f"  Stderr: {result.stderr.strip()}")

    stdout = result.stdout.strip()
    if not stdout:
        print(f"  Result: SILENT PASSTHROUGH (no output)")
        return None

    try:
        output = json.loads(stdout)
        print(f"  Result: {json.dumps(output, indent=2)}")
        return output
    except json.JSONDecodeError:
        print(f"  Result: INVALID JSON: {stdout}")
        return None


def test_debugging_scenario():
    """Should suggest systematic-debugging."""
    return run_classifier({
        "prompt": "I'm getting an error when I run the tests. The login function returns 401 but I don't know why.",
        "transcript_path": str(MOCK_TRANSCRIPT),
    }, "Debugging scenario → should suggest systematic-debugging")


def test_silent_passthrough():
    """Trivial message should produce no output."""
    return run_classifier({
        "prompt": "hello",
        "transcript_path": "",
    }, "Trivial message → should be silent")


def test_creative_work():
    """Should suggest brainstorming for new feature work."""
    return run_classifier({
        "prompt": "I want to add a new notification system to the app. Users should get real-time alerts when their builds complete.",
        "transcript_path": "",
    }, "New feature → should suggest brainstorming")


def test_plan_request():
    """Should suggest writing-plans for planning work."""
    return run_classifier({
        "prompt": "I have the requirements for the new payment integration. Let's plan out the implementation before we start coding.",
        "transcript_path": "",
    }, "Planning request → should suggest writing-plans")


def test_empty_prompt():
    """Empty prompt should silently pass through."""
    return run_classifier({
        "prompt": "",
        "transcript_path": "",
    }, "Empty prompt → should be silent")


def test_latency_batch():
    """Run 5 iterations and report latency stats."""
    print(f"\n{'='*60}")
    print("TEST: Latency batch (5 runs)")
    print(f"{'='*60}")

    times = []
    for i in range(5):
        start = time.time()
        subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps({
                "prompt": "Fix the bug in the payment processing module",
                "transcript_path": "",
            }),
            capture_output=True,
            text=True,
            timeout=30,
        )
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"  Run {i+1}: {elapsed:.2f}s")

    times.sort()
    print(f"\n  Min: {times[0]:.2f}s")
    print(f"  Median: {times[len(times)//2]:.2f}s")
    print(f"  Max: {times[-1]:.2f}s")
    print(f"  p95: {times[int(len(times)*0.95)]:.2f}s")


def main():
    print("frozenSkillz — Test Harness")
    print("Using mock transcript:", MOCK_TRANSCRIPT)

    # Verify skills can be loaded
    from skill_classifier import get_skills
    skills = get_skills()
    print(f"\nLoaded {len(skills)} skills:")
    for s in skills:
        print(f"  - {s['name']}: {s['description'][:60]}...")

    # Run tests
    test_silent_passthrough()
    test_empty_prompt()
    test_debugging_scenario()
    test_creative_work()
    test_plan_request()

    # Latency
    run_latency = input("\nRun latency batch test? (y/N): ").strip().lower()
    if run_latency == "y":
        test_latency_batch()

    print("\n" + "="*60)
    print("Done.")


if __name__ == "__main__":
    main()
