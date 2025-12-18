# Text Transformation Prompt Stack

A systematic, layered approach to transforming raw speech-to-text output into polished, formatted text using composable prompt instructions.

## Overview

This repository provides a methodology for taking raw ASR (Automatic Speech Recognition) output and progressively refining it through layered prompts to produce a wide variety of text formats. By composing different instruction layers, you can generate everything from formal business emails to casual notes, technical documentation to quick to-do lists.

## How It Works

The system uses a **layered architecture** where each layer adds specific transformation instructions:

1. **Context Layer**: Foundational information about the input (voice/audio data) and user personalization
2. **Baseline Layer**: Basic text cleanup (typos, punctuation, paragraphs)
3. **Format Layer**: Output structure (email, documentation, to-do list, etc.)
4. **Tone Layer**: Formality level (formal, business, casual, informal)
5. **Emotional Layer**: Emotional register (heightened, neutral, low)
6. **Style Layer**: Additional style modifiers (concise, verbose, technical, conversational)
7. **Readability Layer**: Complexity level (simple, intermediate, advanced)

Layers are combined into **stacks** - predefined configurations for common use cases like "business email" or "technical documentation."

## Quick Start

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Text-Transformation-Prompt-Stack
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

1. **List available stacks**:
```bash
./concatenate.py --list
```

2. **Generate a prompt from a stack**:
```bash
./concatenate.py business-email.yaml
```

3. **Save to a file**:
```bash
./concatenate.py business-email.yaml -o prompt.txt
```

4. **Use the generated prompt with your LLM** along with your voice-to-text output.

## Directory Structure

```
Text-Transformation-Prompt-Stack/
├── layers/                    # Individual prompt layers
│   ├── context/              # Foundational context
│   │   ├── foundational.md
│   │   └── personalisation.md
│   ├── baseline/             # Basic text cleanup
│   │   ├── fix-typos.md
│   │   └── punctuation-and-paras.md
│   ├── format/               # Output formats
│   │   ├── email.md
│   │   ├── todo-list.md
│   │   ├── task-list.md
│   │   ├── freeform-text.md
│   │   └── documentation.md
│   ├── tone/                 # Formality levels
│   │   ├── maximum-formality.md
│   │   ├── business-appropriate.md
│   │   ├── minimum-formality.md
│   │   └── informal-interpersonal.md
│   ├── emotional/            # Emotional registers
│   │   ├── heightened-emotion.md
│   │   ├── neutral-emotion.md
│   │   └── low-emotion.md
│   ├── style/                # Style modifiers
│   │   ├── concise.md
│   │   ├── verbose.md
│   │   ├── technical.md
│   │   └── conversational.md
│   └── readability/          # Reading levels
│       ├── simple.md
│       ├── intermediate.md
│       └── advanced.md
├── stacks/                    # Predefined stack configurations
│   ├── business-email.yaml
│   ├── formal-email.yaml
│   ├── casual-note.yaml
│   ├── technical-documentation.yaml
│   ├── quick-todo.yaml
│   └── task-list.yaml
├── concatenate.py            # Stack concatenation script
├── ARCHITECTURE.md           # Detailed architecture documentation
└── README.md                 # This file
```

## Available Stacks

### Business Email
Professional business email with appropriate formality and concise style.
```bash
./concatenate.py business-email.yaml
```

### Formal Email
Highly formal email for official or ceremonial correspondence.
```bash
./concatenate.py formal-email.yaml
```

### Casual Note
Friendly, informal text for personal communications.
```bash
./concatenate.py casual-note.yaml
```

### Technical Documentation
Technical documentation with precise terminology and advanced readability.
```bash
./concatenate.py technical-documentation.yaml
```

### Quick To-Do
Simple, actionable to-do list from voice notes.
```bash
./concatenate.py quick-todo.yaml
```

### Task List
Structured task list with clear action items.
```bash
./concatenate.py task-list.yaml
```

## Creating Custom Stacks

You can create your own stack configurations by creating a YAML file in the `stacks/` directory:

```yaml
name: My Custom Stack
description: Description of what this stack does
layers:
  - layers/context/foundational.md
  - layers/context/personalisation.md
  - layers/baseline/fix-typos.md
  - layers/baseline/punctuation-and-paras.md
  - layers/format/email.md
  - layers/tone/business-appropriate.md
  - layers/emotional/neutral-emotion.md
  - layers/style/concise.md
  - layers/readability/intermediate.md
```

### Stack Design Guidelines

1. **Always include context layers**: Start with `foundational.md` and `personalisation.md`
2. **Typically include baseline layers**: Apply `fix-typos.md` and `punctuation-and-paras.md`
3. **Choose one format**: Select exactly one file from `layers/format/`
4. **Choose one tone**: Select exactly one file from `layers/tone/`
5. **Choose one emotional register**: Select exactly one file from `layers/emotional/`
6. **Add style modifiers as needed**: Include any relevant files from `layers/style/`
7. **Choose one readability level**: Select exactly one file from `layers/readability/`

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed information about the layer hierarchy and design patterns.

## Creating New Layers

To add a new transformation layer:

1. **Identify the category** (or create a new one if needed)
2. **Create a markdown file** in the appropriate `layers/` subdirectory
3. **Write a single, clear instruction** - keep it concise and actionable
4. **Test compatibility** - ensure it works well with other layers
5. **Update documentation** - add it to ARCHITECTURE.md if creating a new category

### Example Layer

```markdown
Ensure all monetary amounts are formatted with currency symbols and appropriate decimal places.
```

## Programmatic Usage

You can also use the concatenator in your own Python scripts:

```python
from concatenate import PromptStackConcatenator

# Initialize
concatenator = PromptStackConcatenator()

# List available stacks
stacks = concatenator.list_available_stacks()
print(stacks)

# Generate a prompt
prompt = concatenator.concatenate_from_file("business-email.yaml")

# Use the prompt with your LLM
# ... your LLM integration code here ...
```

## CLI Reference

```
usage: concatenate.py [-h] [-o OUTPUT] [-s SEPARATOR] [-l] [-r REPO_ROOT] [stack]

Concatenate text transformation prompt stack layers

positional arguments:
  stack                 Stack configuration file (from stacks/ directory or full path)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (default: stdout)
  -s SEPARATOR, --separator SEPARATOR
                        Separator between layers (default: double newline)
  -l, --list            List available stack configurations
  -r REPO_ROOT, --repo-root REPO_ROOT
                        Repository root directory (default: script directory)
```

## Use Cases

This system is particularly useful for:

- **Email composition** from voice notes
- **Meeting notes** transformation into structured documents
- **Technical documentation** generation from verbal explanations
- **Task extraction** from brainstorming sessions
- **Content creation** with consistent style and formatting
- **Multi-format output** from a single voice recording

## Typical Workflow

1. **Record voice note** using your preferred STT tool
2. **Select appropriate stack** for your desired output format
3. **Generate concatenated prompt** using this tool
4. **Submit to LLM** with your raw voice-to-text transcript
5. **Receive formatted output** according to your stack specifications

## Contributing

Contributions are welcome! To add new layers or stacks:

1. Follow the existing directory structure
2. Keep layer instructions focused and compatible
3. Test your additions with various combinations
4. Update documentation accordingly

## License

[Add your license here]

## Author

Daniel Rosehill

## Related Projects

- [Add links to your other text transformation projects here]