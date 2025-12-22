![alt text](images/1.png)

 The purpose of this repository is to document and define in suggested layers a stack used to instruct audio multimodal models in the task of providing text in a desired end format. 
 
 This approach was originally used - and can also be used - in a combined ASR and LLM approach - which involves creating an audio processing pipeline that uses both parts to transform user-uploaded audio into a desired output format (like a business email). 
 
My current implementations, however, use audio multimodal/omni models to reduce this workflow to one step (audio and concatenated prompt in, formatted text out.)

The purpose of this stack is to define layers through which text output instructions can be applied so as to ensure so as to provide a robust and replicable methodology for enforcing this workflow.

![alt text](images/2.png)

The layering approach is desirable in my experience in order to define a baseline foundation for verbatim prompts transformations, and then to layer upon us in more specific stacks, like this:

![alt text](images/3.png)

The stacking approach is particularly powerful as it allows for extremely precise configurations to be created, simply through prompt concatenation logic.

## How It Works

The system uses a **layered architecture** where each layer adds specific transformation instructions:

1. **Context Layer**: Foundational information about the input (voice/audio data) and user personalization
2. **Baseline Layer**: Basic text cleanup (typos, punctuation, paragraphs)
3. **Reason-Based Layer**: Intelligent content filtering requiring inference (verbal corrections, unintended audio exclusion, repetition removal)
4. **Format Layer**: Output structure (email, documentation, to-do list, etc.)
5. **Tone Layer**: Formality level (formal, business, casual, informal)
6. **Emotional Layer**: Emotional register (heightened, neutral, low)
7. **Style Layer**: Additional style modifiers (concise, verbose, technical, conversational)
8. **Readability Layer**: Complexity level (simple, intermediate, advanced)

Layers are combined into **stacks** - predefined configurations for common use cases like "business email" or "technical documentation."

---

## Foundational Transcript Cleanup Prompt

The stack approach is useful both to generate concatenated prompts that provide specific text output adherence matching requirements for formatting, style, and even readability levels. 

The more pragmatic day-to-day use for this approach is in concatenating a comprehensive cleanup prompt that defines a precise level of editing deemed generally desirable in cleaning up text transcripts, but which does not go too far when editing the text or removing content. The challenge in defining this general-purpose cleanup approach is one of prompt engineering. 

If this prompt is too simplistic or understated, a lot of the potential value in audio multimodal is lost. 

If this prompt is too extensive, the model is too aggressive in rewriting the user's prompt and the likelihood that desirable text will be edited out increases. It is a balancing act! 

The general principle, however, is that the precise and unredacted replication of the user's speech is almost never desirable in speech-to-text or voice productivity workflows. 

As a simple example, almost no transcript benefits from "ehm" being included. There are edge cases - such as where exact transcripts are required for legal reasons. But these uses are not the focus of most speech users' engagement. Nor is it what the stack is intended to support. 

For this reason, the stack delineates between a foundational layer and a stylistic layer - this delineation being followed in the folder-based approach and the programmatic data definition that reflects it. 

The stylistic layer includes not only definitions for various styles, but also format-specific adherence. The potential permutations for this logic of prompt concatenation are rather vast, so the examples captured here are partial by nature.

## Structured Layer Definition

The complete transformation stack is defined in [`layers.json`](layers.json), which provides a structured data representation of all layers and their elements. This JSON file uses a **numeric hierarchy system** where the layer number represents the logical order of application:

```json
{
  "layers": [
    {
      "layer_number": 1,
      "name": "Context Layer",
      "description": "Foundational information about the input...",
      "usage": "Always applied - both files in this layer...",
      "elements": [
        {
          "name": "foundational",
          "file_path": "layers/context/foundational.md",
          "instruction": "The audio file provided..."
        }
      ]
    }
  ]
}
```

### Key Features

- **Numeric Hierarchy**: Layer numbers (1-8) represent the logical application order
- **Complete Metadata**: Each layer includes name, description, usage guidelines, and all elements
- **Element Details**: Each element contains its name, file path, and the actual instruction text
- **Programmatic Access**: The JSON structure enables easy integration with custom tools and automation

This structured representation is the **key novelty** of this repository, providing a machine-readable definition of the entire transformation stack that can be queried, analyzed, or extended programmatically.

## Example Stacks

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


## Author

Daniel Rosehill
