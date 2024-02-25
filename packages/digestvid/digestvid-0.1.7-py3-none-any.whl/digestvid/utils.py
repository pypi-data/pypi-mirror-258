
import argparse
from moviepy.editor import VideoFileClip
from pathlib import Path
import logging
import whisper
from openai import OpenAI
from digestvid.config_loader import load_api_key
import re
import yt_dlp
import subprocess
import textwrap
import webbrowser
import tempfile
import os

# Define a mutable global variable
video_output_dir = {"path": None}

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize dedicated_output_dir at a higher scope, ensuring it's always a Path object
dedicated_output_dir = Path.home() / ".DigestVid"  # Default initialization

def capture_video_screenshot(video_path, output_dir):
    """
    Captures a screenshot from the midpoint of the video and saves it as an image.
    Returns the path to the saved image.
    """
    with VideoFileClip(str(video_path)) as video:
        # Calculate the midpoint of the video
        midpoint = video.duration / 2
        # Construct the image file path
        image_path = output_dir / f"{video_path.stem}_screenshot.png"
        # Save the frame as an image at the midpoint
        video.save_frame(str(image_path), t=midpoint)
        return image_path


def get_video_screenshot(summary_file):
    """
    Given a summary file, finds the corresponding video file, captures a screenshot,
    and returns the path to the screenshot image.
    """
    # Replace '_summary.txt' with '.mp4' to get the video file name
    video_filename = summary_file.name.replace('_summary.txt', '.mp4')
    video_path = summary_file.parent / video_filename
    # Capture and save the screenshot
    screenshot_path = capture_video_screenshot(video_path, summary_file.parent)
    return screenshot_path  # Converts the path to a URI that can be used in the HTML

def create_summary_prompt(text):
    """
    Prepares a prompt for the AI summarizer.
    """
    instruction = (
        "You are an expert AI summarizer. Review the content given to you, "
        "take your time to tease out the salient points and all the examples provided "
        "to explain the concepts articulated clearly and concisely, in bullet points where necessary."
        "Here is the content:\n\n"
    )
    prompt = instruction + text
    return prompt

def transcribe_audio(audio_path):
    """
    Transcribes audio to text using Whisper.
    """
    model = whisper.load_model("base")
    #model = whisper_metal.load_model("large")
    result = model.transcribe(str(audio_path))
    return result['text']

