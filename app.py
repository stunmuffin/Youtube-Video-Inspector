from flask import Flask, render_template, request
from googleapiclient.discovery import build

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        api_key = request.form['api_key']
        video_id = request.form['video_id']
        
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
        
        if 'items' in response and response['items']:
            video_info = response['items'][0]
            snippet = video_info['snippet']
            statistics = video_info['statistics']

            return render_template('index.html', video_info=video_info, snippet=snippet, statistics=statistics)
        else:
            return "Video not found or API quota exceeded."

    return render_template('index.html', video_info=None, snippet=None, statistics=None)

if __name__ == '__main__':
    app.run(debug=True)
