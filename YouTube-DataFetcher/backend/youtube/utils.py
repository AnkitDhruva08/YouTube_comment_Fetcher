#  extrac video id 
import re
def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    Supports URLs like:
    https://www.youtube.com/watch?v=VIDEO_ID
    https://youtube.com/watch?v=VIDEO_ID
    https://www.youtube.com/v/VIDEO_ID
    """
    video_id = None
    youtube_url_pattern = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'

    match = re.match(youtube_url_pattern, url)
    if match:
        video_id = match.group(1)  # Extract the video ID from the URL
    else:
        print("Invalid YouTube URL format.")
    
    return video_id
