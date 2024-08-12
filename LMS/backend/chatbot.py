import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

os.environ['GROQ_API_KEY'] = "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"
model = ChatGroq(temperature=1.0, model="llama3-8b-8192")

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)


class Chatbot:
    def __init__(self, course, knowledge=None):
        self.config = {"configurable": {"session_id": course['course_id']}}
        self.course = course
        self.setup()
        if knowledge:
            self.update_knowledge(knowledge)
    
    def setup(self):
        with_message_history.invoke(
            [
                SystemMessage(content=f"""You are a helpful assistant for the subject '{self.course['course_name']}' that is being taught through a Learner Management System (LMS) portal called 'SEEK++'. Your name is 'pushPAK' which is an abbreviation for 'pushing Pupils to Attain Knowledge'. Your task is to quickly answer queries of students regarding the course, including deadline of assignments, dates of quizzes and more.
                              
                On the portal, for one course there are multiple modules, and each module has multiple lessons. Each lesson has some content, a video lecture, and a slide deck. There are 4 types of assignments on the portal: PA (Practice Theory Assignment with MCQs), GA (Graded Theory Assignment with MCQs), PrPA (Practice Programming Assignment), and GrPA (Graded Programming Assignment).
                
                The 'SEEK++' is an advanced LMS portal with integrated GenAI features. The portal has a summarizer to summarize the contents of the videos as well as slides into short notes which can also be translated to the student's native language. There is a feature to generate as many practice assignments (both theory and programming) as a student wants. There is a feature to detect learning pain points of a student and suggest a corresponding revision plan for the quizzes. During coding, there are features to provide help and even provide feedback and tips based on the student's response on the assignments. There is also an inclusivity feature that allows a student with limited motor skills to speak the code and portal will format the code accordingly. Finally, there is also a friendly assistant, which is you, for quick queries of students.
                              
                You should provide friendly responses and should act like a mentor to whom students are open to share their problems and discuss solutions. You should not give direct solutions to problems but rather motivate them and nudge them to think and learn themselves."""),
            ],
            config=self.config
        )
        
    def update_knowledge(self, knowledge):
        with_message_history.invoke(
            [
                SystemMessage(content=knowledge)
            ],
            config=self.config
        )

    def query(self, query):
        response = with_message_history.invoke(
            [
                HumanMessage(content=query)
            ],
            config=self.config
        )
    
        return response.content


if __name__ == "__main__":
    pwpcb = Chatbot({"course_id": "BSCS1002", "course_name": "Programming with Python"})
    print(pwpcb.query("Can you write a function that returns the factorial of a number?"))
    print(pwpcb.query("I am still stuck!"))
    print(pwpcb.query("What is the deadline for GrPA 8?"))