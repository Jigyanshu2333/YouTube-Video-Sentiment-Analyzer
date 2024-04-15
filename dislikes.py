from googleapiclient.discovery import build 
import re 
API_KEY = 'AIzaSyCl6YnUwPwKSx7yqq-5FsFlIZBBLZ6Gv8o'
def get_input(url):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video_id = url[-11:]

    request = youtube.videos().list(
        part='statistics',
        id=video_id
    )
    response = request.execute()
    if 'items' in response:
        stats = response['items'][0]['statistics']
        dislikes = int(stats['dislikeCount']) if 'dislikeCount' in stats else None
        return dislikes
    else:
        return None