import argparse
import os
import shutil

import yt_dlp


def format_video(ctx):
    """Select the best video and the best audio that won't result in an mkv.

    Args:
        ctx (dict): The context dictionary containing format information.

    Yields:
        dict: A dictionary containing the merged format details.
    """
    # formats are already sorted worst to best
    formats = ctx.get("formats")[::-1]

    # acodec='none' means there is no audio
    best_video = next(
        f for f in formats if f["vcodec"] != "none" and f["acodec"] == "none"
    )

    # find compatible audio extension
    audio_ext = {"mp4": "m4a", "webm": "webm"}[best_video["ext"]]
    # vcodec='none' means there is no video
    best_audio = next(
        f
        for f in formats
        if (f["acodec"] != "none" and f["vcodec"] == "none" and f["ext"] == audio_ext)
    )

    # These are the minimum required fields for a merged format
    yield {
        "format_id": f'{best_video["format_id"]}+{best_audio["format_id"]}',
        "ext": best_video["ext"],
        "requested_formats": [best_video, best_audio],
        # Must be + separated list of protocols
        "protocol": f'{best_video["protocol"]}+{best_audio["protocol"]}',
    }


ydl_audio_m4a = {
    "format": "m4a/bestaudio/best",
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }
    ],
}


def main(input_file, output_folder):
    """Download videos from a list of URLs.

    Args:
        input_file (str): Path to the text file containing the URLs.
        output_folder (str): Folder to save the downloaded videos.
    """
    with open(input_file, "r") as file:
        urls = file.read().splitlines()

    # Delete the output folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_audio_m4a) as ydl:
        error_code = ydl.download(urls)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download videos from a list of URLs")
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
        help="Folder to save the downloaded videos (default: download)",
    )

    args = parser.parse_args()
    main(args.input_file, args.output_folder)
