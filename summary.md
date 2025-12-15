---
description: Create a summary of the history
---

## Your task

Evaluate thoroughly the conversation history to provide a comprehensive summary of the problem that we are trying to solve.

### Task Guidelines:

1. Information Analysis
 - Carefully analyze the conversation history to identify truly useful information.
 - Focus on information that directly contributes to the solution of the problem that we are trying to solve.
 - Do NOT make assumptions, guesses, or inferences beyond what is explicitly stated in the conversation.
 - If information is missing or unclear, do NOT include it in your summary.
2. Summary Requirements
 - Extract only the most relevant information that is explicitly present in the conversation.
 - Synthesize information from multiple exchanges when relevant. Only include information that is certain and clearly stated in the conversation.
 - Do NOT output or mention any information that is uncertain, insufficient, or cannot be confirmed from the conversation.

### Output format

Your response ALWAYS must be saved into a file named: $1 , structured as follows:

```
## Problem 
[Statement of the problem that we are trying to solve]

## Essential Information 
[Organize the relevant and certain information from the conversation history that helps address the question.]
```

## Rules
Strictly avoid fabricating, inferring, or exaggerating any information not present in the conversation.
Only output information that is certain and explicitly stated.
