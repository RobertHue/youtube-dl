import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs

def extract_video_ids_from_urls(urls):
    video_ids = []
    for url in urls:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            video_ids.append(query_params['v'][0])
    return video_ids

def get_video_title(url):
    result = subprocess.run(['yt-dlp', '--get-title', url], capture_output=True, text=True)
    return result.stdout.strip()


def download_video(url, output_folder):
    video_title = get_video_title(url)
    output_path = os.path.join(output_folder, f'{video_title}.mp4')
    subprocess.run(['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', '-o', output_path, url])
  

def download_audio(url, output_folder):
    video_title = get_video_title(url)
    output_path = os.path.join(output_folder, f'{video_title}.mp3')
    subprocess.run(['yt-dlp', '-f', 'bestaudio[ext=m3a]/mp3', '-o', output_path, url])
            
            
            
def download(urls, output_folder, strategy=download_video): 
    with ThreadPoolExecutor() as executor:
        for url in urls:
            executor.submit(strategy, url, output_folder)


def main():
    file_path = "urls.txt"  # Path to the text file containing the URLs
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    
    output_folder = "downloaded_videos"
    # Delete the output folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist
    download_videos(urls, output_folder)


if __name__ == "__main__":
    main()
