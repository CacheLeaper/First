import os
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# 1. Setup Authentication (Requires OAuth 2.0 Client ID)
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)

def check_and_comment(youtube, channel_id):
    # 2. Get the latest video from a specific channel
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        order="date",
        type="video",
        maxResults=1
    )
    response = request.execute()
    
    if response['items']:
        latest_video_id = response['items'][0]['id']['videoId']
        print(f"New video found: {latest_video_id}. Attempting to comment...")
        youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": latest_video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": "first"
                        }
                    }
                }
            }
        ).execute()

# Note: This is a simplified logic map; a real script requires loops and error handling.
