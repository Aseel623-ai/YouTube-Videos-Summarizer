import sys
import re
import requests
import time
import random
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, VideoUnavailable, NoTranscriptFound



def extract_video_id(url):
    if not url:
        return None
    
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    match = re.search(r'v=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    return None



def extract_metadata(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, features='html.parser')
        title = soup.find('title').text
        return title
    
    except requests.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return None
        


def download_thumbnail(video_id):
    if not video_id:
        return None
    
    try:
        image_url = f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'
        img_data = requests.get(image_url).content
        with open('thumbnail.jpg', 'wb') as handler:
            handler.write(img_data)
    except VideoUnavailable:
        return None        
        
      
def get_transcript(video_id):
    if not video_id:
        return None
    
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_fetched = ytt_api.fetch(video_id=video_id, languages=['en'])
        transcript_raw = transcript_fetched.to_raw_data()
        return ' '.join([i['text'] for i in transcript_raw])
        
    except VideoUnavailable:
        print(f'{video_id} is unavailable')
        return None
        
    except NoTranscriptFound:
        print('no transcript found!')
        return None
        
             