from yt_dlp import YoutubeDL

def download_video(query, output_file="video.mp4"):
    """
    Downloads a video based on the given query using yt-dlp's Python API.

    Args:
        query (str): Search query for the video.
        output_file (str): The output file name for the downloaded video.

    Returns:
        str: Path to the downloaded video file.
    """
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_file,  # Output template for the file
            'quiet': True,  # Suppress yt-dlp logs
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch:{query}"])
        return output_file
    except Exception as e:
        raise RuntimeError(f"Failed to download video: {e}")
    
if __name__ == "__main__":
    try:
        video_file = download_video("super mario movie trailer")
        print(f"Video downloaded to: {video_file}")
    except Exception as e:
        print(f"Error: {e}")
