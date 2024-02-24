import re
import os
import pytube
from pytube import Playlist
from moviepy.editor import *


def get_playlist_video_urls(playlist_url):
    """Get all video URLs from a YouTube playlist."""
    playlist = Playlist(playlist_url)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    return playlist.video_urls


def download_video(video_url, output_path):
    """Download a single video from YouTube."""
    video = pytube.YouTube(video_url)
    stream = video.streams.get_highest_resolution()
    print(f"Downloading: {video.title}...")
    stream.download(output_path)
    print(f"{video.title} downloaded successfully!")


def convert_to_mp3(input_path, output_path):
    try:
        clip = AudioFileClip(input_path)
        clip.write_audiofile(output_path)
        clip.close()
        return True
    except Exception as e:
        print("Error:", e)
        return False


def download_audio(video_url, output_path):
    """Download a single video from YouTube."""
    video = pytube.YouTube(video_url)
    audio_stream = video.streams.filter(only_audio=True).first()
    print(f"Downloading: {video.title}...")
    audio_stream.download(output_path)
    audio_file = audio_stream.default_filename
    mp3_file = audio_file.replace(".mp4", ".mp3")
    if convert_to_mp3(
        os.path.join(output_path, audio_file), os.path.join(output_path, mp3_file)
    ):
        os.remove(os.path.join(output_path, audio_file))
    print(f"{video.title} downloaded successfully!")


def download_playlist_videos(playlist_url, output_path, audio_only=False):
    """Download all videos from a YouTube playlist."""
    video_urls = get_playlist_video_urls(playlist_url)
    print(f"Total videos in playlist: {len(video_urls)}")

    downloader = download_audio if audio_only else download_video
    for video_url in video_urls:
        downloader(video_url, output_path)


def handle_video_download(is_playlist: bool = False, audio_only: bool = False) -> None:
    output_path = input("Output path: ")
    if is_playlist:
        playlist_url = input("Playlist URL: ")
        download_playlist_videos(playlist_url, output_path, audio_only)
    else:
        video_url = input("Video URL: ")
        if audio_only:
            download_audio(video_url, output_path)
        else:
            download_video(video_url, output_path)


def main() -> None:
    while True:
        is_playlist_download: str = None
        while True:
            print(
                """Welcome to the YouTube Playlist Downloader!
            Please enter the URL of the playlist you want to download.
                Choose the download type:
                    1. Single Video
                    2. Playlist
        """
            )
            download_type = input("Enter your choice (1/2): ")
            if download_type.isnumeric() and int(download_type) in [1, 2]:
                is_playlist_download = int(download_type) == 2
                break
            print("\nInvalid choice! Please enter 1 or 2.")

        download_type: str = None
        while True:
            print(
                """Welcome to the YouTube Playlist Downloader!
            Please enter the URL of the playlist you want to download.
                Choose the download type:
                    1. Video
                    2. Audio
        """
            )
            download_type = input("Enter your choice (1/2): ")
            if download_type.isnumeric() and int(download_type) in [1, 2]:
                break
            print("\nInvalid choice! Please enter 1 or 2.")

        handle_video_download(is_playlist_download, int(download_type) == 2)
        print("All videos downloaded successfully!")


if __name__ == "__main__":
    main()
