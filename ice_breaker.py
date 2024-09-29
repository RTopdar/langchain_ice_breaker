from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import json
import os
from dotenv import load_dotenv
from agents.linkedin_lookup_agent import lookup
from output_parsers import summary_parser

from third_party.third_party.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()

    print("This is the main langchain module")

    summary_template = """
    given the information {information} about a person that I got from linkedin, i want you to create
    1. a short bio
    2. a short description of their personality
    3. two interesting facts about them

    I need you to write it in a proper json format. 
    Also write which model you have used to generate this information.
    \nformat instructions: {format_instructions}
    """
    linkedin_url = lookup("Rounak Topdar")
    print(f"Linkedin URL: {linkedin_url}")

    information = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    summary_prompt = PromptTemplate(
        input_variables=[
            "information",
        ],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
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

    chain = summary_prompt | llm | summary_parser
    # lanchain expression language (LCEL)
    print("Invoking the chain")
    print(f"Using model: {llm.model_name}")
    res = chain.invoke(input={"information": information})
    print("Chain invoked")
    if hasattr(res, "dict"):
        res_dict = res.dict()
    else:
        res_dict = res

    # Serialize to JSON and write to file
    file_path = "response.json"
    with open(file_path, "w") as file:
        json.dump(res_dict, file, indent=4)

    print("Response written to response.json")
