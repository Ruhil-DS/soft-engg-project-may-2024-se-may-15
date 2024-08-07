import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

# This is my personal API key, need to remove it from the code later
os.environ['GOOGLE_API_KEY'] = "AIzaSyBl_AiZVeYjCyekAkdVeL26yV3_yPektJo"

# chat object for our LLM; to be used throughout
# Temperature defines the randomness
chat_model = ChatGoogleGenerativeAI(temperature=0.0, model='gemini-pro')


def code_error_explanation(chat_model=chat_model, code_block: str=None) -> str:
    """
    This function will help explain the error in the code block using the LLM.
    :param code_block: the code block that contains the error.
    :return: a string containing the explanation of the error in the code block.
    """
    # string template text for getting the output. Here, we define variables using {}
    error_explain_template = """You are coding expert, who knows all sorts of computer languages. \
    You can identify the language and the errors very quickly in any code block. \
    As a god programmer, you are asked to explain the error in the code block in a detailed manner. \
    You are really good with explaining the error in detail and in simple terms.
    If there is no error, you simply say "no error" and nothing else. But if there is an error, \
    you give a very detailed explanation of what went wrong with the code block. at least 25 words \
    for small errors and at least 50 words for large errors. \ 
    The code block is as follows: {code_block_input} \
    
    The output should be formatted in a way that it can be parsed as a json. The entire output \
    should be in a json format and no boilerplate text is required outside of the json structure. \
    Follow the following JSON structure by using the following keys. Value will be the explanation \
    that was asked to you for the error in the code block: 
    line_x: the line number of the error. Here, x denotes the line number. \
    
    Again, remember not to provide boilerplate text, no explanation, no unnecessary text \
    to explain the output. \
    and directly the json formatted data.
    """
    # converting it to langchain supportive prompt template
    prompt_template = ChatPromptTemplate.from_template(error_explain_template)

    # final prompt with the variable values inputted
    final_input_prompt = prompt_template.format_messages(code_block_input=code_block)

    # getting the response from the LLM model
    response = chat_model.invoke(final_input_prompt)

    # returning the content of the response from the LLM model
    return response.content


if __name__ == '__main__':
    sample_code = """
    print(Hello World)
    """
    print(code_error_explanation(chat_model, code_block=sample_code))