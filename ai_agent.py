import os
from dotenv import load_dotenv
from typing import List
from langchain.memory import ConversationBufferMemory 
from langchain_groq import ChatGroq
from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from template import PROMPT_TEMPLATE
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load .env variables
load_dotenv()

# LLM Initialization
#GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#llm = ChatGroq(temperature=0, model_name="llama3-groq-70b-8192-tool-use-preview", groq_api_key=GROQ_API_KEY, max_retries=7)
#llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, google_api_key=GOOGLE_API_KEY, convert_system_message_to_human=True)
#llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0, google_api_key=GOOGLE_API_KEY, convert_system_message_to_human=True)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=GOOGLE_API_KEY, convert_system_message_to_human=True)
#llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0)

def initialize_agent(tools: List, is_agent_verbose: bool = True, max_iterations: int = 5, return_thought_process: bool = True):
    """
    system_message = SystemMessage(content=SYSTEM_MESSAGE)
    MEMORY_KEY = "chat_history"
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name=MEMORY_KEY)],
        "system_message": system_message
    }
    memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)
    prompt = hub.pull("hwchase17/structured-chat-agent")
    """

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    memory = ChatMessageHistory(session_id="test-session")

    agent=create_structured_chat_agent(llm, tools, prompt)

    # Initialize agent
    agent_executor=AgentExecutor(agent=agent, tools=tools, verbose=is_agent_verbose, 
                                 handle_parsing_errors=True, max_iterations=max_iterations,
                                 return_intermediate_steps=return_thought_process
                                 )
    
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        # This is needed because in most real world scenarios, a session id is needed
        # It isn't really used here because we are using a simple in memory ChatMessageHistory
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    """
    agent_executor=AgentExecutor(agent=agent, tools=tools, verbose=is_agent_verbose, 
                                 handle_parsing_errors=True, max_iterations=max_iterations,
                                 return_intermediate_steps=return_thought_process, memory=memory,
                                 agent_kwargs=agent_kwargs)
    """

    return agent_with_chat_history
