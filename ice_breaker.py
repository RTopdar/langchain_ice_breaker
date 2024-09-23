from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import re
import os
from dotenv import load_dotenv


def extract_markdown_content(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()

    # Use regex to extract the content field
    match = re.search(r"content='(.*?)' additional_kwargs", file_content, re.DOTALL)
    if match:
        markdown_content = match.group(1)
        return markdown_content
    else:
        return None


def save_markdown_content(markdown_content, output_file_path):
    with open(output_file_path, "w") as file:
        file.write(markdown_content)


if __name__ == "__main__":
    load_dotenv()

    print("This is the main langchain module")

    # summary_template = """
    # given the information {information} about a person, i want you to create
    # 1. a short bio
    # 2. a short description of their personality
    # 3. two interesting facts about them

    # I need you to write it in a proper markdown format so that I can easily read it from a .md file. Also write which model you have used to generate this information
    # """

    summary_template = """

    Do you know about vergil in devil may cry 5 
    and of the like a prayer song by madonna? I want you to write me a song 
    that is a mix of both. Format it properly for a .md file
    """


    information = [
        {
            "name": "John Doe",
            "age": 25,
            "occupation": "Software Engineer",
            "location": "San Francisco",
            "hobbies": ["reading", "hiking", "biking"],
            "interests": ["machine learning", "data science", "blockchain"],
        },
        {
            "name": "Jane Doe",
            "age": 30,
            "occupation": "Data Scientist",
            "location": "New York",
            "hobbies": ["painting", "cooking", "traveling"],
            "interests": ["artificial intelligence", "big data", "neural networks"],
        },
        {
            "name": "Alice Smith",
            "age": 35,
            "occupation": "Product Manager",
            "location": "Los Angeles",
            "hobbies": ["swimming", "dancing", "singing"],
            "interests": ["product design", "user experience", "agile methodology"],
        },
    ]
    summary_prompt = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    models = {
    "gpt-4o-mini": ChatOpenAI(temperature=0, model_name="gpt-4o-mini"),
    "llama3": ChatOllama(model="llama3"),
    "mistral": ChatOllama(model="mistral"),
    # Add more models as needed
}

    # llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    # llm = ChatOllama(model="llama3")
    llm = models["gpt-4o-mini"]

    chain = summary_prompt | llm | StrOutputParser()
    print("Invoking the chain")
    res = chain.invoke(input={"information": information[2]})

    with open("response.md", "w") as file:
        file.write(str(res))
    print("Response written to response.md")
