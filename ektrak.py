import re

def extract_video_id(url):
    pattern = r"(?:https?://(?:www\.)?youtube\.com(?:/[^/]+)?\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# Contoh penggunaan
url = "https://www.youtube.com/live/mOecqXrYvfw?si=Rz7XGh8JOzRVH7UV"
video_id = extract_video_id(url)
print(video_id)  # Output: dQw4w9WgXcQ
