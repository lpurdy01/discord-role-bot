from langchain.agents import initialize_agent
from langchain.agents import AgentType
from agent_configurator import tools, llm, memory, prompt


def init_agent():
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True,
                                   memory=memory)
    agent_chain.agent.llm_chain.prompt = prompt
    return agent_chain



if __name__ == "__main__":
    agent_chain = init_agent()
    output = agent_chain.run(input="hi, i am bob")
    print(output)
    output = agent_chain.run(
        input="tell me the last letter in my name, and also tell me who won the world cup in 1978?")
    print(output)
