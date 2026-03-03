---
description: How to implement Autonomous Tool Use in agents (Function Calling)
---

# Autonomous Tool Use Workflow

Based on the learnings from the Haven v2 (Luna) Belasis Integration, this workflow explains how to give an agent the ability to execute real-world actions (like checking availability, booking appointments, or querying a database) using Anthropic's tool-use API.

## Step 1: Define the Tools (JSON Schemas)

Create a dedicated file (e.g., `definitions.js`) containing the JSON schemas that describe what each tool does and what inputs it requires. The description is critical—the LLM reads this to decide *when* to use it.

```javascript
export const MY_TOOLS = [
  {
    name: "verificar_disponibilidade",
    description: "Verifica horários disponíveis. Use quando o cliente perguntar sobre horários livres.",
    input_schema: {
      type: "object",
      properties: {
        data: { type: "string", description: "Data no formato YYYY-MM-DD" },
        profissional_id: { type: "integer", description: "ID do profissional (opcional)" }
      },
      required: ["data"]
    }
  }
];
```

## Step 2: Implement the Tool Executor

Create a logic layer (e.g., `executor.js`) that connects the tool name to the actual backend service/API. This layer must return a string or JSON object describing the result of the action.

```javascript
export const toolExecutor = {
  execute: async (toolName, toolInput) => {
    try {
      switch (toolName) {
        case 'verificar_disponibilidade':
          const disponiveis = await myApi.getDisponibilidade(toolInput.data);
          return { success: true, horarios: disponiveis.map(h => h.time) };
        default:
          return { error: `Tool ${toolName} not found.` };
      }
    } catch (e) {
      return { success: false, error: e.message };
    }
  }
};
```

## Step 3: Implement the Recursive Loop in the Brain

When you pass `tools` to the Anthropic API, it might decide to stop and ask you to run a tool (`stop_reason === 'tool_use'`). You must catch this, execute the tool, feed the result back to the LLM, and let it generate the final response.

```javascript
let finalResponse = null;
let toolLoopCount = 0;
const MAX_TOOL_LOOPS = 5;

while (toolLoopCount < MAX_TOOL_LOOPS) {
  const response = await anthropicClient.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 1024,
    system: systemPrompt,
    messages: messages,
    tools: MY_TOOLS // <--- Pass the schemas here
  });

  if (response.stop_reason === 'tool_use') {
    // 1. Extract the requested tool
    const toolUse = response.content.find(c => c.type === 'tool_use');
    
    // 2. Execute it in your backend
    const toolResult = await toolExecutor.execute(toolUse.name, toolUse.input);

    // 3. Append the assistant's request AND the tool result to the history
    messages.push({ role: 'assistant', content: response.content });
    messages.push({
      role: 'user',
      content: [{ type: 'tool_result', tool_use_id: toolUse.id, content: JSON.stringify(toolResult) }]
    });

    // 4. Loop again so the LLM can read the result and answer the user
    toolLoopCount++;
    continue;
  }

  // If we reach here, the LLM replied with text.
  finalResponse = response.content[0].text;
  break;
}
```

## Important Considerations

- **Error Handling**: If a tool fails, pass the error back to the LLM (e.g., `{ error: "Service unavailable" }`). The LLM is smart enough to apologize to the user and try another approach.
- **Max Loops**: Always implement a `MAX_TOOL_LOOPS` variable to prevent infinite loops if the LLM gets stuck calling tools.
- **Validation**: Ensure the prompt explicitly tells the agent *how* to use the tools (e.g., "Always use `tool_X` to confirm prices before telling the customer").
