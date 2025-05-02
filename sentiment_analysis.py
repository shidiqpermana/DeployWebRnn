from googleapiclient.discovery import build
from textblob import TextBlob
import time
import csv

API_KEY = 'AIzaSyDedWfbZ2u2rpbO5R_Ka15jvhjdwooyDN8'

def get_comments_data(video_id, max_total=10000):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    comments = []
    request = youtube.commentThreads().list(
        part="snippet,replies", videoId=video_id,
        maxResults=100, textFormat="plainText"
    )
    response = request.execute()

    while request is not None and len(comments) < max_total:
        for item in response['items']:
            top_comment = item['snippet']['topLevelComment']['snippet']
            comments.append(top_comment['textDisplay'])

        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
            time.sleep(0.5)
        else:
            break

    save_comments_to_csv(comments)
    return comments

def save_comments_to_csv(comments, filename='youtube_comments.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['comment', 'positive', 'neutral', 'negative'])  # Header with sentiment columns
        for comment in comments:
            sentiment = analyze_sentiment(comment)  # Analyze sentiment for each comment
            # Mark the sentiment in the appropriate column
            writer.writerow([comment, 1 if sentiment == 'positive' else 0, 1 if sentiment == 'neutral' else 0, 1 if sentiment == 'negative' else 0])

def analyze_sentiment(comment):
    blob = TextBlob(comment)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

def analyze_sentiments(comments):
    categorized = {'positive': 0, 'neutral': 0, 'negative': 0}
    detailed = []

    for comment in comments:
        sentiment = analyze_sentiment(comment)
        categorized[sentiment] += 1
        detailed.append({'text': comment, 'sentiment': sentiment})

    return {'summary': categorized, 'details': detailed}
