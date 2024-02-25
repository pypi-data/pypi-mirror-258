# digestvid

digestvid is a Python tool designed to automatically transcribe, review, and summarize video content, making it easier to digest video content efficiently. It supports processing both local video files and YouTube videos by downloading them. The tool utilizes advanced AI models for transcription and summarization.

## Features

- Transcribe audio from videos to text
- Summarize transcribed text into concise summaries
- Download YouTube videos for processing
- Extract and summarize specific chapters or sections of videos

## Installation

To install digestvid, you will need Python 3.6 or later. It's recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, you can install DigestVid using pip:

```bash
pip install git+https://github.com/AI-Sherpa/DigestVid.git
```

## Usage

After installation, you can use DigestVid from the command line to process a local video file or a YouTube URL:

```bash
digestvid <path to video file or YouTube URL>
```

## Examples

To process a local video file:

```bash
digestvid path/to/video.mp4
```

To download and process a YouTube video:

```bash
digestvid https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Contributing

Contributions to digestvid are welcome! Here are a few ways you can help:

- Report bugs and request features by creating issues.
- Contribute to the code via pull requests. Please read our contribution guidelines first.

## License

digestvid is released under the MIT License. See the LICENSE file for more details.