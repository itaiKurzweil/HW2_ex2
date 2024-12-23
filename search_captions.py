import json


def load_captions(file_path="scene_captions.json"):
    """
    Loads captions from a JSON file.

    Args:
        file_path (str): Path to the captions JSON file.

    Returns:
        dict: Captions loaded from the JSON file.
    """
    if not file_path or not file_path.endswith(".json"):
        raise ValueError("Invalid captions file path.")
    
    with open(file_path, "r") as f:
        captions = json.load(f)
    return captions


def search_captions_basic(captions, keyword):
    """
    Basic search for a keyword in captions.

    Args:
        captions (dict): Dictionary of scene captions.
        keyword (str): Word to search for.

    Returns:
        list: List of scene numbers containing the keyword.
    """
    return [scene for scene, caption in captions.items() if keyword.lower() in caption.lower()]


if __name__ == "__main__":
    captions_file = "scene_captions.json"
    captions = load_captions(captions_file)

    # Prompt user for search input
    search_word = input("Search the video using a word: ").strip()

    # Perform basic search
    matches = search_captions_basic(captions, search_word)

    # Display results
    if matches:
        print(f"Scenes containing '{search_word}': {matches}")
    else:
        print(f"No scenes found containing the word '{search_word}'.")
