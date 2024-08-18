from typing import List
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(temperature=0.4, model="llama3-8b-8192")


class PainPointsRevision(BaseModel):
    revision_plan: str = Field(description="revision plan for the student based on his/her learning pain points")
    pain_points: List[str] = Field(description="5-10 learning pain points for the student based on their submission")


def detect_pain_points(submissions):
    prompt_template = """
        You are given submissions by a student for the course "Programming in Python". You are tasked to identify 5-10 concepts of the course where the student is struggling or the student has not understood the course module or in which assignments (theory or programming, graded or practice) is he/she struggling.
        
        The submissions are presented to you as a list of objects with module_id, module_name, assignment_type (theory or programming), assessment_type (graded or practice), and grade as keys of the object as follow:
        {submissions}
        
        Identify the learning pain points, in order of importance (first is most important and last is least important), in a manner that caters to concepts of Python but do not list down the module names in the output. Write something like: "Difficulty in understanding dictionaries as key-value pairs".
        
        But while listing, don't be harsh, be selective and maintain a friendly and approachable tone.
        
        After identifying the learning pain points, devise a revision plan for the student highlighting what aspects should he focus on, such as which modules should he/she revise first, and which type of questions (programming or theory) should he/she practice more.
        
        Based on this list of submissions, return the pain points and revision plan in JSON format. Do not provide boilerplate text,
        no explanation, no unnecessary text to explain the output, not even the 'Here is
        the response' like text.
        
        Here are the format instructions for the output:
        
        {format_instructions}
        """

    parser = PydanticOutputParser(pydantic_object=PainPointsRevision)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["submissions"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser
    response = chain.invoke({"submissions": str(submissions)})

    output = {}
    output['revision_plan'] = response.revision_plan
    output['pain_points'] = []
    for p in response.pain_points:
        output['pain_points'].append(p)

    return output
