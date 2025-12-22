#!/usr/bin/env python3
"""
Foundational Prompt Generator

Generates the concatenated foundational cleanup prompt from layers.json.
Reads content from markdown files referenced in the config.
Outputs are version-controlled with date-stamped filenames (ddmmyy format).
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def load_layers_config(repo_root: Path) -> dict:
    """Load the layers.json configuration file."""
    config_path = repo_root / "layers.json"
    with open(config_path, 'r') as f:
        return json.load(f)


def read_markdown_file(repo_root: Path, file_path: str) -> str:
    """Read content from a markdown file."""
    full_path = repo_root / file_path
    if full_path.exists():
        return full_path.read_text().strip()
    return ""


def extract_foundational_instructions(config: dict, repo_root: Path) -> list[tuple[str, str, str, bool]]:
    """
    Extract all foundational layer instructions in optimized order.

    Order: Context -> Personalization -> Exclusions -> Corrections -> Inference

    Returns:
        List of tuples: (layer_name, element_name, instruction, no_header)
    """
    instructions = []

    foundational = config.get("foundational", {})
    layers = foundational.get("layers", [])

    # Custom order: context first, then personalization, then the rest
    # This puts user identity info near the start for better prompt flow
    order_map = {
        "01-context": 1,
        "05-personalization": 2,  # Move personalization early
        "02-exclusions": 3,
        "03-corrections": 4,
        "04-inference": 5,
    }

    sorted_layers = sorted(
        layers,
        key=lambda x: order_map.get(x.get("folder", ""), x.get("order", 99))
    )

    for layer in sorted_layers:
        layer_name = layer.get("name", "Unknown")
        elements = layer.get("elements", [])

        for element in elements:
            element_name = element.get("name", "unknown")
            file_path = element.get("file_path", "")
            no_header = element.get("no_header", False)

            # Read from file if file_path exists, otherwise fall back to instruction
            if file_path:
                instruction = read_markdown_file(repo_root, file_path)
            else:
                instruction = element.get("instruction", "")

            if instruction:
                instructions.append((layer_name, element_name, instruction, no_header))

    return instructions


def format_element_name(element_name: str) -> str:
    """Convert element-name to Title Case Header."""
    return element_name.replace("-", " ").title()


def generate_foundational_prompt(instructions: list[tuple[str, str, str, bool]],
                                  include_headers: bool = True) -> str:
    """
    Generate the concatenated foundational prompt.

    Args:
        instructions: List of (layer_name, element_name, instruction, no_header) tuples
        include_headers: If True, include section headers for each element (default: True)

    Returns:
        Concatenated prompt string
    """
    if include_headers:
        sections = []

        for layer_name, element_name, instruction, no_header in instructions:
            if no_header:
                # No header for this element (e.g., task-definition)
                sections.append(instruction)
            else:
                header = format_element_name(element_name)
                sections.append(f"## {header}\n\n{instruction}")

        return "\n\n".join(sections)
    else:
        # Simple concatenation without headers
        return "\n\n".join(instruction for _, _, instruction, _ in instructions)


def get_output_filenames(date: datetime = None) -> tuple[str, str]:
    """Generate output filenames with ddmmyy date format.

    Returns:
        Tuple of (auto_generated_filename, manual_filename)
    """
    if date is None:
        date = datetime.now()
    date_str = date.strftime('%d%m%y')
    return (
        f"foundational_auto_generated_{date_str}.md",
        f"foundational_{date_str}.md"
    )


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate concatenated foundational cleanup prompt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with today's date (includes headers by default)
  %(prog)s

  # Generate with specific date
  %(prog)s --date 221225

  # Generate without section headers
  %(prog)s --no-headers

  # Output to stdout instead of file
  %(prog)s --stdout
        """
    )

    parser.add_argument(
        '--date',
        help='Date in ddmmyy format (default: today)',
        type=str
    )

    parser.add_argument(
        '--no-headers',
        help='Omit section headers (headers included by default)',
        action='store_true'
    )

    parser.add_argument(
        '--stdout',
        help='Output to stdout instead of file',
        action='store_true'
    )

    parser.add_argument(
        '-r', '--repo-root',
        help='Repository root directory (default: script directory)',
        type=str
    )

    args = parser.parse_args()

    # Determine repo root
    if args.repo_root:
        repo_root = Path(args.repo_root)
    else:
        repo_root = Path(__file__).parent

    # Parse date if provided
    if args.date:
        try:
            date = datetime.strptime(args.date, '%d%m%y')
        except ValueError:
            print(f"Error: Invalid date format '{args.date}'. Use ddmmyy.", file=sys.stderr)
            sys.exit(1)
    else:
        date = datetime.now()

    # Load configuration
    try:
        config = load_layers_config(repo_root)
    except FileNotFoundError:
        print(f"Error: layers.json not found in {repo_root}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing layers.json: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract and concatenate
    instructions = extract_foundational_instructions(config, repo_root)

    if not instructions:
        print("Error: No foundational instructions found", file=sys.stderr)
        sys.exit(1)

    prompt = generate_foundational_prompt(instructions, include_headers=not args.no_headers)

    # Output
    if args.stdout:
        print(prompt)
    else:
        output_dir = repo_root / "generated" / "foundational"
        output_dir.mkdir(parents=True, exist_ok=True)

        auto_filename, manual_filename = get_output_filenames(date)

        # Write auto-generated version
        auto_path = output_dir / auto_filename
        with open(auto_path, 'w') as f:
            f.write(prompt)

        # Write manual editing version (same content, for user to customize)
        manual_path = output_dir / manual_filename
        with open(manual_path, 'w') as f:
            f.write(prompt)

        print(f"Generated: {auto_path}")
        print(f"For editing: {manual_path}")
        print(f"Layers included: {len(instructions)}")


if __name__ == '__main__':
    main()
