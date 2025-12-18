# Text Transformation Prompt Stack Architecture

## Overview

This system uses a layered approach to transform raw speech-to-text output into polished, formatted text. Layers are applied hierarchically, with each layer adding specific instructions to refine the output.

## Layer Hierarchy

Layers are applied in the following order:

### 1. Context Layer (Always Applied)
**Location**: `layers/context/`

Provides foundational context about the input and transformation process.

- `foundational.md` - Explains that input is voice/audio data
- `personalisation.md` - User-specific details (name, email signature, etc.)

**Usage**: Both files in this layer are always included in every stack.

---

### 2. Baseline Layer (Typically Always Applied)
**Location**: `layers/baseline/`

Basic text cleanup operations that should be applied to most transformations.

- `fix-typos.md` - Corrects spelling and grammatical errors
- `punctuation-and-paras.md` - Adds proper punctuation and paragraph breaks

**Usage**: Generally included in all stacks unless explicitly omitted.

---

### 3. Reason-Based Layer (Optional, Recommended)
**Location**: `layers/reason-based/`

Intelligent content filtering that requires reasoning and inference to identify what should be excluded or modified.

- `inferred-corrections.md` - Acts on verbal instructions like "scratch that" or "don't include that"
- `non-transcribed-audio.md` - Excludes unintended audio (greetings, interruptions, side conversations)
- `repetition-avoidance.md` - Removes redundant repetitions and honors user instructions to exclude content

**Usage**: Can include all files or select specific ones based on needs. These layers require the model to exercise judgment about user intent.

---

### 4. Format Layer (Select One)
**Location**: `layers/format/`

Defines the output format structure.

- `email.md` - Professional email with greeting and closing
- `todo-list.md` - Structured to-do list
- `task-list.md` - Task list format
- `freeform-text.md` - Unstructured text
- `documentation.md` - Technical documentation format

**Usage**: Choose exactly one format per stack.

---

### 5. Tone Layer (Select One)
**Location**: `layers/tone/`

Controls the formality and tone of the output.

- `maximum-formality.md` - Highly formal, ceremonial language
- `business-appropriate.md` - Professional business tone
- `minimum-formality.md` - Casual but respectful
- `informal-interpersonal.md` - Friendly, conversational

**Usage**: Choose exactly one tone per stack.

---

### 6. Emotional Layer (Select One)
**Location**: `layers/emotional/`

Controls the emotional register of the output.

- `heightened-emotion.md` - Expressive, emotionally engaged
- `neutral-emotion.md` - Balanced, moderate emotion
- `low-emotion.md` - Reserved, minimal emotional expression

**Usage**: Choose exactly one emotional register per stack.

---

### 7. Style Layer (Select One or More)
**Location**: `layers/style/`

Additional stylistic modifiers that can be combined.

- `concise.md` - Brief, to-the-point
- `verbose.md` - Detailed, expansive
- `technical.md` - Technical vocabulary and precision
- `conversational.md` - Approachable, dialogue-like

**Usage**: Can select multiple compatible style modifiers.

---

### 8. Readability Layer (Select One)
**Location**: `layers/readability/`

Controls the complexity and reading level.

- `simple.md` - Simple vocabulary, short sentences
- `intermediate.md` - Balanced complexity
- `advanced.md` - Sophisticated vocabulary and structure

**Usage**: Choose exactly one readability level per stack.

---

## Stack Composition

A complete stack is composed by:

1. **Always including**: Context layer (both files)
2. **Typically including**: Baseline layer (both files)
3. **Optionally including**: Reason-Based layer (one, some, or all files as needed)
4. **Selecting one** from: Format, Tone, Emotional, Readability
5. **Optionally adding**: One or more Style modifiers

### Example Stack: Business Email

```
layers/context/foundational.md
layers/context/personalisation.md
layers/baseline/fix-typos.md
layers/baseline/punctuation-and-paras.md
layers/reason-based/inferred-corrections.md
layers/reason-based/non-transcribed-audio.md
layers/reason-based/repetition-avoidance.md
layers/format/email.md
layers/tone/business-appropriate.md
layers/emotional/neutral-emotion.md
layers/style/concise.md
layers/readability/intermediate.md
```

### Example Stack: Casual Note

```
layers/context/foundational.md
layers/context/personalisation.md
layers/baseline/fix-typos.md
layers/baseline/punctuation-and-paras.md
layers/format/freeform-text.md
layers/tone/informal-interpersonal.md
layers/emotional/heightened-emotion.md
layers/style/conversational.md
layers/readability/simple.md
```

---

## Layer Design Guidelines

When creating new layers:

1. **Single Purpose**: Each layer should contain one clear instruction
2. **Brevity**: Keep instructions concise and actionable
3. **Compatibility**: Ensure layers can be combined without conflicts
4. **Context-Aware**: Layers should work with the assumption that other layers may be present
5. **No Redundancy**: Avoid repeating instructions that exist in other layers

---

## Adding New Layers

To add a new layer:

1. Identify which category it belongs to (or create a new category if needed)
2. Create a `.md` file in the appropriate `layers/` subdirectory
3. Write a clear, single-purpose instruction
4. Update this architecture document if creating a new category
5. Add the layer to relevant stack configurations

---

## Custom Stack Creation

Users can create custom stacks by:

1. Creating a stack configuration file in `stacks/`
2. Listing the desired layer files in order
3. Running the concatenation script to generate the final prompt

See the `stacks/` directory for predefined examples.
