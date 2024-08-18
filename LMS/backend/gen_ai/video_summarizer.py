import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import YoutubeLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
import json

os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(temperature=0.8, model="llama3-8b-8192")

def get_video_summary(course, lesson):
    prompt_template = f"""
        You are given the transcript of a video lesson on the topic {lesson.lesson_name} for the course
        {course.course_name}. Summarize the video content in a concise manner in about 100 words
        highlighting any specific computer science functions or concepts. You can breakdown the summary
        into multiple paragraphs, or even list down 5-10 quick key points for revising the concept under
        the heading 'Quick Key Points'.
        """
    prompt_template += """
        Here is the video transcript:
        "{text}"
        
        Just return the summary as a JSON, and make sure you use the word 'video' and not 'text' in the
        summary.
        
        Template for JSON response:
            "summary": <Concise Summary>,
            "key_points": [<Key Point 1>, <Key Point 2>, ...]
            
        Remember not to provide boilerplate text, no explanation, no unnecessary text like 'Here is the
        JSON response' to explain the output.
        """
    
    prompt = PromptTemplate.from_template(prompt_template)

    loader = YoutubeLoader.from_youtube_url(lesson.video_url)
    docs = loader.load()

    chain = load_summarize_chain(model, chain_type="stuff", prompt=prompt)
    response = chain.invoke(docs)
    
    print(response['output_text'])
    return json.loads(response['output_text'])