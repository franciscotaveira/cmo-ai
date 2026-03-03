---
description: How to implement Smart LLM Routing for cost-effective AI agents
---

# Smart LLM Routing Workflow

Based on the learnings from the Haven v2 (Luna) implementation, this workflow explains how to build a Smart Router that dynamically selects between a fast/cheap model (e.g., Claude 3.5 Haiku) and a powerful/expensive model (e.g., Claude 3.5 Sonnet) based on the user's input complexity.

## Step 1: Define Complexity Patterns

Create dictionaries of RegEx patterns to classify user intent.

- **Simple Patterns**: Greetings, confirmations, simple questions (e.g., "hi", "yes", "what time?").
- **Complex Patterns**: Complaints, reasoning requests, complex modifications (e.g., "I need to cancel because...", "I'm not sure which service to choose").

## Step 2: Build the Routing Logic

Implement a service (e.g., `smartRouter.js`) with a `routeToModel(message, history)` function:

1. **Check Complex Patterns First**: If the message matches a complex pattern, immediately return the powerful model (Sonnet).
2. **Evaluate History Depth**: If the conversation history is long (e.g., > 6 messages), the context is deep. Route to the powerful model to avoid context hallucination or dropped context.
3. **Check Simple Patterns**: If the message matches a simple pattern, return the fast model (Haiku).
4. **Fallback**: Set a default baseline model if neither matches (usually the fast one to save costs).

**Example Implementation:**

```javascript
export const smartRouter = {
  routeToModel: (message, conversationHistory = []) => {
    for (const p of complexPatterns) if (p.test(message)) return 'claude-3-5-sonnet';
    if (conversationHistory.length > 6) return 'claude-3-5-sonnet';
    for (const p of simplePatterns) if (p.test(message)) return 'claude-3-5-haiku';
    return 'claude-3-5-haiku';
  }
};
```

## Step 3: Integrate with the Agent Brain

Call the `smartRouter` right before initiating the LLM request. Replace hardcoded model strings with the dynamically returned model.

## Step 4: Implement Usage Logging (Crucial)

Track tokens and calculate estimated costs based on the dynamically chosen model to measure the ROI of the router. Store this in Redis or PostgreSQL.

```javascript
const COSTS = {
  'claude-3-5-haiku': { in: 0.00025, out: 0.00125 }, // Per 1k tokens
  'claude-3-5-sonnet': { in: 0.003, out: 0.015 }
};
// Log cost = (tokens_in * in) + (tokens_out * out)
```

## When to use this workflow

Use this whenever you are building a conversational agent that receives a high volume of low-complexity messages but still needs to handle complex edge cases gracefully.
