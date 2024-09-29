from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import re
import os
from dotenv import load_dotenv
from agents.linkedin_lookup_agent import lookup

from third_party.third_party.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()

    print("This is the main langchain module")

    summary_template = """
    given the information {information} about a person that I got from linkedin, i want you to create
    1. a short bio
    2. a short description of their personality
    3. two interesting facts about them

    I need you to write it in a proper markdown format so that I can easily read it from a .md file. 
    Also write which model you have used to generate this information. 
    Also, are you sure that you are using gpt 3.5 and not using GPT 4o-mini, because I specifically asked for GPT 4o mini and paid for it 
    """
    linkedin_url = lookup("Rounak Topdar")
    print(f"Linkedin URL: {linkedin_url}")

    information = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    summary_prompt = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    models = {
        "gpt-4o-mini": ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        ),
        "llama3": ChatOllama(model="llama3"),
        "mistral": ChatOllama(model="mistral"),
        # Add more models as needed
    }
    llm = models["gpt-4o-mini"]

    chain = summary_prompt | llm | StrOutputParser()
    print("Invoking the chain")
    print(f"Using model: {llm.model_name}")
    res = chain.invoke(input={"information": information})

    with open("response.md", "w") as file:
        file.write(str(res))
    print("Response written to response.md")
