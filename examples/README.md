# Examples

This directory contains example prompts generated from various stacks.

## Contents

- `sample-input.txt` - Raw voice-to-text input example
- `business-email-prompt.txt` - Generated prompt using business-email.yaml
- `casual-note-prompt.txt` - Generated prompt using casual-note.yaml

## Using These Examples

To see how the prompts work:

1. Look at the raw input in `sample-input.txt`
2. Examine the generated prompt (e.g., `business-email-prompt.txt`)
3. Combine them and send to your LLM:

```
[Contents of business-email-prompt.txt]

---

Input text:
[Contents of sample-input.txt]
```

## Expected Output Examples

### Business Email Output (from business-email.yaml)

```
Subject: Project Status Update and Meeting Request

Dear [Recipient],

I wanted to reach out regarding the project we've been working on. We're making good progress, but there are a couple of items that need to be addressed before next week's deadline.

First, the database migration is taking longer than expected. Second, we need to coordinate with the design team about the final UI mockups.

I suggest we schedule a meeting this week to review everything and ensure we're aligned. Please let me know what works for your schedule.

Best regards,
Daniel
```

### Casual Note Output (from casual-note.yaml)

```
Hey!

Just wanted to touch base about our project - things are going really well! But we've got a couple things to sort out before next week.

The database migration is running a bit behind, and we need to sync up with the design folks about those final UI mockups.

Think we should grab some time this week to chat through everything? Let me know when works for you!

- Daniel
```

## Generating Your Own Examples

```bash
# Generate a prompt
../concatenate.py stack-name.yaml -o my-prompt.txt

# Combine with your input
cat my-prompt.txt
echo "---"
echo ""
echo "Input text:"
cat your-input.txt
```
