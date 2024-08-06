from database import database_func


# This is a placeholder for the LLM model. It should be replaced with the actual model.
def llm_model(prompt: str) -> str:
    return "This is a placeholder for the LLM model. It should be replaced with the actual model." + prompt


# This is a placeholder for the video_summery function. It should be replaced with the actual function.
def video_summary(lecture_num: int, week_num: int) -> str:
    data = database_func(lecture_num, week_num)
    summary: str = llm_model(data)
    return "Scaffolding from video_summery function" + summary
