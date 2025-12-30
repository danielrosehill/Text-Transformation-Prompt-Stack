#!/bin/bash
# Wrapper script for generate-foundational.py
# Generates the concatenated foundational cleanup prompt

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/scripts/generate-foundational.py" "$@"
