from googleapiclient.discovery import build 
import re 
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_scores(comment, polarity):
    sentiment_object = SentimentIntensityAnalyzer()
    sentiment_dict = sentiment_object.polarity_scores(comment)
    polarity.append(sentiment_dict['compound'])
    return polarity

API_KEY = 'AIzaSyCl6YnUwPwKSx7yqq-5Fsxxxxxxxxxxxxx'
def get_input(url):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video_id = url[-11:]
    print("video id: " + video_id)

    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    video_snippet = video_response['items'][0]['snippet']
    uploader_channel_id = video_snippet['channelId']
    comments = []
    nextPageToken = None
    while len(comments) < 600:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,  # You can fetch up to 100 comments per request
            pageToken=nextPageToken
        )
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            # Check if the comment is not from the video uploader
            if comment['authorChannelId']['value'] != uploader_channel_id:
                comments.append(comment['textDisplay'])
        nextPageToken = response.get('nextPageToken')
    
        if not nextPageToken:
            break
    hyperlink_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    threshold_ratio = 0.65
    relevant_comments = []
    for comment_text in comments:
        comment_text = comment_text.lower().strip()
        emojis = emoji.emoji_count(comment_text)
        text_characters = len(re.sub(r'\s', '', comment_text))
        if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
            if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
                relevant_comments.append(comment_text)
    f = open("ytcomments.txt", 'w', encoding='utf-8')
    for idx, comment in enumerate(relevant_comments):
        f.write(str(comment)+"\n")
    f.close()
    polarity = []
    positive_comments = []
    negative_comments = []
    neutral_comments = []

    f = open("ytcomments.txt", 'r', encoding='`utf-8')
    comments = f.readlines()
    f.close()
    for index, items in enumerate(comments):
        polarity = sentiment_scores(items, polarity)
        if polarity[-1] > 0.05:
            positive_comments.append(items)
        elif polarity[-1] < -0.05:
            negative_comments.append(items)
        else:
            neutral_comments.append(items)
    avg_polarity = sum(polarity)/len(polarity)
    if avg_polarity > 0.05:
        return "The Video has got a Positive response",avg_polarity
    elif avg_polarity < -0.05:
        return "The Video has got a Negative response",avg_polarity
    else:
        return "The Video has got a Neutral response",avg_polarity
