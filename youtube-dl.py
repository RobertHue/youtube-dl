import argparse
import os
import shutil
import logging
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


def main(input_file, output_folder, strategy):
    """Download videos or audios from a list of URLs based on the selected strategy.

    Args:
        input_file (str): Path to the text file containing the URLs.
        output_folder (str): Folder to save the downloaded videos or audios.
        strategy (str): The download strategy ('audio' or 'video').
    """
    try:
        with open(input_file, "r") as file:
            urls = file.read().splitlines()
    except FileNotFoundError:
        logging.error(f"Input file {input_file} not found.")
        return

    # Delete the output folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = ydl_audio_m4a if strategy == "audio" else ydl_video_best

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)


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

    args = parser.parse_args()
    main(args.input_file, args.output_folder, args.strategy)
