#!/usr/bin/env python3
"""
Text Transformation Prompt Stack Concatenator

This script reads a stack configuration file and concatenates the specified
layer files into a single prompt for use with LLMs.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional
import yaml


class PromptStackConcatenator:
    """Concatenates prompt layers into a complete transformation prompt."""

    def __init__(self, repo_root: Optional[Path] = None):
        """
        Initialize the concatenator.

        Args:
            repo_root: Path to repository root. If None, uses script directory.
        """
        if repo_root is None:
            self.repo_root = Path(__file__).parent.parent
        else:
            self.repo_root = Path(repo_root)

    def load_stack_config(self, stack_path: Path) -> Dict:
        """
        Load a stack configuration file.

        Args:
            stack_path: Path to stack YAML file

        Returns:
            Dictionary containing stack configuration
        """
        try:
            with open(stack_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Error: Stack file not found: {stack_path}", file=sys.stderr)
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}", file=sys.stderr)
            sys.exit(1)

    def load_layer(self, layer_path: Path) -> str:
        """
        Load a single layer file.

        Args:
            layer_path: Path to layer markdown file

        Returns:
            Content of the layer file
        """
        full_path = self.repo_root / layer_path
        try:
            with open(full_path, 'r') as f:
                content = f.read().strip()
            return content
        except FileNotFoundError:
            print(f"Error: Layer file not found: {full_path}", file=sys.stderr)
            sys.exit(1)

    def concatenate_stack(self, stack_config: Dict, separator: str = "\n\n") -> str:
        """
        Concatenate all layers in a stack.

        Args:
            stack_config: Stack configuration dictionary
            separator: String to use between layers

        Returns:
            Concatenated prompt string
        """
        layers = stack_config.get('layers', [])
        if not layers:
            print("Error: No layers defined in stack configuration", file=sys.stderr)
            sys.exit(1)

        layer_contents = []
        for layer_path in layers:
            content = self.load_layer(Path(layer_path))
            layer_contents.append(content)

        return separator.join(layer_contents)

    def concatenate_from_file(self, stack_file: str, separator: str = "\n\n") -> str:
        """
        Load and concatenate a stack from a file path.

        Args:
            stack_file: Path to stack configuration file
            separator: String to use between layers

        Returns:
            Concatenated prompt string
        """
        stack_path = Path(stack_file)
        if not stack_path.is_absolute():
            # Try in stacks directory first
            stack_path = self.repo_root / "stacks" / stack_file
            if not stack_path.exists():
                # Try as relative path from repo root
                stack_path = self.repo_root / stack_file

        config = self.load_stack_config(stack_path)
        return self.concatenate_stack(config, separator)

    def list_available_stacks(self) -> List[str]:
        """
        List all available stack configurations.

        Returns:
            List of stack file names
        """
        stacks_dir = self.repo_root / "stacks"
        if not stacks_dir.exists():
            return []

        return sorted([f.name for f in stacks_dir.glob("*.yaml")])


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Concatenate text transformation prompt stack layers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Concatenate a stack and print to stdout
  %(prog)s business-email.yaml

  # Save to a file
  %(prog)s business-email.yaml -o prompt.txt

  # Use custom separator
  %(prog)s business-email.yaml -s " "

  # List available stacks
  %(prog)s --list
        """
    )

    parser.add_argument(
        'stack',
        nargs='?',
        help='Stack configuration file (from stacks/ directory or full path)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)',
        type=str
    )

    parser.add_argument(
        '-s', '--separator',
        help='Separator between layers (default: double newline)',
        default='\n\n',
        type=str
    )

    parser.add_argument(
        '-l', '--list',
        help='List available stack configurations',
        action='store_true'
    )

    parser.add_argument(
        '-r', '--repo-root',
        help='Repository root directory (default: script directory)',
        type=str
    )

    args = parser.parse_args()

    # Initialize concatenator
    repo_root = Path(args.repo_root) if args.repo_root else None
    concatenator = PromptStackConcatenator(repo_root)

    # List stacks if requested
    if args.list:
        stacks = concatenator.list_available_stacks()
        if stacks:
            print("Available stacks:")
            for stack in stacks:
                print(f"  - {stack}")
        else:
            print("No stacks found in stacks/ directory")
        return

    # Require stack argument if not listing
    if not args.stack:
        parser.error("stack argument is required (unless using --list)")

    # Concatenate the stack
    try:
        prompt = concatenator.concatenate_from_file(args.stack, args.separator)

        # Output to file or stdout
        if args.output:
            with open(args.output, 'w') as f:
                f.write(prompt)
            print(f"Prompt written to: {args.output}", file=sys.stderr)
        else:
            print(prompt)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
