if __name__ == "__main__":

    from agents import LangChainAgent
    from agent_pool import AgentPool
    from orchestrator import Orchestrator
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    import pandas as pd
    from langchain_community.llms import Ollama

    llm_mistral = Ollama(model="mistral")
    llm_openai = ChatOpenAI(openai_api_key="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")


    # Create prompt templates 
    prompt = ChatPromptTemplate.from_messages([("user", "{input}")])

    # Initialize chains
    opensource = prompt | llm_mistral
    closedsource = prompt | llm_openai
    judge = prompt | llm_openai


    # Initialize AgentPool and register agents
    agent_pool = AgentPool()
    agent_pool.register_agent(LangChainAgent(name="OpenSource", description="I am an expert debator and I present the side for open source AI as the future", agent = opensource))
    agent_pool.register_agent(LangChainAgent(name="ClosedSource",description= "I am an expert debator and I present the side for closed source AI as the future", agent = closedsource))
    agent_pool.register_agent(LangChainAgent(name="Judge", description="I judge the debate on the merits of each argument and select a winner for each discussion. Present your arguments", agent= judge))

    # Initialize Manager with specific configurations
    orchestrate = Orchestrator(agent_pool, scheduling='round_robin', num_rounds=2, max_calls=10, include_prior_history="global", start_agent_name='Judge')

    # Process task
    responses = orchestrate.process_task("We are here to judge the merits and demerits of closed vs open soure AI")

    for agent_name, response in responses:
        print("\n")
        print(f"Response from {agent_name}: {response}")
