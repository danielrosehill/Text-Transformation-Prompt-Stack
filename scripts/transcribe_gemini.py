#!/usr/bin/env python3
"""
Audio transcription using Google Gemini API.
Transcribes audio files and cleans up the transcript.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

CLEANUP_PROMPT = """You are a speech-to-text transcript cleanup assistant.

Your task is to take this audio recording and produce a clean, readable transcript.

Instructions:
1. Transcribe the audio accurately
2. Remove filler words (um, uh, like, you know) unless they add meaning
3. Fix obvious transcription errors
4. Add proper punctuation and paragraph breaks
5. Maintain the speaker's intended meaning
6. Format as clean prose, not verbatim transcription

Please transcribe and clean up the following audio:"""


def transcribe_audio(audio_path: Path, output_path: Path = None):
    """Transcribe audio file using Gemini API."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment", file=sys.stderr)
        sys.exit(1)

    genai.configure(api_key=api_key)

    # Upload the audio file
    print(f"Uploading audio file: {audio_path}")
    audio_file = genai.upload_file(str(audio_path))
    print(f"Upload complete: {audio_file.uri}")

    # Use Gemini 2.0 Flash for audio processing
    model = genai.GenerativeModel("gemini-2.0-flash-exp")

    print("Transcribing and cleaning up...")
    response = model.generate_content([CLEANUP_PROMPT, audio_file])

    transcript = response.text

    # Determine output path
    if output_path is None:
        output_path = audio_path.parent / f"{audio_path.stem}_transcript.md"

    # Save transcript
    with open(output_path, 'w') as f:
        f.write(f"# Transcript: {audio_path.name}\n\n")
        f.write(transcript)

    print(f"Transcript saved to: {output_path}")
    return transcript


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Transcribe audio using Gemini API")
    parser.add_argument("audio_file", help="Path to audio file")
    parser.add_argument("-o", "--output", help="Output file path (default: same dir as input)")

    args = parser.parse_args()

    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else None

    transcribe_audio(audio_path, output_path)


if __name__ == "__main__":
    main()
