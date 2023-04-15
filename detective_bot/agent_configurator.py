from dotenv import load_dotenv

from langchain.utilities import SerpAPIWrapper
import os
from langchain.agents import Tool
from langchain.memory import ConversationTokenBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents.react.base import DocstoreExplorer
from langchain import Wikipedia
from langchain.utilities import PythonREPL

load_dotenv()

docstore = DocstoreExplorer(Wikipedia())

search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERP_API_KEY"))
tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
    ),
    Tool(
        name="Wikipedia",
        func=docstore.search,
        description="A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, historical events, or other subjects. Input should be a search query."
    ),
    Tool(
        name="Python REPL",
        func=PythonREPL().run,
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you expect output it should be printed out."
    )
]

llm = ChatOpenAI(temperature=0, model="gpt-4")

memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=3000, return_messages=True, memory_key="chat_history")
