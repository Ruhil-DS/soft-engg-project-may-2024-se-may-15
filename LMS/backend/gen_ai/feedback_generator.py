import os
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(temperature=0.4, model="llama3-8b-8192")

class Feedback(BaseModel):
    feedback: str = Field(description="feedback for the question highlighting where the student might have gone wrong")
    tip: str = Field(description="tip to help the student for avoiding such mistakes in the future")

def generate_theory_feedback(module, question, options, chosen_option, correct_option):
    prompt_template = """
        You are given submission for a multiple-choice question based assignment by a student for the module {module_name}. You are tasked to identify if the chosen option matches the correct option, and give feedback (whether correct or not) and a tip to attempt such questions in the future.
        
        The question is "{question}" and the options are "1. {option_1}", "2. {option_2}", "3. {option_3}", "4. {option_4}". Student has chosen option "{chosen_option}" and the correct option is "{correct_option}".
        
        Based on this submission, return the feedback in JSON format. Do not provide boilerplate text, no explanation, no unnecessary text to explain the output, not even the 'Here is the response' like text.
        
        Here are the format instructions for the output:
        
        {format_instructions}
        """
    
    parser = PydanticOutputParser(pydantic_object=Feedback)
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["module_name", "question", "option_1", "option_2", "option_3", "option_4", \
            "chosen_option", "correct_option"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | model | parser
    
    return chain.invoke({"module_name": module.module_name, "question": question.question, \
        "option_1": options[0].option, "option_2": options[1].option, "option_3": options[2].option, \
        "option_4": options[3].option, "chosen_option": chosen_option.option, \
        "correct_option": correct_option.option})

def generate_programming_feedback(question, chosen_option, correct_option):
    pass

def generate_code_help(question, chosen_option, correct_option):
    pass