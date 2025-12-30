#!/usr/bin/env python3
"""
Generate a PDF documentation of the foundational prompt stack.

Reads layers.json and generates a Typst document that compiles to a
version-controlled PDF showing all layers and their exact prompts.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).parent.parent
LAYERS_JSON = REPO_ROOT / "layers.json"
EXPORTS_DIR = REPO_ROOT / "exports"
TYPST_TEMPLATE = EXPORTS_DIR / "foundational-stack.typ"


def load_layers() -> dict:
    """Load and parse layers.json."""
    with open(LAYERS_JSON) as f:
        return json.load(f)


def escape_typst(text: str) -> str:
    """Escape special Typst characters in text."""
    replacements = [
        ("\\", "\\\\"),
        ("#", "\\#"),
        ("$", "\\$"),
        ("@", "\\@"),
        ("<", "\\<"),
        (">", "\\>"),
        ("_", "\\_"),
        ("*", "\\*"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def generate_typst(data: dict, version: str = "2.0") -> str:
    """Generate Typst document content from layers data."""

    meta = data["meta"]
    foundational = data["foundational"]
    today = datetime.now().strftime("%B %d, %Y")

    # Build the complete foundational prompt by concatenating all elements
    complete_prompt_parts = []
    for layer in foundational["layers"]:
        for element in layer["elements"]:
            prompt_text = element.get("prompt_text", "")
            if prompt_text:
                complete_prompt_parts.append(prompt_text)

    complete_prompt = "\n\n".join(complete_prompt_parts)
    complete_prompt_escaped = escape_typst(complete_prompt)

    # Start building the Typst document
    typst = f'''// Text Transformation Prompt Stack - Foundational Layers Documentation
// Generated: {today}
// Version: {version}

#set document(
  title: "Text Transformation Prompt Stack",
  author: "Daniel Rosehill",
)

#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  footer: context [
    #set text(8pt)
    #align(center)[
      #counter(page).display("1 / 1", both: true)
      #v(0.3em)
      #text(fill: gray)[Author: Daniel Rosehill · public\\@danielrosehill.com · License: MIT]
    ]
  ],
)

#set text(font: "IBM Plex Sans", size: 11pt)
#set par(justify: true)

// Title page
#align(center + horizon)[
  #text(28pt, weight: "bold")[Text Transformation Prompt Stack]
  #v(1cm)
  #block(width: 85%)[
    #set text(12pt)
    #set par(justify: false, leading: 0.8em)
    A version-controlled prompt layering system intended for \
    concatenating effective system prompts for the generation \
    of edited transcription text from audio tokens provided to \
    audio multimodal and omnimodal AI models.
  ]
  #v(1.5cm)
  #text(12pt, fill: gray)[Version {version}]
  #v(0.5cm)
  #text(11pt)[Daniel Rosehill#footnote[#link("https://danielrosehill.com")[danielrosehill.com]]]
]

#pagebreak()

// Design section (formerly Introduction)
#text(16pt, weight: "bold")[Design]
#v(0.5em)

This document describes a layer-based approach for constructing system prompts for text transcription with audio multimodal models, leveraging prompt concatenation logic.

#v(0.5em)

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: none,
  [*Date:*], [{today}],
  [*Version:*], [{version}],
  [*Application:*], [Audio multimodal models for transcription use cases],
)

#v(1em)

=== Audio Multimodal Approach

This method leverages audio understanding capabilities of multimodal models while providing precisely targeted transcription formatting. This contrasts with traditional architectures that stack large language models with separate ASR (Automatic Speech Recognition) models.

The stack can be formulated for virtually any combination of format, style, and tone. A general-purpose cleanup prompt can also be generated, providing a regimented series of basic text edits that maximize intelligibility while minimizing destructive edits to the source material.

This document defines the version control system for programmatically concatenating the foundational text transformation stack.

#v(1em)

=== Two-Stack Architecture

#box(
  width: 100%,
  fill: rgb("#f5f5f5"),
  inset: 1em,
  radius: 4pt,
)[
  *Foundational Stack* (Layers 1-5)

  {escape_typst(meta["architecture"]["foundational"])}
]

#v(0.5em)

#box(
  width: 100%,
  fill: rgb("#e8f4e8"),
  inset: 1em,
  radius: 4pt,
)[
  *Stylistic Stack* (Layers 6-10)

  {escape_typst(meta["architecture"]["stylistic"])}
]

#v(1em)

This document details the *Foundational Stack*—the layers that are always applied to transform raw audio into polished text.

#pagebreak()

// Layer Flow Diagram
#text(16pt, weight: "bold")[Layer Flow]
#v(1em)

#align(center)[
  #set text(10pt)
'''

    # Generate flowchart
    layers_list = foundational["layers"]
    for idx, layer in enumerate(layers_list):
        order = layer["order"]
        name = escape_typst(layer["name"])
        num_elements = len(layer["elements"])

        typst += f'''
  #box(
    width: 70%,
    fill: rgb("#f0f4f8"),
    stroke: 1pt + rgb("#4a90d9"),
    inset: 1em,
    radius: 6pt,
  )[
    #align(center)[
      #text(weight: "bold")[Layer {order}: {name}]
      #v(0.3em)
      #text(fill: gray, size: 9pt)[{num_elements} element{"s" if num_elements != 1 else ""}]
    ]
  ]
'''
        # Add arrow between layers (except after last)
        if idx < len(layers_list) - 1:
            typst += '''
  #v(0.3em)
  #text(size: 16pt, fill: rgb("#666"))[↓]
  #v(0.3em)
'''

    typst += ''']

#pagebreak()

// Detailed Layer Documentation
#text(16pt, weight: "bold")[Layer Definitions]
#v(0.5em)

'''

    # Generate detailed documentation for each layer
    for idx, layer in enumerate(foundational["layers"]):
        order = layer["order"]
        folder = layer["folder"]
        name = escape_typst(layer["name"])
        description = escape_typst(layer["description"])
        elements = layer["elements"]

        # Add page break before each layer (except the first one which follows the section header)
        if idx > 0:
            typst += '''
#pagebreak()

'''

        typst += f'''
#text(14pt, weight: "bold")[{order}.0 {name}]
#v(0.3em)

#box(
  width: 100%,
  fill: rgb("#f0f4f8"),
  inset: 1em,
  radius: 4pt,
)[
  *Purpose:* {description}
]

#v(0.5em)

'''

        # Add each element with flat numbering
        for i, element in enumerate(elements, 1):
            elem_name = escape_typst(element["name"])
            prompt_text = escape_typst(element.get("prompt_text", "No prompt text available."))
            display_name = elem_name.replace("-", " ").title()

            typst += f'''
#text(12pt, weight: "medium")[{order}.{i} {display_name}]
#v(0.3em)

#box(
  width: 100%,
  stroke: 0.5pt + rgb("#ccc"),
  inset: 1em,
  radius: 4pt,
  fill: rgb("#fafafa"),
)[
  #set text(10pt)
  {prompt_text}
]

'''
            # Add horizontal separator between elements (except after last element in layer)
            if i < len(elements):
                typst += '''
#v(0.5em)
#line(length: 100%, stroke: 0.5pt + rgb("#ddd"))
#v(0.5em)

'''
            else:
                typst += '''
#v(1em)

'''

    # Add complete concatenated prompt section with proper page breaking
    typst += f'''
#pagebreak()

#text(16pt, weight: "bold")[Complete Foundational Prompt]
#v(0.5em)

The following is the complete foundational system prompt, formed by concatenating all layer elements in order. This represents the full instruction set provided to the audio multimodal model.

#v(1em)

#block(
  width: 100%,
  stroke: (left: 3pt + rgb("#4a90d9")),
  inset: (left: 1.5em, top: 1em, bottom: 1em, right: 1em),
  fill: rgb("#f8f8f8"),
  breakable: true,
)[
  #set text(9.5pt)
  #set par(leading: 0.9em)
  {complete_prompt_escaped}
]
'''

    return typst


def compile_pdf(typst_file: Path) -> Path:
    """Compile Typst file to PDF."""
    pdf_file = typst_file.with_suffix(".pdf")

    result = subprocess.run(
        ["typst", "compile", str(typst_file), str(pdf_file)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Error compiling Typst: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    return pdf_file


def main():
    """Main entry point."""
    # Ensure exports directory exists
    EXPORTS_DIR.mkdir(exist_ok=True)

    # Load layers data
    print(f"Loading layers from {LAYERS_JSON}...")
    data = load_layers()

    # Get version from meta
    version = data["meta"]["version"]

    # Generate Typst content
    print(f"Generating Typst document (version {version})...")
    typst_content = generate_typst(data, version)

    # Write Typst file
    TYPST_TEMPLATE.write_text(typst_content)
    print(f"Wrote Typst file: {TYPST_TEMPLATE}")

    # Compile to PDF
    print("Compiling to PDF...")
    pdf_file = compile_pdf(TYPST_TEMPLATE)
    print(f"Generated PDF: {pdf_file}")

    # Also create a versioned copy
    versioned_pdf = EXPORTS_DIR / f"foundational-stack-v{version.replace('.', '-')}.pdf"
    import shutil
    shutil.copy(pdf_file, versioned_pdf)
    print(f"Created versioned copy: {versioned_pdf}")


if __name__ == "__main__":
    main()
