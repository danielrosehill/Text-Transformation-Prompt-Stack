# CLAUDE.md

## Project Overview

This repository defines a **modular prompt stack** for transforming raw audio into polished text using audio multimodal LLMs (primarily Gemini). The system constructs comprehensive system prompts by concatenating individual instruction layers.

### Core Concept

Traditional speech-to-text produces verbatim transcripts full of filler words, false starts, self-corrections, and missing punctuation. This stack leverages audio multimodal models to perform **intelligent transcription editing in a single pass**—producing text that reflects what the speaker *meant* to say, not merely what they said.

The key insight: with audio multimodal models (unlike Whisper + LLM pipelines), the model simultaneously processes audio tokens and text instructions. There's no intermediate verbatim transcript—the model reasons about the audio directly and applies all editing in one pass.

## Two-Stack Architecture

### Foundational Stack (Always Applied)

Located in `layers/foundational/`, these layers represent universally desirable cleanup:

| Order | Folder | Purpose |
|-------|--------|---------|
| 01 | `01-context/` | Task definition, establishes the transcription role |
| 02 | `02-exclusions/` | Background audio, filler words, repetitions |
| 03 | `03-corrections/` | Meta-instructions, spelling, grammar, punctuation, paragraphs, subheadings, capitalization |
| 04 | `04-inference/` | Smart format detection |
| 05 | `05-personalization/` | User-specific details (name, signature) |

**Design principle:** Maximum specificity—each discrete instruction is its own layer file, enabling modular construction.

### Stylistic Stack (Context-Specific)

Located in `layers/stylistic/`, select appropriate layers based on output needs:

| Category | Purpose | Selection Rule |
|----------|---------|----------------|
| `format-adherence/` | Output structure (email, docs, lists) | Select one |
| `tone/` | Formality level | Select one |
| `emotional/` | Emotional register | Select one |
| `writing-style/` | Style modifiers (concise, verbose, technical) | Select one or more |
| `readability/` | Complexity level | Select one |

## Key Files

- **`layers.json`** - Machine-readable definition of all layers with metadata
- **`concatenate.py`** - Script to build prompts from stack YAML configs
- **`generate-foundational.py`** - Generates the foundational prompt
- **`stacks/`** - Pre-built stack configurations (YAML files)
- **`generated/`** - Output directory for constructed prompts
- **`ref.md`** - API reference for target models (Gemini)

## Inferred Instructions

A key feature is "inferred instructions"—the model uses reasoning to identify content that should be excluded or corrected without explicit markup:

1. **Self-corrections**: "I went to the store—no wait, the pharmacy" → "I went to the pharmacy"
2. **Spelling instructions**: "Use Zod. Zod is spelled Z-O-D" → "Use Zod"
3. **Background interruptions**: Side conversations, doorbell, etc. are excluded
4. **Meta-instructions**: "scratch that", "don't include that" are acted upon

## Working with This Repository

### Adding New Layers

1. Create a `.md` file in the appropriate `layers/` subdirectory
2. Write a clear, single-purpose instruction
3. Update `layers.json` with the new layer metadata
4. Add to relevant stack configurations in `stacks/`

### Creating Custom Stacks

Create a YAML file in `stacks/`:

```yaml
name: My Custom Stack
description: Description of purpose
layers:
  # Include all foundational layers
  - layers/foundational/01-context/task-definition.md
  # ... rest of foundational stack
  # Then add stylistic layers
  - layers/stylistic/format-adherence/email.md
  - layers/stylistic/tone/business-appropriate.md
```

### Generating Prompts

```bash
# Generate from stack config
./concatenate.py business-email.yaml

# Generate foundational prompt only
./generate-foundational.py

# Test against audio
./test-foundational.py
```

## Audio Preprocessing Notes

For optimal results with Gemini:
- VAD (Voice Activity Detection) to remove silence
- Convert stereo to mono
- Compress to Opus format
- Target: under 20MB file size limit

## Target Model

Current testing uses `gemini-3-flash-preview`. See `ref.md` for API documentation links.
