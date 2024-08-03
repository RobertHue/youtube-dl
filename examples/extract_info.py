import json
import yt_dlp
from pprint import pprint

URL = 'https://www.youtube.com/watch?v=BaW_jenozKc'

# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # ℹ️ ydl.sanitize_info makes the info json-serializable
    json_info = json.dumps(ydl.sanitize_info(info))
    pprint(json_info)
    
    title = info['title']
    print(f'Title: {title}') 