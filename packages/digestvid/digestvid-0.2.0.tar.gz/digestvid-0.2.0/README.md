# digestvid

`digestvid` is a Python package designed to automate the transcription, summarization, and processing of video content. It supports both local video files and YouTube videos, leveraging advanced AI models for accurate transcription and concise summarization. With `digestvid`, users can efficiently digest video content, making it an ideal tool for content creators, educators, and researchers.

## Features

- **Transcribe Audio from Videos**: Converts spoken words in videos into text using the Whisper model.
- **Summarize Transcribed Text**: Generates concise summaries from transcribed text using OpenAI's powerful models.
- **YouTube Video Support**: Downloads YouTube videos for processing, including handling videos with chapters.
- **Video Screenshot Capture**: Automatically captures and saves a screenshot from the midpoint of a video.
- **Flexible Output Management**: Saves transcriptions, summaries, and screenshots in user-specified directories, with support for filename sanitization.

## Installation

Ensure you have Python 3.6 or later installed. It's recommended to use a virtual environment for installation:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install `digestvid` using pip:

```bash
pip install git+https://github.com/AI-Sherpa/DigestVid.git
```

## Usage

After installation, `digestvid` can be used from the command line to process either a local video file or a YouTube URL:

```bash
digestvid <path to video file or YouTube URL>
```

### Examples

Process a local video file:

```bash
digestvid path/to/video.mp4
```

Download and process a YouTube video:

```bash
digestvid https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Contributing

Contributions to `digestvid` are welcome! You can contribute by reporting bugs, requesting features, or submitting pull requests. Please read our contribution guidelines for more information.

## License

`digestvid` is released under the MIT License. See the LICENSE file for more details.