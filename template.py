PROMPT_TEMPLATE = """
    Respond to the human as helpfully and accurately as possible. You have access to the following tools:

    {tools}

    Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

    Valid "action" values: "Final Answer" or {tool_names}

    Provide only ONE action per $JSON_BLOB, as shown:

    ```
    {{
    "action": $TOOL_NAME,
    "action_input": $INPUT
    }}
    ```

    Follow this format:

    Question: input question to answer
    Thought: consider previous and subsequent steps
    Action:
    ```
    $JSON_BLOB
    ```
    Observation: action result
    ... (repeat Thought/Action/Observation N times)
    Thought: I know what to respond
    Action:
    ```
    {{
    "action": "Final Answer",
    "action_input": "Final response to human"
    }}

    Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation

    Also, considers the history of the following conversation so you either can answer the questions from the user or use the context from that conversation into the tools you have available to use:

    {chat_history}

    User Input: {input}

    {agent_scratchpad}

    (reminder to respond in a JSON blob no matter what)
"""

AGENT_MESSAGE = """
Welcome! I am your Instagram Agent, Tell me what action do you want to do.

#### 📸 Tools Available 📸
- **Create Post:** Create a Post about a Beautiful Sunset.
- **Upload a Story:** Upload a Story about a Green Montain.

#### 👤 Account Settings 👤 
- **Change Picture Profile:** Modify my Picture Profile with an Image of a Blue Sky.
- **Notes:** Publish a Note that says I Feel Hungry!
- **Bio:** Modify my Biography with the Message Currently Not In Love.
"""
