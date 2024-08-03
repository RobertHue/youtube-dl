# youtube-dl

This script is a wrapper for [yt-dlp](https://github.com/yt-dlp/yt-dlp), designed to download audio or video from provided URLs.

## Features

- **Audio Download**: Default mode downloads the best audio available in `.m4a` format.
- **Video Download**: Optionally, you can download the best available video in `.mp4` format.

## Table of Contents

- [youtube-dl](#youtube-dl)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command-Line Arguments](#command-line-arguments)
    - [Example](#example)

## Installation

- [Git](https://git-scm.com/downloads)
- [VSCode](https://code.visualstudio.com/)
- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

To install Poetry, follow these steps:

   ```sh
   python -m pip install --upgrade pip
   python -m pip install --user pipx
   python -m pipx ensurepath
   pipx install poetry
   ```

To install the project dependencies, execute the following command:

   ```sh
   poetry install
   ```

To activate the virtual environment, run:

   ```sh
   poetry shell
   ```

## Usage

To use the script, you can specify the input file containing URLs and the output folder. Additionally, you can choose between downloading audio or video.

### Command-Line Arguments

For command line arguments, use:

  ```sh
  python video2images.py --help
  ```

- `--input_file` (default: `urls.txt`): Path to the text file containing the URLs to download.
- `--output_folder` (default: `download`): Directory to save the downloaded files.
- `--strategy` (choices: `audio`, `video`; default: `audio`): Specify the download strategy. Use `audio` to download audio files or `video` to download video files.
- `--concurrent_fragments` (default: `4`): Number of concurrent fragments to download for each video.

### Example

To download video from the URLs listed in `urls.txt`:

```sh
python youtube-dl.py --strategy=video
```

By default, this command will create a folder named `download`.
