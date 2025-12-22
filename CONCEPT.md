# Text Transformation Prompt Stack: Concept

## Overview

The Text Transformation Prompt Stack is a modular system for constructing LLM prompts that transform raw audio transcriptions into polished, formatted text. This system is specifically designed for **audio multimodal models** (e.g., Gemini series) that can perform single-pass dictation processing—receiving audio directly and producing edited text that goes far beyond verbatim transcription.

## The Core Innovation

Traditional speech-to-text produces verbatim transcripts. Users then must manually edit out:
- Filler words ("um", "uh", "like")
- False starts and self-corrections
- Meta-instructions ("scratch that", "don't include that")
- Background conversations and interruptions
- Repetitive statements of the same idea
- Missing punctuation and paragraph breaks

This stack leverages multimodal LLMs to perform **intelligent transcription editing in a single pass**, producing text that reflects what the speaker *meant* to say, not merely what they said.

## Two-Stack Architecture

### 1. Foundational Stack (Always Applies)

The foundational stack contains editing instructions that are **universally desirable** for virtually all transcription use cases. These represent corrections that no reasonable user would want to see in their final text.

**Foundational layers include:**

| Layer | Purpose |
|-------|---------|
| `context/foundational.md` | Establishes the audio processing context |
| `baseline/fix-typos.md` | Corrects typos and grammatical errors |
| `baseline/punctuation-and-paras.md` | Restores punctuation and paragraph structure |
| `reason-based/inferred-corrections.md` | Handles meta-instructions ("scratch that") |
| `reason-based/non-transcribed-audio.md` | Excludes background conversations/interruptions |
| `reason-based/repetition-avoidance.md` | Consolidates redundant repetitions |
| `reason-based/spelling-resolution.md` | Processes spelled-out words ("Z-O-D" → "Zod") |

**The foundational stack premise:** There exists a baseline level of text cleanup that is almost always desirable. Outside of narrow use cases like court transcription requiring verbatim records, no user benefits from seeing "umm" written out or reading the same idea expressed three different ways.

### 2. Format Adherence Stack (Context-Specific)

Built on top of the foundational stack, format adherence layers customize the output for specific purposes:

- **Format layers:** email, documentation, task lists, freeform text
- **Tone layers:** formal, business-appropriate, informal
- **Style layers:** concise, verbose, technical, conversational
- **Readability layers:** simple, intermediate, advanced
- **Emotional layers:** neutral, heightened, low

## System Prompt Construction

The complete system prompt is constructed by concatenating layers in order:

```
[Foundational Context]
[Baseline Corrections]
[Reason-Based Intelligence]
[Format Specification]
[Tone/Style/Readability Modifiers]
```

The result is a comprehensive instructional prompt (typically 400-700 words) that provides determinative guidance for consistent, reliable text transformation.

## Versioning Strategy

### Individual Layers
Each layer is version-controlled as a separate markdown file in `layers/v{N}/`. This allows:
- Iterative refinement of specific instructions
- A/B testing of layer variations
- Clear history of changes to each editing rule

### Concatenated Prompts
Complete system prompts are generated and stored in `prompts/` with version identifiers:
- `prompts/foundational-v2.0.md` - Full foundational stack prompt
- `prompts/business-email-v2.0.md` - Business email stack prompt

This enables:
- Version control of the actual prompts used in production
- Direct comparison between prompt versions
- Reproducible results by referencing specific prompt versions

## Usage

### Generate a Complete Prompt

```bash
# Generate foundational stack prompt
python concatenate.py foundational-stack.yaml -o prompts/foundational-v2.0.md

# Generate format-specific stack prompt
python concatenate.py business-email.yaml -o prompts/business-email-v2.0.md

# List available stacks
python concatenate.py --list
```

### In Your Application

The generated prompts are designed to be used as system prompts with audio multimodal models:

```
System Prompt: [Contents of prompts/foundational-v2.0.md]
User Input: [Audio file]
Model Output: [Polished, formatted text]
```

## Design Principles

1. **Determinism over flexibility:** Comprehensive instructions reduce model interpretation variance
2. **Layered composition:** Complex behaviors built from simple, testable components
3. **Universal baseline:** Foundational corrections apply without user configuration
4. **Explicit versioning:** Both components and assembled prompts are versioned

## Comparison to Verbatim Transcription

| Verbatim (Traditional) | Intelligent (This Stack) |
|------------------------|--------------------------|
| "Um, so like, I was thinking we should—no wait, scratch that—we should probably, um, meet on Tuesday" | "We should meet on Tuesday." |
| Includes all filler words | Removes filler words |
| Includes self-corrections | Applies self-corrections |
| Includes meta-instructions | Acts on meta-instructions |
| No punctuation/structure | Proper punctuation and paragraphs |
| Background noise transcribed | Background conversations excluded |
