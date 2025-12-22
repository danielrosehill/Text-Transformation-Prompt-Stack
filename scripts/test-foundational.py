#!/usr/bin/env python3
"""
Foundational Prompt Testing Script

Tests the current state of the foundational prompt against an audio file.
Drop an audio file (e.g., note.mp3) into the planning/ directory and run this script.

Usage:
    python test-foundational.py [audio_file]

Examples:
    python test-foundational.py                    # Uses planning/note.mp3 by default
    python test-foundational.py my-recording.mp3   # Uses specified file
    python test-foundational.py planning/test.mp3  # Full path
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Suppress deprecation warning
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai


def load_api_key():
    """Load Gemini API key from .env file."""
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print("Error: .env file not found", file=sys.stderr)
        sys.exit(1)

    with open(env_path) as f:
        for line in f:
            if line.startswith('GEMINI_API_KEY='):
                return line.strip().split('=', 1)[1]

    print("Error: GEMINI_API_KEY not found in .env", file=sys.stderr)
    sys.exit(1)


def get_foundational_prompt():
    """Generate the current foundational prompt."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    result = subprocess.run(
        ['python3', str(script_dir / 'generate-foundational.py'), '--stdout'],
        capture_output=True, text=True, cwd=repo_root
    )
    if result.returncode != 0:
        print(f"Error generating foundational prompt: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def compress_audio(input_path: Path, max_size_mb: float = 19.0) -> Path:
    """Compress audio if needed to stay under Gemini's size limit."""
    file_size_mb = input_path.stat().st_size / (1024 * 1024)

    if file_size_mb <= max_size_mb:
        return input_path

    print(f"Compressing audio ({file_size_mb:.1f}MB -> target <{max_size_mb}MB)...")

    # Create temp file for compressed audio
    compressed_path = input_path.parent / f"{input_path.stem}_compressed.mp3"

    result = subprocess.run([
        'ffmpeg', '-i', str(input_path),
        '-b:a', '64k', '-ar', '22050',
        str(compressed_path), '-y'
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error compressing audio: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    new_size = compressed_path.stat().st_size / (1024 * 1024)
    print(f"Compressed to {new_size:.1f}MB")

    return compressed_path


def transcribe(audio_path: Path, prompt: str) -> str:
    """Send audio to Gemini with the foundational prompt."""
    api_key = load_api_key()
    genai.configure(api_key=api_key)

    print(f"Uploading: {audio_path.name}")
    audio_file = genai.upload_file(str(audio_path))
    print("Upload complete")

    model = genai.GenerativeModel('gemini-2.5-flash')
    print("Transcribing with foundational prompt...")

    response = model.generate_content([prompt, audio_file])
    return response.text


def main():
    repo_root = Path(__file__).parent.parent

    # Determine audio file path
    if len(sys.argv) > 1:
        audio_input = sys.argv[1]
        audio_path = Path(audio_input)
        if not audio_path.is_absolute():
            # Check if it exists relative to repo root
            if (repo_root / audio_input).exists():
                audio_path = repo_root / audio_input
            elif (repo_root / "planning" / audio_input).exists():
                audio_path = repo_root / "planning" / audio_input
    else:
        # Default to planning/note.mp3
        audio_path = repo_root / "planning" / "note.mp3"

    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        print(f"\nUsage: python {Path(__file__).name} [audio_file]", file=sys.stderr)
        print(f"Default: planning/note.mp3", file=sys.stderr)
        sys.exit(1)

    print(f"Testing foundational prompt with: {audio_path}")
    print("-" * 50)

    # Get the current foundational prompt
    prompt = get_foundational_prompt()

    # Compress if needed
    working_audio = compress_audio(audio_path)
    compressed = working_audio != audio_path

    try:
        # Transcribe
        transcript = transcribe(working_audio, prompt)

        # Save output
        output_path = audio_path.parent / f"{audio_path.stem}_transcript.md"
        with open(output_path, 'w') as f:
            f.write(transcript)

        print("-" * 50)
        print(f"Transcript saved to: {output_path}")
        print(f"\nFirst 500 characters:")
        print(transcript[:500])

    finally:
        # Clean up compressed file if we created one
        if compressed and working_audio.exists():
            working_audio.unlink()
            print(f"\nCleaned up temporary compressed file")


if __name__ == "__main__":
    main()
