import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
import gdown
import json

os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(temperature=0.8, model="llama3-8b-8192")

def download_slide(file_id):
    download_url = f'https://drive.google.com/uc?id={file_id}'
    output = f'downloads/{file_id}.pdf'
    gdown.download(download_url, output, quiet=False)
    
    print(f"Downloaded file: {output}")


def get_slide_summary(course, lesson):
    prompt_template = f"""
        You are given the slides as a PDF used by an instructor to teach the topic {lesson.lesson_name}
        for the course {course.course_name}. Summarize the document content in a concise manner in about
        100 words, highlighting any specific computer science functions or concepts. You can breakdown the summary into multiple paragraphs, or even list down 5-10 quick key points for revising the concept under the heading 'Quick Key Points'.
        """
    prompt_template += """
        Here is the slide content:
        "{text}"
        
        Just return the summary as a JSON, and make sure you use the word 'slide' and not 'text' in the
        summary.
        
        Remember not to provide boilerplate text, no explanation, no unnecessary text to explain the
        output.
        
        Here is the template for JSON response:
            "summary": <Concise Summary>,
            "key_points": [<Key Point 1>, <Key Point 2>, ...]
            
        Do not return an extra text like 'Here is the response' apart from JSON.
        """
    
    prompt = PromptTemplate.from_template(prompt_template)

    file_id = lesson.slide_url.split('/d/')[1].split('/')[0]
    
    if not os.path.exists(f"downloads/{file_id}.pdf"):
        download_slide(file_id)
    
    loader = PyPDFLoader(f"downloads/{file_id}.pdf")
    docs = loader.load()

    chain = load_summarize_chain(model, chain_type="stuff", prompt=prompt)
    response = chain.invoke(docs)
    
    return json.loads(response['output_text'])