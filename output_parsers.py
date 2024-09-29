from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(
        description="The summary of the person",
        example="John Doe is a software engineer with 5 years of experience. He is a hardworking person and a team player. He has worked on various projects in the past and has a good understanding of the latest technologies.",
    )
    facts: List[str] = Field(
        description="Two interesting facts about the person",
        example=[
            "John has a pet dog named Max.",
            "John loves to travel and explore new places.",
        ],
    )

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
