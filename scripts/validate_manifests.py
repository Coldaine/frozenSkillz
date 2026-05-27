import json
import os
from pathlib import Path

def validate_manifest(filepath):
    print(f"Validating {filepath}...")
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        required_fields = ['name', 'version', 'description']
        missing = [f for f in required_fields if f not in data]
        if missing:
            print(f"  FAILED: Missing fields {missing}")
            return False

        print("  PASSED")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False

def main():
    manifests = []
    for root, dirs, files in os.walk('plugins'):
        for file in files:
            if file == 'plugin.json' and ('.codex-plugin' in root or '.cursor-plugin' in root):
                manifests.append(os.path.join(root, file))
            if file == 'gemini-extension.json':
                manifests.append(os.path.join(root, file))

    results = [validate_manifest(m) for m in manifests]

    if all(results) and len(results) >= 12:
        print(f"\nAll {len(results)} manifests validated successfully.")
    else:
        print(f"\nValidation failed. Found {len(results)} manifests.")
        exit(1)

if __name__ == "__main__":
    main()
