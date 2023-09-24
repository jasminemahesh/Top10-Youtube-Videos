from flask import Flask, render_template_string, jsonify, request
import pandas as pd
import csv
from googleapiclient.discovery import build

app = Flask(__name__)

def get_youtube_handle(API_KEY, API_VERSION, API_SERVICE_NAME):
    youtube_handle = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
    return youtube_handle

def get_top10_videos_with_highest_Comments(topic):
    API_KEY = ''
    API_VERSION = 'v3'
    API_SERVICE_NAME = 'youtube'
    # Build the YouTube API client
    youtube = get_youtube_handle(API_KEY, API_VERSION, API_SERVICE_NAME)
    
    #get first 50 videos
    search_response_top_50 = youtube.search().list(
    q=topic,
    type='video',
    part='id,snippet',
    maxResults=50,
    regionCode='US',
    order='relevance'
    ).execute()
    
    print("overall list")
    print(search_response_top_50)
    
    #write the video stats like no of comments, likes, views to the file
    with open('video_stats.csv', mode='w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Video ID', 'Title','No of Views', 'No of Likes', 'No of Comments', 'Youtube Url'])

        for item in search_response_top_50['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            
            # Construct the video link
            video_link = f'https://www.youtube.com/watch?v={video_id}'

            video_response = youtube.videos().list(
            part='statistics',
            id=video_id
            ).execute()

            print("video_response:", video_response)
            for item in video_response['items']:
                video_no_of_views = item['statistics'].get('viewCount', 0)
                video_no_of_likes = item['statistics'].get('likeCount', 0)
                video_no_of_comments = item['statistics'].get('commentCount', 0)
                writer.writerow([video_id,video_title,video_no_of_views,video_no_of_likes,video_no_of_comments, video_link])

    
    #read csv file generated above in pandas dataframe
    df = pd.read_csv('video_stats.csv',encoding='ISO-8859-1')

    # Sort the DataFrame by comment count in descending order
    df = df.sort_values(by='No of Comments', ascending=False)

    #get top 10 videos by comments
    df = df.head(10)

    print(df)
    # Get the IDs and titles from the DataFrame
    video_ids = df.iloc[:, 0].tolist()
    video_titles = df.iloc[:, 1].tolist()
    video_comments = df.iloc[:, 4].tolist()
    video_youtube_url = df.iloc[:, 5].tolist()

    video_data_list = []
        # Retrieve the snippet data for the top 10 videos
    if len(video_titles) == len(video_comments):
        for i in range(len(video_titles)):
            video_data_list.append({"Video Title": video_titles[i], "Comments": video_comments[i], "Youtube Url": video_youtube_url[i]})
    else:
        print("The number of video titles does not match the number of comments.")
    
    #print(video_data_list)

    template = """<!DOCTYPE html><html><head><title>Video Data</title></head><body><h1>Video Data</h1><ul>{% for video in video_data_list %}<li><strong>Video Title:</strong>{{ video["Video Title"] }}<br><strong>Comments:</strong> {{ video["Comments"] }}<br><strong>YouTube Url:</strong> <a href="{{ video["Youtube Url"] }}" target="_blank">{{ video["Youtube Url"] }}</a></li>{% endfor %}</ul></body></html>"""
	
    html_content = render_template_string(template, video_data_list=video_data_list)
    html = html_content.strip('"')
    return html, 200, {'Content-Type': 'text/html'}

from flask import Flask, render_template, request

app = Flask(__name__)

# Define a simple HTML form
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Enter Topic</title>
</head>
<body>
    <h1>Enter a Topic</h1>
    <form method="POST" action="/get_top10_videos">
        <label for="topic">Topic:</label>
        <input type="text" id="topic" name="topic" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

# Create a route to display the form
@app.route('/')
def index():
    return form_html


@app.route('/get_top10_videos', methods=['POST'])
def get_top10_videos():
    # Call your function here
    topic = request.form['topic']
    top_10_videos = get_top10_videos_with_highest_Comments(topic)
    return top_10_videos

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)