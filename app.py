from flask import Flask, render_template, request, jsonify
from sentiment_analysis import analyze_sentiments, get_comments_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_id = request.form['video_id']
    comments = get_comments_data(video_id)
    results = analyze_sentiments(comments)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
