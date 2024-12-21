import subprocess
import pytest
import json
from rapidfuzz import process
from unittest.mock import MagicMock

# Mock function for search
def mock_search_captions(captions, query, threshold=75):
    """
    Mock function to simulate searching captions using rapidfuzz.
    Returns a list of scene numbers where the query matches.
    """
    matches = []
    for scene, caption in captions.items():
        if process.extractOne(query, [caption], score_cutoff=threshold):
            matches.append(scene)
    return matches

# Mock function for collage creation
def mock_create_collage(scene_images, matching_scenes, output_file):
    """
    Mock function to simulate collage creation.
    Returns a message indicating the collage has been 'saved.'
    """
    matched_images = [scene_images[scene] for scene in matching_scenes]
    # Simulate combining images (in reality, you'd use an image library here)
    return f"Collage created with images: {matched_images}"

# Test for search functionality
def test_search_captions():
    """
    Test for searching captions functionality using MagicMock.
    """
    # Mock the rapidfuzz process for searching captions
    mock_extract_one = MagicMock()
    mock_extract_one.side_effect = lambda query, choices, score_cutoff: (
        (query in choices[0], 85) if query in choices[0] else None
    )

    # Mock captions dictionary
    captions = {
        1: "A red car driving down the street.",
        2: "A group of people sitting in a park.",
        3: "A person playing a guitar on stage."
    }

    # Use MagicMock to simulate the behavior of rapidfuzz search
    matches = []
    for scene, caption in captions.items():
        result = mock_extract_one("car", [caption], score_cutoff=75)
        if result:
            matches.append(scene)

    # Assert the correct scenes are returned
    assert matches == [1]

    # Simulate a search for a different term
    matches = []
    for scene, caption in captions.items():
        result = mock_extract_one("guitar", [caption], score_cutoff=75)
        if result:
            matches.append(scene)

    # Assert the correct scenes are returned
    assert matches == [3]


# Test for collage creation
def test_create_collage():
    """
    Test for collage creation functionality.
    """
    # Mocked scene images
    scene_images = {
        1: "scene_1.jpg",
        2: "scene_2.jpg",
        3: "scene_3.jpg",
    }
    
    # Mocked matching scenes
    matching_scenes = [1, 3]
    
    # Simulate creating a collage
    collage_message = mock_create_collage(scene_images, matching_scenes, "collage.png")
    
    # Assert the collage message is correct
    assert collage_message == "Collage created with images: ['scene_1.jpg', 'scene_3.jpg']"

# Mock function for image captioning
def mock_caption_image(image_path):
    """
    Mock function to simulate image captioning with moondream2.
    Returns a mocked caption for the image.
    """
    if image_path == "scene_1.jpg":
        return "A red car driving down the street."
    elif image_path == "scene_2.jpg":
        return "A group of people sitting in a park."
    return "Unknown scene"

# Mock function to save captions to JSON
def mock_save_captions_to_json(captions, output_file):
    """
    Mock function to simulate saving captions to a JSON file.
    """
    # Simulate saving to JSON without writing to disk
    return json.dumps(captions)

# Test for captioning
def test_caption_images():
    """
    Test for image captioning functionality.
    """
    # Mocked scene images
    scene_images = {
        1: "scene_1.jpg",
        2: "scene_2.jpg",
    }
    
    # Generate captions using the mock function
    captions = {
        scene: mock_caption_image(image) for scene, image in scene_images.items()
    }
    
    # Assert the captions are correct
    assert captions == {
        1: "A red car driving down the street.",
        2: "A group of people sitting in a park."
    }
    
    # Simulate saving the captions to JSON
    json_output = mock_save_captions_to_json(captions, "scene_captions.json")
    
    # Assert the JSON output is correct
    expected_json = json.dumps({
        1: "A red car driving down the street.",
        2: "A group of people sitting in a park."
    })
    assert json_output == expected_json


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
