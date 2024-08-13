import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import json

os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(temperature=0.8, model="llama3-8b-8192")

def get_translation(source_text, target_language):
    prompt = f"""
        You are given a piece of source text in English that needs to be translated to {target_language}. Make sure the meaning is not lost during the translation. If there certain domain specific words, like 'def' keyword in Python language, leave them in English.
        Here is the piece of text in English that needs to be translated to {target_language}:
        "{source_text}"
        
        Just return the translation as a JSON. Remember not to provide boilerplate text, no explanation, no unnecessary text to explain the output.
        
        Here is the template for JSON response:
            "source_text": <Source Text>,
            "target_language": <Target Language>,
            "translated_text": <Translated Text>
        """
    
    response = model.invoke(prompt)
    print(response.content)
    return json.loads(response.content)