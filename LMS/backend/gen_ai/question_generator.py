import os
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import json

os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(temperature=0.4, model="llama3-8b-8192")

class Option(BaseModel):
    option_num: int = Field(description="answer option number for listing in the question")
    option: str = Field(description="answer option text to be displayed")
    is_correct: bool = Field(description="identicator if the option is correct or not")

class TheoryQuestion(BaseModel):
    question_num: int = Field(description="theory question number for listing in the assignment")
    question: str = Field(description="theory question for the assignment")
    options: List[Option] = Field(description="list of answer options for the question")
    
class TheoryQuestionList(BaseModel):
    __root__: List[TheoryQuestion] = Field(description="list of theory questions for the assignment")

def generate_theory_questions(course, module):
    prompt_template = """
        You work for an instructor who teaches the course {course_name}. You are tasked to design multiple-choice questions (with only one correct answer) for the course module {module_name} so that students can practice the concepts covered in the module.
        
        Design 5 questions for the module in JSON format. Make sure the questions are related to topics covered in the module. All questions must be Multiple-Choice Questions (MCQs) with just one correct answer. You must provide the question as well as 4 options per question. Highlight the correct option by assigning its is_correct attribute to true, false for the rest.
        
        Just return the set of questions as a List of Questions in JSON. Do not provide boilerplate text, no explanation, no unnecessary text to explain the output, not even the 'Here is the response' like text.
        
        Here are the format instructions for the output:
        
        {format_instructions}
        """
    
    parser = PydanticOutputParser(pydantic_object=TheoryQuestionList)
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["course_name", "module_name"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | model | parser
    
    return chain.invoke({"course_name": course.course_name, "module_name": module.module_name})


class ProgrammingQuestionList(BaseModel):
    __root__: List[str] = Field(description="list of programming questions for the assignment")

def generate_programming_questions(course, module):
    prompt_template = """
        You work for an instructor who teaches the course {course_name}. You are tasked to design programming questions for the course module {module_name} so that students can practice the concepts covered in the module.
        
        Design 2 programming questions for the module in JSON format. Make sure the questions are related to topics covered in the module. All questions must start with 'Define a function...' so that it is easy for the backend to run and check the code.
        
        Just return the set of questions as a List of Questions in JSON. Do not provide boilerplate text, no explanation, no unnecessary text to explain the output, not even the 'Here is the response' like text.
        
        Here are the format instructions for the output:
        
        {format_instructions}
        """
    
    parser = PydanticOutputParser(pydantic_object=ProgrammingQuestionList)
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["course_name", "module_name"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | model | parser
    
    return chain.invoke({"course_name": course.course_name, "module_name": module.module_name})