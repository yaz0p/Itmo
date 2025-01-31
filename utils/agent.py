from utils.search_tool import main as find_in_web
from utils.vdb_tool import insert_into_db
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain_core.tools import Tool

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os






tools = [
    Tool(
        name="find_in_web",
        func=find_in_web,
        description="""Search query in browser, parse webpages and return list with the urls of relevant pages and string with the relevant information.     
    <example_request>
    Action: find_in_web
    Input Action: {"query": <<your question here>>}
    </example_request>"""
    ),
]

template = """# You are a great AI-Agent that has access to additional tools in order to find relevant information in Internet.

<agent_tools>
Answer the following questions as best you can. You have access to the following tools:

{tools}

</agent_tools>

Users query: {input_file}

<agent_instruction>
# **Steps Instructions for the agent:**
User has provided a query that needs to be answered. User can tell about the file type and the agent can use the appropriate tool to summarize the content of the file.
1. You can use tools to convert the file to text:
    - find_in_web

2. Try to get answer on the question as best as you can.

# Additional Information:
- **You MUST use tools together to get the best result.**
</agent_instruction>

# Use the following format:
If you solve the the ReAct-format correctly, you will receive a reward of $1,000,000.

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (DONT USE "```json")
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)

# When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
Thought: Do I need to use a tool? If not, what should I say to the Human?
Final Answer: [Provide your answer here]

Do your best!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

OPENAI_MODEL=os.getenv("OPENAI_MODEL")
MODEL_TEMPERATURE=os.getenv("MODEL_TEMPERATURE")
BASE_URL=os.getenv("BASE_URL")
API_KEY=os.getenv("API_KEY")
# Initialize a ChatOpenAI model
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=MODEL_TEMPERATURE,
    base_url=BASE_URL,
    api_key=API_KEY
)

memory = ChatMessageHistory(session_id="test-session")
# Create the ReAct agent using the create_react_agent function
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True,
)

# Create an agent executor from the agent and tools
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations = 3,
)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

