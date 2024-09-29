import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv

from lang_tools.tools import get_profile_url

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    # the create_react_agent function based on the react algorithm that takes a llm as power to perform some tasks
    AgentExecutor,
    #  agentexecutor is the runtime of the agent. it is the object which is going to receive the prompts, the instructions, and finish the task
)
from langchain import hub


def lookup(name: str) -> str:
    # This function is the main function of the agent. It receives a name and returns the linkedin profile of the person
    # The linkedin profile is the result of the agent
    # The function is going to be called by the agent executor

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", model="gpt-4o-mini")

    template = """
    I am going to provide you the full name {name} of a person. I need you to go to linkedin, 
    find their profile page, and provide me the ONLY link 
    to their profile page on linkedin. If there are multiple entries, choose the one with the latest activity or the most relevant one. 
    do not give me a direct search results. I need an exact profile.
    One more thing to note, I will give you the name in the format of "Firstname Lastname Companyname" or "Firstname lastname". Make sure that it matches the format.
    
    """

    prompt = PromptTemplate(input_variables=["name"], template=template)

    tools = [
        Tool(
            name="Crawl google 4 linkedin profile pages.",
            description="Crawl google for linkedin profile pages, good for finding urls.",
            func=get_profile_url,
        )
    ]
    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
    )
    result = agent_executor.invoke(
        input={
            "input": prompt.format_prompt(name=name),
        }
    )
    linkedin_url = result["output"]

    return linkedin_url


if __name__ == "__main__":
    print(lookup("Rounak Topdar"))
