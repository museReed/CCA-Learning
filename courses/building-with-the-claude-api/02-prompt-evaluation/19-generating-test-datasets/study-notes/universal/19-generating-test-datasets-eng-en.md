# Generating Test Datasets — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.2 (test datasets), 3.1 (eval design), 3.3 (eval execution) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 19 |

---

## One-Liner

You can bootstrap an eval dataset in minutes by asking Claude to generate realistic test cases for you — using a fast model like Haiku, JSON prefilling, and stop sequences to get parseable output on the first try.

---

## The Scenario: AWS Code Assistant

The lesson builds an eval system for a prompt that helps users write **AWS-specific code** in three output formats:

- Python code
- JSON configuration files
- Regular expressions

The key requirement: the output must be **clean** — no extra explanations, headers, or footers around the code. That clean-output requirement is exactly the kind of property an eval dataset is meant to stress-test.

The starting (v1) prompt:

```python
prompt = f"""
Please provide a solution to the following task:
{task}
"""
```

---

## Dataset Shape: An Array of Tasks

The dataset is an array of JSON objects where each object has a `task` property describing what we want Claude to accomplish:

```json
[
  { "task": "Description of task" },
  ...additional
]
```

This minimal shape is deliberate. At evaluation time you will loop over the array, interpolate each `task` into the prompt template, and run it through Claude. Adding fields later (expected output, category, difficulty) is easy; starting simple is faster.

---

## Why Use Haiku for Dataset Generation

The lesson explicitly recommends **Haiku** for dataset generation rather than the full Claude model. The reasoning is economic:

- Dataset generation is a bulk, creative task that doesn't need frontier-model reasoning.
- Haiku is faster and cheaper per call.
- A 100-entry dataset on Sonnet is expensive; on Haiku it's trivial.

This is a general pattern in the CCA curriculum: **use a fast model for bulk work, save the frontier model for the task under evaluation.**

---

## Helper Functions for Claude Interaction

The lesson introduces three helpers that will be reused throughout the chapter:

```python
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    response = client.messages.create(**params)
    return response.content[0].text
```

Three observations:

1. **`temperature=1.0` by default** — high entropy is good for dataset generation because you want *diverse* test cases, not a repetitive list.
2. **`stop_sequences` is wired in** — this is what lets the prefilling trick work cleanly (see below).
3. **`chat()` returns `.content[0].text`** — it abstracts away the content-block structure so the caller gets plain text.

---

## The Dataset Generation Function

The lesson's main function:

```python
def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Description of task",
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
```

Three prompt-engineering choices worth noting:

- **Example output in fenced block** — Claude gets a concrete shape to match, not just a description.
- **Two explicit constraints** — "single function/object/regex" and "don't require much code." These narrow the generation space so the dataset stays focused.
- **Exact count** — "Please generate 3 objects" gives deterministic output size.

---

## The JSON Prefilling + Stop Sequence Trick

The most important technique in the lesson:

```python
messages = []
add_user_message(messages, prompt)
add_assistant_message(messages, "```json")
text = chat(messages, stop_sequences=["```"])
return json.loads(text)
```

This is a canonical pattern for getting parseable JSON out of Claude. The mechanics:

1. **Append an assistant message containing ` ```json `** — Claude is told "you have already started writing a JSON code block, now continue."
2. **Set `stop_sequences=["```"]`** — Claude will stop generation the moment it tries to close the code fence.
3. **Parse the raw text with `json.loads`** — what comes back is pure JSON, no surrounding prose, no closing fence.

Why this matters: without prefilling, Claude often wraps output in prose ("Here is your dataset:") or forgets to close the fence. Prefilling + stop sequences turn JSON extraction from a regex-parsing problem into a trivial `json.loads` call.

This is a **D5 production pattern** as well as a D3 technique — you will use it anywhere you need structured output from Claude without tool use.

---

## Running It

```python
dataset = generate_dataset()
print(dataset)
```

This returns three test cases covering Python, JSON configs, and regex patterns for AWS-specific tasks.

---

## Persisting the Dataset

```python
with open('dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)
```

Saving the dataset to a file is essential because:

- **Reproducibility** — the same dataset must be reused across prompt iterations (otherwise comparisons are invalid, as covered in Lesson 18).
- **Version control** — you can commit `dataset.json` into the repo so every engineer scores against the same canonical input set.
- **Decoupling** — generation and execution become separate steps; you generate once, run evals many times.

The file lives next to the notebook so the eval runner in Lesson 20 can load it with `open("dataset.json", "r")`.

---

## Common Mistakes

1. **Using Sonnet for dataset generation** — wasted money; Haiku is the correct choice for bulk creative work.
2. **Skipping the JSON prefilling trick** — your parser will break on Claude's prose preamble and postamble.
3. **Forgetting `stop_sequences`** — without it, Claude closes the fence and may keep writing, corrupting the parse.
4. **Generating a dataset then regenerating it between prompt iterations** — this destroys comparability; generate once, persist to disk, reuse.
5. **Not specifying an exact count in the prompt** — "generate some test cases" gives you unpredictable sizes, breaking batch-processing assumptions.

---

> **Key Insight**
>
> The prefilling + stop-sequence trick is the single most reusable technique in this lesson. It turns "ask Claude for JSON" from a brittle parsing problem into a one-liner. Memorize it — it appears in D3 (dataset generation), D5 (structured output in production), and anywhere else you need machine-readable output without invoking the full tool-use protocol.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: dataset generation is a named sub-step of the eval workflow; know both the "generate with Claude" and "generate by hand" options.
- **D5 (Enterprise Deployment)**: the prefilling + stop-sequence pattern is a go-to for structured output in production systems.
- Be ready for exam questions like: "How do you bootstrap an eval dataset for a new prompt?" → generate with Haiku, prefill the JSON code fence, use stop sequences, `json.loads`, save to disk.

---

## Flashcards

| Front | Back |
|-------|------|
| Which model does the lesson recommend for dataset generation, and why? | Haiku — it is faster and cheaper than the full Claude model for bulk creative work like generating test cases. |
| What three output formats does the AWS code assistant prompt target? | Python code, JSON configuration files, and regular expressions. |
| What is the minimal shape of the dataset? | An array of JSON objects, each with a `task` property describing what Claude should accomplish. |
| How do you get clean JSON out of Claude without tool use? | Prefill an assistant message with ` ```json `, set `stop_sequences=["```"]`, then call `json.loads(text)` on the result. |
| What does `stop_sequences=["```"]` accomplish in this pattern? | It stops generation as soon as Claude writes the closing code fence, so the returned text is pure JSON. |
| Why is the dataset saved to disk? | So the same dataset can be reused across prompt iterations, which is required for valid score comparisons. |
| What two explicit constraints does the generation prompt include? | "Single Python function / JSON object / regex" and "do not require writing much code." |
| Default temperature in the `chat()` helper, and why? | `temperature=1.0` — higher entropy produces more diverse test cases, which is desirable for an eval dataset. |
