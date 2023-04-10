from dotenv import load_dotenv
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate
)
from langchain.prompts.prompt import PromptTemplate
from langchain.utilities import SerpAPIWrapper
import os
from langchain.agents import Tool
from langchain.memory import ConversationTokenBufferMemory
from langchain.chat_models import ChatOpenAI


load_dotenv()

search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERP_API_KEY"))
tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
    ),
]


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], output_parser=None, partial_variables={},
                                                      template='Assistant is a large language model trained by OpenAI.\n\nAssistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.\n\nAssistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.\n\nOverall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.',
                                                      template_format='f-string', validate_template=True),
                                additional_kwargs={}),
    MessagesPlaceholder(variable_name='chat_history'),
    HumanMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=['input'], output_parser=None, partial_variables={},
                              template='TOOLS\n------\nAssistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:\n\n> Current Search: useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term.\n\nRESPONSE FORMAT INSTRUCTIONS\n----------------------------\n\nWhen responding to me please, please output a response in one of two formats:\n\n**Option 1:**\nUse this if you want the human to use a tool.\nMarkdown code snippet formatted in the following schema:\n\n```json\n{{\n    "action": string \\ The action to take. Must be one of Current Search\n    "action_input": string \\ The input to the action\n}}\n```\n\n**Option #2:**\nUse this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:\n\n```json\n{{\n    "action": "Final Answer",\n    "action_input": string \\ You should put what you want to return to use here\n}}\n```\n\nUSER\'S INPUT\n--------------------\nHere is the user\'s input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):\n\n{input}',
                              template_format='f-string', validate_template=True), additional_kwargs={}),
    MessagesPlaceholder(variable_name='agent_scratchpad')
])

llm = ChatOpenAI(temperature=0, model="gpt-4")

memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=3000, return_messages=True, memory_key="chat_history")
