from flask import Flask, jsonify, request
from llm import video_summery

app = Flask(__name__)


# This endpoint can be used to check if the server is running. Returns a JSON object with a message.
@app.route('/test/')
def home():
    return jsonify({"message": "Hello Vue!"})


# Request should have lecture_num and week_num. Gets <that thing from below the vid> from database. Queries the LLM model to expand the summary and returns the expanded summary.
@app.route('/summary/video/', methods=['POST'])
def summary_lecture():
    if request.method == 'POST':
        data = request.get_json()
        lecture_num: int = data['lecture_num']
        week_num: int = data['week_num']
        summary: str = "Week Num:" + str(week_num) + "Lecture Num:" + str(lecture_num) + video_summery(lecture_num, week_num)
        return jsonify({"summary": summary})
    else:
        return jsonify({"summary": "Default summery :)"})


if __name__ == '__main__':
    app.run(debug=True)