def summarize_with_openai(text):
    """
    Generates a summary for the given text using OpenAI's chat-based model.
    """
    openai_api_key = load_api_key()
    client = OpenAI(
        base_url="http://localhost:11434/v1", #Ollama by default, comment out to use OpenAI
        api_key=openai_api_key
    )
    prompt = create_summary_prompt(text)
    response = client.chat.completions.create(
        model="aisherpa/mistral-7b-instruct-v02:Q5_K_M", #Ollama by default, replace with "gpt-4" for OpenAI
        max_tokens=1024,
        temperature=0.1,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content 



def sanitize_filename(filename, max_length=50):
    """
    Sanitizes the filename to avoid path issues and limits its length.
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = sanitized.replace('%', '_').replace('.', '_').replace(' ', '_')
    return sanitized[:max_length]
def get_video_path(summary_file):
    """
    Given a summary file, finds the corresponding video file and returns the Path object.
    """
    video_filename = summary_file.name.replace('_summary.txt', '.mp4')
    return summary_file.parent / video_filename  # This returns a Path object

def get_video_title(url):
    """
    Fetches the video title using yt-dlp.
    """
    cmd = ['yt-dlp', '--get-title', url]
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        title = result.stdout.strip()
        return title
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while fetching the video title: {e}")
        return None

def download_youtube_video(url, output_dir):
    """
    Downloads a YouTube video by chapters to a dedicated subfolder within the specified directory using yt-dlp via command line, if chapters are available.
    If the video does not contain chapters, downloads the entire video as a single file.
    Returns a list of paths to the downloaded chapter files or the single video file.
    """
    video_title = get_video_title(url)
    if video_title is None:
        logger.error("Failed to fetch video title. Cannot proceed with download.")
        return []

    sanitized_title = sanitize_filename(video_title)
    dedicated_output_dir = output_dir / sanitized_title
    video_output_dir["path"] = dedicated_output_dir

    print("download_youtube_video: Video Output Dir")
    print(video_output_dir["path"])
    dedicated_output_dir.mkdir(parents=True, exist_ok=True)

    # Define the output template for yt-dlp
    output_template = str(dedicated_output_dir / f'{sanitized_title}_%(chapter_number)s_%(chapter)s.%(ext)s')
    cmd = [
        'yt-dlp',
        url,
        '--output', output_template,
        '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        '--split-chapters',
        '--no-keep-video',
        '--postprocessor-args', '-metadata:s:a:0 language=eng'
    ]

    try:
        subprocess.run(cmd, check=True, cwd=str(dedicated_output_dir))
        logger.info(f"Video downloaded successfully to {dedicated_output_dir}")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while downloading the video: {e}")
        return []

    # Initially, list all MP4 files
    print("Listing all files in the dedicated_output_dir:")
    for file in dedicated_output_dir.iterdir():
        if file.is_file():
            print(file.name)
    all_mp4_files = list(dedicated_output_dir.glob('*.mp4'))
    print("all_mp4_files:")
    for file in all_mp4_files:
        print(file,"\n")

    # Assuming all_mp4_files is already populated with Path objects of .mp4 files in dedicated_output_dir

    # Step 1: Attempt to filter for chapter files
    chapter_files = [file for file in all_mp4_files if re.search(r' - (\d{3}) ', file.name)]

    # Step 2: If no chapter files are found, filter for "_NA_NA" files
    if not chapter_files:
        chapter_files = [file for file in all_mp4_files if "_NA_NA.mp4" in file.name]

    # Now chapter_files will contain either chapter files if available, or "_NA_NA" files if no chapter files were found

    if not chapter_files:
        logger.error("No relevant video files found. Please check the download.")
        return []

    print("digestvi.utils: Chapter files: ",chapter_files)
    return chapter_files



def is_youtube_url(url):
    """
    Checks if the provided URL is a valid YouTube URL.
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return True
    return False

def extract_and_summarize(video_path, output_dir=None):
    """
    Extracts speech from the video, summarizes it, and writes the transcript.
    """
    video_path = Path(video_path)
    if output_dir is None:
        output_dir = video_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    audio_filename = video_path.stem + ".mp3"
    audio_path = output_dir / audio_filename
    transcript_filename = video_path.stem + "_transcript.txt"
    transcript_path = output_dir / transcript_filename

    if audio_path.exists():
        logger.info(f"Audio file {audio_path} already exists. Skipping audio extraction.")
    else:
        video = VideoFileClip(str(video_path))
        video.audio.write_audiofile(str(audio_path))
        video.close()
        logger.info(f"Audio extracted to {audio_path}")

    if transcript_path.exists():
        logger.info(f"Transcript file {transcript_path} already exists. Skipping transcription.")
        with open(transcript_path, 'r') as file:
            transcript = file.read()
    else:
        transcript = transcribe_audio(str(audio_path))
        logger.info("Transcription completed.")
        with open(transcript_path, 'w') as file:
            file.write(transcript)
        logger.info(f"Transcript written to {transcript_path}")

    summary = summarize_with_openai(transcript)
    logger.info("Summary completed.")

    summary_filename = video_path.stem + "_summary.txt"
    summary_path = output_dir / summary_filename
    with open(summary_path, 'w') as file:
        file.write(summary)
    logger.info(f"Summary written to {summary_path}")

    return summary

def process_chapter_file(chapter_file, output_dir):
    """
    Process a single chapter file: extract audio, transcribe, and summarize.
    """
    logger.info(f"Processing chapter: {chapter_file.name}")
    summary = extract_and_summarize(chapter_file, output_dir)
    print(f"Summary for {chapter_file.name}:\n{summary}")



# Assuming dedicated_output_dir is the Path object pointing to the directory containing the summary files
summary_files = list(dedicated_output_dir.glob('*_summary.txt'))

def read_summary(file_path):
    """Reads the content of a summary file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

import re
import textwrap

def safe_extract_number(filename):
    """Extracts chapter number from filename, returning a large default value if not found."""
    # Attempt to extract the chapter number based on the observed pattern in your filenames
    match = re.search(r'- (\d+) ', filename.stem)
    if match:
        return int(match.group(1))
    else:
        # Return a large number to place unmatched files at the end of the list
        return float('inf')

def display_chapter_summaries(summary_files):
    print(f"{'Chapter Name':<50} | {'Chapter Summary'}")
    print(f"{'-'*50} | {'-'*80}")

    # Use the safe_extract_number function for sorting
    sorted_summary_files = sorted(summary_files, key=safe_extract_number)

    for summary_file in sorted_summary_files:
        chapter_name = summary_file.stem.replace('_summary', '')

        summary_text = read_summary(summary_file)

        wrapped_name = textwrap.wrap(chapter_name, width=50)
        wrapped_summary = textwrap.wrap(summary_text, width=80)
        max_lines = max(len(wrapped_name), len(wrapped_summary))

        for i in range(max_lines):
            name_segment = wrapped_name[i] if i < len(wrapped_name) else " " * 50
            summary_segment = wrapped_summary[i] if i < len(wrapped_summary) else ""
            print(f"{name_segment:<50} | {summary_segment}")

        print(f"{'-'*50} | {'-'*80}")

def get_video_link(summary_file):
    """
    Constructs the path to the video file based on the summary file's name.
    Assumes video files are in the same directory and follow a similar naming convention.
    """
    # Replace '_summary.txt' with '.mp4' to get the video file name
    video_filename = summary_file.name.replace('_summary.txt', '.mp4')
    video_path = summary_file.parent / video_filename
    return video_path.as_uri()  # Converts the path to a URI that can be used in the HTML

def extract_sequence_number(filename):
    """
    Extracts the first sequence of digits found in the filename and returns it as an integer.
    If no digits are found, returns a high default value to ensure such files are sorted last.
    """
    match = re.search(r'\d+', filename.stem)
    if match:
        return int(match.group(0))
    else:
        return float('inf')  # Use infinity to sort non-matching files last


def display_chapter_summaries_in_browser(summary_files):
    # Sort the summary files based on the sequence number
    sorted_summary_files = sorted(summary_files, key=lambda file: extract_sequence_number(Path(file)))

    # HTML template for the page
    html_template = """
    <html>
    <head>
        <title>Chapter Summaries</title>
        <style>
            body {{font-family: Arial, sans-serif;}}
            table {{border-collapse: collapse; width: 100%;}}
            th, td {{text-align: left; padding: 8px; border-bottom: 1px solid #ddd;}}
            th {{background-color: #f2f2f2;}}
            img {{max-width: 200px; height: auto;}}
            ul, ol {{margin-left: 20px;}}
        </style>
    </head>
    <body>
        <h2>Chapter Summaries</h2>
        <table>
            <tr>
                <th>Chapter Name</th>
                <th>Chapter Video Screenshot</th>
                <th>Chapter Summary</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """


    rows = ""
    
    for summary_file in sorted_summary_files:
        chapter_name = Path(summary_file).stem.replace('_summary', '')
        summary_text = read_summary(Path(summary_file))
        # Remove leading asterisks and convert bullet points and numbered lists to HTML lists
        summary_text = summary_text.lstrip('* ')
        summary_text = convert_to_html_lists(summary_text)

        screenshot_path = get_video_screenshot(Path(summary_file))
        video_path = get_video_link(Path(summary_file))

        rows += f"""
        <tr>
            <td>{chapter_name}</td>
            <td><a href="{video_path}" target="_blank"><img src="{screenshot_path}" alt="Chapter Screenshot"></a></td>
            <td>{summary_text}</td>
        </tr>
        """

    html_content = html_template.format(rows=rows)

    # Write the HTML content to a temporary file and open it in the browser
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as tmp_file:
        tmp_file.write(html_content)
        webbrowser.open('file://' + os.path.realpath(tmp_file.name))


def convert_to_html_lists(text):
    """Converts markdown-style lists to HTML lists."""
    lines = text.split('\n')
    html_lines = []
    in_list = False
    list_type = None  # 'ul' for unordered list, 'ol' for ordered list

    for line in lines:
        if line.startswith('* '):
            if not in_list or list_type != 'ul':
                if in_list:  # Close the previous list
                    html_lines.append(f"</{list_type}>")
                html_lines.append("<ul>")
                in_list = True
                list_type = 'ul'
            html_lines.append(f"<li>{line[2:]}</li>")
        elif re.match(r'\d+\.', line.strip()):
            if not in_list or list_type != 'ol':
                if in_list:  # Close the previous list
                    html_lines.append(f"</{list_type}>")
                html_lines.append("<ol>")
                in_list = True
                list_type = 'ol'
            html_lines.append(f"<li>{line[line.index('.')+2:]}</li>")
        else:
            if in_list:  # Close the current list
                html_lines.append(f"</{list_type}>")
                in_list = False
                list_type = None
            html_lines.append(line)

    if in_list:  # Ensure the final list is closed
        html_lines.append(f"</{list_type}>")

    return '<br>'.join(html_lines)


    # Use the safe_extract_number function for sorting, assuming it's defined elsewhere to sort chapters
    sorted_summary_files = sorted(summary_files, key=lambda f: safe_extract_chapter_number(Path(f)))

    # Generate table rows, now including video screenshots linked to the videos
    rows = ""
    for summary_file in sorted_summary_files:
        chapter_name = summary_file.stem.replace('_summary', '')
        summary_text = read_summary(summary_file)
        # Convert bullet points marked by "*" into HTML list items
        summary_text_formatted = summary_text.replace('\n* ', '\n<li>').replace('<li>', '</ul><ul><li>', 1).rstrip('</ul><ul><li>').rstrip('\n<li>') + '</ul>'
        summary_text_formatted = summary_text_formatted if summary_text_formatted.startswith('<ul>') else '<ul>' + summary_text_formatted
        summary_text_formatted = summary_text_formatted if summary_text_formatted.endswith('</ul>') else summary_text_formatted + '</ul>'
        summary_text_formatted = summary_text_formatted.replace('</ul><ul>', '')
        
        screenshot_path = get_video_screenshot(summary_file)  # Function to get screenshot, assume defined elsewhere
        video_path = get_video_link(summary_file)  # Function to construct video path, assume defined elsewhere

        rows += f"""
        <tr>
            <td>{chapter_name}</td>
            <td><a href="{video_path}" target="_blank"><img src="{screenshot_path}" alt="Chapter Screenshot"></a></td>
            <td>{summary_text_formatted}</td>
        </tr>
        """

    html_content = html_template.format(rows=rows)

    # Write the HTML content to a temporary file and open it in the browser
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as tmp_file:
        tmp_file.write(html_content)
        webbrowser.open('file://' + os.path.realpath(tmp_file.name))

def safe_extract_chapter_number(filename):
    """
    Attempts to extract a chapter number from a filename.
    Returns the chapter number if found, or a high default value for sorting.
    """
    # Attempt to find a sequence of digits that likely represents the chapter number
    match = re.search(r'\b(\d+)\b', filename.stem)
    if match:
        return int(match.group(1))
    else:
        return float('inf')  # Use infinity to ensure non-matching files sort last



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe and summarize video content.")
    parser.add_argument("video_path_or_url", type=str, help="Path to the video file or YouTube URL to process.")
    args = parser.parse_args()



    if is_youtube_url(args.video_path_or_url):
        logger.info("Downloading YouTube video...")
        # Set dedicated_output_dir based on the YouTube video
        dedicated_output_dir = Path.home() / ".DigestVid"
        chapter_files = download_youtube_video(args.video_path_or_url, dedicated_output_dir)
        if not chapter_files:
            logger.error("No chapters were downloaded.")
            exit(1)
        for chapter_file in chapter_files:
            process_chapter_file(chapter_file, chapter_file.parent)
    else:
        video_path = Path(args.video_path_or_url)
        if not video_path.is_file():
            logger.error("Video file does not exist.")
            exit(1)
        dedicated_output_dir = video_path.parent
        summary = extract_and_summarize(video_path, dedicated_output_dir)
        print(f"Summary:\n{summary}")

    # After processing, check if dedicated_output_dir is set and display the chapter summaries
    print("Video Output Dir")
    print(video_output_dir["path"])

    # This assumes dedicated_output_dir is correctly set to the individual video's subdirectory as per the rest of your script logic
    if video_output_dir["path"] and video_output_dir["path"].exists():
        # Directly use dedicated_output_dir to glob for summary files, as it should already point to ~/.DigestVid/<VideoName>
        summary_files = list(video_output_dir["path"].glob('*_summary.txt'))
        if summary_files:
            display_chapter_summaries(summary_files)
            display_chapter_summaries_in_browser(summary_files)
        else:
            print(f"No summary files found in {video_output_dir['path']}.")

    else:
        logger.error("The output directory is not set or does not exist.")





