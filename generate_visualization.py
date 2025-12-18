#!/usr/bin/env python3
"""
Generate a visual representation of the Text Transformation Prompt Stack
using Replicate's image generation models.
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import replicate
except ImportError:
    print("Error: replicate package not installed. Install with: pip install replicate")
    sys.exit(1)


def generate_stack_visualization(output_path: str = "stack_visualization.png",
                                 model: str = "black-forest-labs/flux-1.1-pro"):
    """
    Generate a visual representation of the prompt stack architecture.

    Args:
        output_path: Where to save the generated image
        model: Replicate model to use for generation
    """

    # Check for API token
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("Error: REPLICATE_API_TOKEN environment variable not set")
        print("Get your token from: https://replicate.com/account/api-tokens")
        sys.exit(1)

    # Detailed prompt for the diagram
    prompt = """Create a clean, professional technical diagram illustration showing a text transformation pipeline. The diagram should flow from left to right:

1. On the LEFT: A stylized microphone icon representing voice input, with small sound waves around it
2. A rightward arrow
3. In the MIDDLE: A vertical stack of 7 colorful rectangular blocks/layers stacked on top of each other (like building blocks or Jenga pieces), each a different pastel color. Label them from bottom to top:
   - "Context Layer" (blue)
   - "Baseline Layer" (green)
   - "Format Layer" (yellow)
   - "Tone Layer" (orange)
   - "Emotional Layer" (purple)
   - "Style Layer" (pink)
   - "Readability Layer" (teal)
4. A rightward arrow
5. On the RIGHT: A stylized document/page icon with text lines, representing the formatted output

Style: Clean, modern, minimalist technical diagram with flat design, pastel colors, white background, professional appearance suitable for technical documentation. Clear labels, balanced composition, icon-based illustration style."""

    print(f"Generating visualization using {model}...")
    print("This may take a minute...")

    try:
        # Run the model
        output = replicate.run(
            model,
            input={
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "output_format": "png",
                "output_quality": 90,
            }
        )

        # Download the image
        import urllib.request

        # output is usually a URL string or list of URLs
        if isinstance(output, list):
            image_url = output[0]
        else:
            image_url = output

        print(f"Downloading image from: {image_url}")
        urllib.request.urlretrieve(image_url, output_path)
        print(f"✓ Visualization saved to: {output_path}")

        return output_path

    except Exception as e:
        print(f"Error generating visualization: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a visual representation of the Text Transformation Prompt Stack"
    )

    parser.add_argument(
        '-o', '--output',
        default='stack_visualization.png',
        help='Output file path (default: stack_visualization.png)'
    )

    parser.add_argument(
        '-m', '--model',
        default='black-forest-labs/flux-1.1-pro',
        help='Replicate model to use (default: black-forest-labs/flux-1.1-pro)'
    )

    args = parser.parse_args()

    generate_stack_visualization(args.output, args.model)


if __name__ == '__main__':
    main()
