# Quick Usage Guide

## Common Commands

### List All Available Stacks
```bash
./concatenate.py --list
```

### Generate a Prompt
```bash
./concatenate.py business-email.yaml
```

### Save to File
```bash
./concatenate.py business-email.yaml -o my-prompt.txt
```

### Use Custom Separator
```bash
./concatenate.py business-email.yaml -s " | "
```

---

## Quick Stack Reference

| Stack | Use Case | Key Features |
|-------|----------|--------------|
| `business-email.yaml` | Professional emails | Business tone, concise, intermediate readability |
| `formal-email.yaml` | Official correspondence | Maximum formality, verbose, advanced readability |
| `casual-note.yaml` | Personal messages | Informal tone, conversational, simple readability |
| `technical-documentation.yaml` | Technical docs | Technical style, verbose, advanced readability |
| `quick-todo.yaml` | To-do lists | Minimal formality, concise, simple readability |
| `task-list.yaml` | Project tasks | Business tone, concise, intermediate readability |

---

## Typical Workflow

1. **Record your voice note** using your STT tool (e.g., Whisper, Google STT, etc.)

2. **Choose the appropriate stack** based on your desired output

3. **Generate the prompt**:
   ```bash
   ./concatenate.py business-email.yaml -o prompt.txt
   ```

4. **Send to your LLM** with this structure:
   ```
   [Contents of prompt.txt]

   ---

   Input text:
   [Your raw voice-to-text transcript here]
   ```

5. **Receive formatted output** in your desired format

---

## Creating a Custom Stack

Create a new YAML file in `stacks/` directory:

```yaml
name: My Custom Stack
description: What this stack does
layers:
  - layers/context/foundational.md       # Always include
  - layers/context/personalisation.md    # Always include
  - layers/baseline/fix-typos.md         # Usually include
  - layers/baseline/punctuation-and-paras.md  # Usually include
  - layers/format/email.md               # Choose one format
  - layers/tone/business-appropriate.md  # Choose one tone
  - layers/emotional/neutral-emotion.md  # Choose one emotional level
  - layers/style/concise.md              # Add style modifiers
  - layers/readability/intermediate.md   # Choose one readability
```

Then use it:
```bash
./concatenate.py my-custom-stack.yaml
```

---

## Layer Categories Quick Reference

### 1. Context (Always Include)
- `foundational.md` - Voice/audio context
- `personalisation.md` - User details

### 2. Baseline (Usually Include)
- `fix-typos.md` - Fix errors
- `punctuation-and-paras.md` - Format text

### 3. Format (Choose One)
- `email.md` - Email format
- `todo-list.md` - To-do list
- `task-list.md` - Task list
- `freeform-text.md` - Unstructured text
- `documentation.md` - Documentation format

### 4. Tone (Choose One)
- `maximum-formality.md` - Very formal
- `business-appropriate.md` - Professional
- `minimum-formality.md` - Casual
- `informal-interpersonal.md` - Friendly

### 5. Emotional (Choose One)
- `heightened-emotion.md` - Expressive
- `neutral-emotion.md` - Balanced
- `low-emotion.md` - Reserved

### 6. Style (Can Choose Multiple)
- `concise.md` - Brief
- `verbose.md` - Detailed
- `technical.md` - Technical vocabulary
- `conversational.md` - Dialogue-like

### 7. Readability (Choose One)
- `simple.md` - Easy to read
- `intermediate.md` - Moderate complexity
- `advanced.md` - Sophisticated

---

## Examples

### Example 1: Business Email from Voice Note
```bash
./concatenate.py business-email.yaml -o prompt.txt
```

Then combine with your transcript:
```
[Contents of prompt.txt]

---

Input text:
Hey so I wanted to reach out about the project timeline we discussed
last week um I think we need to push back the deadline by about two
weeks because of the resource constraints and also the scope has
changed a bit so yeah let me know if that works for you
```

Result: Professional business email with proper formatting.

---

### Example 2: Quick To-Do List
```bash
./concatenate.py quick-todo.yaml
```

Input:
```
okay so things I need to do today um first call the dentist and
reschedule that appointment then I need to finish the report for
the meeting tomorrow also pick up groceries and don't forget to
send that email to Sarah about the conference
```

Result: Clean, actionable to-do list.

---

## Troubleshooting

### "Stack file not found"
Make sure you're either:
- Running from the repository root directory
- Providing the full path to the stack file
- Using just the filename if it's in the `stacks/` directory

### "Layer file not found"
Check that all layer files referenced in your stack YAML actually exist in the `layers/` directory.

### ImportError: No module named 'yaml'
Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Tips

1. **Test your stacks** - Try different combinations to see what works best for your use case
2. **Keep layers simple** - Each layer should have one clear purpose
3. **Document custom stacks** - Add clear descriptions to your YAML files
4. **Version control personalization** - Update `personalisation.md` for your specific needs
5. **Experiment with separators** - Try different separators to see what your LLM prefers

---

## Integration Ideas

### Shell Alias
Add to your `.bashrc` or `.zshrc`:
```bash
alias prompt-gen='python3 /path/to/concatenate.py'
```

Usage:
```bash
prompt-gen business-email.yaml
```

### API Integration
Use the Python module in your own scripts:
```python
from concatenate import PromptStackConcatenator

concatenator = PromptStackConcatenator()
prompt = concatenator.concatenate_from_file("business-email.yaml")

# Use with your LLM API
response = your_llm_api.complete(
    prompt=prompt + "\n\n---\n\nInput text:\n" + transcript
)
```

### Automation Pipeline
Create a pipeline that:
1. Records voice → STT
2. Generates appropriate prompt
3. Sends to LLM
4. Returns formatted output

---

For more details, see [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md).
