# Changelog

## V2 (Current)

Major architectural revision introducing the two-stack architecture.

### Two-Stack Architecture

The layer system is now split into two distinct stacks:

- **Foundational Stack** (`layers/foundational/`) - Universal baseline corrections applied to all transcriptions
- **Stylistic Stack** (`layers/stylistic/`) - Context-specific formatting and style adjustments

### Foundational Stack Structure

Reorganized into numbered subfolders showing application order:

```
layers/foundational/
├── 01-context/
│   └── task-definition.md
├── 02-exclusions/
│   ├── background-audio.md
│   ├── filler-words.md
│   └── repetitions.md
├── 03-corrections/
│   ├── meta-instructions.md
│   ├── spelling-clarifications.md
│   ├── grammar-and-typos.md
│   └── punctuation.md
├── 04-inference/
│   └── format-detection.md
└── 05-personalization/
    └── user-details.md
```

### Stylistic Stack Structure

Organized by category:

```
layers/stylistic/
├── format-adherence/
├── tone/
├── emotional/
├── writing-style/
└── readability/
```

### New Layers Added

- **Filler Words Removal** (`filler-words.md`) - Removes "um", "uh", "like", and other verbal hesitations
- **Format Detection** (`format-detection.md`) - Infers intended output format from context
- **Spelling Clarifications** (`spelling-clarifications.md`) - Handles spelled-out words in dictation

### Layer Improvements

- **Task Definition** - Enhanced context-setting with comprehensive instructions for single-pass dictation processing
- **Grammar and Typos** - Expanded to include homophone correction and mistranscription handling
- **Punctuation** - Added guidance for paragraph breaks and sentence capitalization

### Structural Changes

- `layers.json` updated to version 2.0.0 with foundational/stylistic split
- File paths updated to reflect new folder structure
- Layer numbering now reflects logical application order

## V1 (Archived)

Initial release of the Text Transformation Prompt Stack with base layers for:
- Baseline corrections (typos, punctuation)
- Context layers (foundational, personalisation)
- Emotional tone layers (heightened, low, neutral)
- Format layers (documentation, email, freeform text, task list, todo list)
- Readability layers (advanced, intermediate, simple)
- Reason-based layers (inferred corrections, non-transcribed audio, repetition avoidance)
- Style layers (concise, conversational, technical, verbose)
- Tone layers (business appropriate, informal interpersonal, maximum/minimum formality)
