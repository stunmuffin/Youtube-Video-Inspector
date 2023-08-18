from flask import Flask, render_template, request
from googleapiclient.discovery import build

app = Flask(__name__)

def get_authenticated_service(api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube

def get_video_info(youtube, video_id):
    response = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
    if 'items' in response and response['items']:
        video_data = response['items'][0]
        channel_id = video_data['snippet']['channelId']
        
        channel_response = youtube.channels().list(part='snippet', id=channel_id).execute()
        if 'items' in channel_response and channel_response['items']:
            channel_info = channel_response['items'][0]
            return video_data, channel_info
    return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        api_key = request.form['api_key']
        video_id = request.form['video_id']
        
        youtube = get_authenticated_service(api_key)
        video_info, channel_info = get_video_info(youtube, video_id)

        if video_info and channel_info:
            snippet = video_info['snippet']
            statistics = video_info['statistics']

            return render_template('index.html', video_info=video_info, snippet=snippet, statistics=statistics, channel_info=channel_info)
        else:
            return "Video not found or API quota exceeded."

    return render_template('index.html', video_info=None, snippet=None, statistics=None, channel_info=None)

if __name__ == '__main__':
    app.run(debug=True)
