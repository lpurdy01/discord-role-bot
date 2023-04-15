from langchain.agents import initialize_agent
from langchain.agents import AgentType
from agent_configurator import tools, llm, memory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate
)
from langchain.prompts.prompt import PromptTemplate


def init_agent():
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True,
                                   memory=memory)
    system_message_prompt_template = agent_chain.agent.llm_chain.prompt.messages[0]
    message_placeholder_chat_history = agent_chain.agent.llm_chain.prompt.messages[1]
    human_message_prompt_template = agent_chain.agent.llm_chain.prompt.messages[2]
    message_placeholder_agent_scratchpad = agent_chain.agent.llm_chain.prompt.messages[3]

    prompt = ChatPromptTemplate.from_messages([
        system_message_prompt_template,
        message_placeholder_chat_history,
        human_message_prompt_template,
        message_placeholder_agent_scratchpad
    ])

    agent_chain.agent.llm_chain.prompt = prompt
    return agent_chain



if __name__ == "__main__":
    agent_chain = init_agent()
    output = agent_chain.run(input="hi, i am bob")
    print(output)
    output = agent_chain.run(
        input="tell me the last letter in my name, and also tell me who won the world cup in 1978?")
    print(output)
