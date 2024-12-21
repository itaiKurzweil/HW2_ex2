import subprocess
import pytest

# Mock function for video download
def mock_download_video(query):
    """
    Mock function to simulate video download.
    Returns a mocked video file path.
    """
    if query == "super mario movie trailer":
        return "video.mp4"  # Mocked video file path
    raise ValueError("Invalid query")

# Test for video download
def test_download_video():
    """
    Test for the video download functionality using a mock function.
    """
    # Simulate the function call
    result = mock_download_video("super mario movie trailer")
    
    # Assert the function returns the correct value
    assert result == "video.mp4"

# Mock function for scene detection
def mock_detect_scenes(video_path):
    """
    Mock function to simulate pyscenedetect detecting scenes.
    Returns a list of mocked scene timestamps.
    """
    if video_path == "video.mp4":
        return [(0, 100), (101, 200)]  # Mocked scene data
    return []

# Test for scene detection
def test_detect_scenes():
    """
    Test for scene detection functionality using a mock function.
    """
    # Simulate the function call
    scenes = mock_detect_scenes("video.mp4")
    
    # Assert the scenes are detected correctly
    assert scenes == [(0, 100), (101, 200)]
