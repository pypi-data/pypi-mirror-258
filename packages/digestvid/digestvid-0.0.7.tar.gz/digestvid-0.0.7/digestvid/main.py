# main.py

import argparse
from pathlib import Path
import logging
# Import necessary functions from your package
from digestvid.utils import is_youtube_url, download_youtube_video, process_chapter_file, extract_and_summarize, display_chapter_summaries, display_chapter_summaries_in_browser, video_output_dir
from digestvid.utils import video_output_dir

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
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


if __name__ == "__main__":
    main()



