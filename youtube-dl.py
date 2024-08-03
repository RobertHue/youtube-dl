import argparse
import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

import yt_dlp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

ydl_audio_best = {
    "format": "m4a/bestaudio/best",
    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}],
}

ydl_video_best = {
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
}


def download_url(url, ydl_opts):
    """Download a single URL using the specified yt_dlp options."""
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.info(f"Successfully downloaded: {url}")
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")


def main(input_file, output_folder, strategy, concurrent_fragments):
    """Download videos or audios from a list of URLs based on the selected strategy.

    Args:
        input_file (str): Path to the text file containing the URLs.
        output_folder (str): Folder to save the downloaded videos or audios.
        strategy (str): The download strategy ('audio' or 'video').
        concurrent_fragments (int): Number of concurrent fragments to use for downloading.
    """
    try:
        with open(input_file, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"Input file {input_file} not found.")
        return

    if not urls:
        logging.error("No valid URLs found in the input file.")
        return

    # Delete the output folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = ydl_audio_best if strategy == "audio" else ydl_video_best
    ydl_opts["outtmpl"] = os.path.join(output_folder, "%(title)s.%(ext)s")
    ydl_opts["concurrent_fragment_downloads"] = concurrent_fragments

    # Use ThreadPoolExecutor for concurrent downloads
    with ThreadPoolExecutor(max_workers=concurrent_fragments) as executor:
        futures = [executor.submit(download_url, url, ydl_opts) for url in urls]
        for future in as_completed(futures):
            try:
                future.result()  # Check if the download was successful
            except Exception as e:
                logging.error(f"Error in concurrent execution: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download videos or audios from a list of URLs"
    )
    parser.add_argument(
        "--input_file",
        type=str,
        default="urls.txt",
        help="Path to the text file containing the URLs (default: urls.txt)",
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        default="download",
        help="Folder to save the downloaded videos or audios (default: download)",
    )
    parser.add_argument(
        "--strategy",
        type=str,
        choices=["audio", "video"],
        default="audio",
        help="Download strategy: 'audio' to extract audio only, 'video' to download the best video with audio (default: audio)",
    )
    parser.add_argument(
        "--concurrent_fragments",
        type=int,
        default=4,
        help="Number of concurrent fragments to use for downloading (default: 4)",
    )

    args = parser.parse_args()
    main(args.input_file, args.output_folder, args.strategy, args.concurrent_fragments)
