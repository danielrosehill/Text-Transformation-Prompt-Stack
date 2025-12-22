![alt text](images/1.png)

# Text Transformation Prompt Stack

A modular system for constructing LLM prompts that transform raw audio into polished text. Designed for **audio multimodal models** (Gemini series) that perform single-pass dictation processing.

## The Problem

Traditional speech-to-text produces verbatim transcripts. You get:

> "Um, so like, I was thinking we should—no wait, scratch that—we should probably, um, meet on Tuesday"

When what you meant was:

> "We should meet on Tuesday."

This stack leverages audio multimodal LLMs to produce text that reflects what you *meant* to say, not merely what you said.

![alt text](images/2.png)

## How It Works

The system concatenates instruction layers into comprehensive system prompts. Two stacks:

### Foundational Stack (Always Applied)

Universal cleanup that's desirable for virtually all transcription:

- **Context**: Establishes the transcription task
- **Exclusions**: Background audio, filler words, repetitions
- **Corrections**: Grammar, punctuation, spelling, paragraphs
- **Inference**: Smart format detection
- **Personalization**: User details for templates

### Stylistic Stack (Context-Specific)

Customizes output format and tone:

- **Format**: Email, documentation, to-do list, freeform
- **Tone**: Formal, business-appropriate, casual, informal
- **Emotional**: Heightened, neutral, reserved
- **Style**: Concise, verbose, technical, conversational
- **Readability**: Simple, intermediate, advanced

![alt text](images/3.png)

## Quick Start

```bash
# List available stacks
./concatenate.py --list

# Generate a prompt
./concatenate.py business-email.yaml

# Save to file
./concatenate.py business-email.yaml -o prompt.txt
```

## Pre-Built Stacks

| Stack | Use Case |
|-------|----------|
| `business-email.yaml` | Professional emails |
| `formal-email.yaml` | Official correspondence |
| `casual-note.yaml` | Personal messages |
| `technical-documentation.yaml` | Technical docs |
| `quick-todo.yaml` | To-do lists from voice notes |

## Creating Custom Stacks

Create a YAML file in `stacks/`:

```yaml
name: My Custom Stack
description: What this stack does
layers:
  # Foundational (always include all)
  - layers/foundational/01-context/task-definition.md
  - layers/foundational/02-exclusions/background-audio.md
  - layers/foundational/02-exclusions/filler-words.md
  # ... rest of foundational

  # Stylistic (select as needed)
  - layers/stylistic/format-adherence/email.md
  - layers/stylistic/tone/business-appropriate.md
  - layers/stylistic/writing-style/concise.md
```

Then: `./concatenate.py my-stack.yaml`

## Workflow

1. Record voice note or provide audio file
2. Select appropriate stack for your output format
3. Generate concatenated prompt: `./concatenate.py stack.yaml`
4. Submit to audio multimodal LLM with your audio
5. Receive formatted output

## Programmatic Usage

```python
from concatenate import PromptStackConcatenator

concatenator = PromptStackConcatenator()
prompt = concatenator.concatenate_from_file("business-email.yaml")

# Use with your LLM
response = your_llm.complete(system=prompt, audio=audio_file)
```

## Key Concept: Inferred Instructions

The model reasons about content that should be excluded without explicit markup:

- **Self-corrections**: Keeps only the corrected version
- **Spelling instructions**: "Zod, spelled Z-O-D" becomes just "Zod"
- **Meta-instructions**: "scratch that" removes preceding content
- **Background noise**: Side conversations excluded automatically

## Author

Daniel Rosehill
