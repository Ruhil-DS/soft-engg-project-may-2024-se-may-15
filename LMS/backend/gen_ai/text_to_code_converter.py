import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import json

os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(temperature=0.8, model="llama3-8b-8192")


def get_converted_code(transcript, coding_language, question):
    prompt = f"""
        You work for an online Learner Management System (LMS). One of the functionalities of this
        portal is that it fosters inclusivity for students. It allows students with limited motor skills
        to speak the code verbatim and the portal will format the code accordingly.
        
        You are given the audio transcript for the code that needs to be retyped and formatted so that
        it is executable in {coding_language}. Make sure you do not modify what was mentioned in the
        transcript.
        
        Here is the audio transcript that needs to be converted to {coding_language}:
        "{transcript}"
        
        Here is the assignment question for which the above code was spoken:
        "{question}"
        
        Do not modify the workings of the function based on the question. Convert to {coding_language}
        code as is.
        
        Just return the formatted code (with correct indentation preserved) as a JSON. Remember not to
        provide boilerplate text, no explanation, no unnecessary text to explain the output, not even
        the 'Here is the response'.
        
        Here is the template for JSON response:
        
            "audio_transcript": <Original Audio Transcript>,
            "coding_language": <Coding Language>,
            "formatted_code": <Formatted Code as a String in a single line with escape characters>
        """

    response = model.invoke(prompt)
    print(response.content)
    return json.loads(response.content)
