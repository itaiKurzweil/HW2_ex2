import json
from rapidfuzz import process


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


def search_captions_advanced(captions, keyword, threshold):
    """
    Advanced search using rapidfuzz for keyword similarity in captions.

    Args:
        captions (dict): Dictionary of scene captions.
        keyword (str): Word to search for.
        threshold (float): Similarity threshold (0-100).

    Returns:
        list: List of scene numbers with captions matching the keyword.
    """
    matches = []
    for scene, caption in captions.items():
        match_score = process.extractOne(keyword, [caption], score_cutoff=threshold)
        if match_score:
            matches.append(scene)
    return matches


if __name__ == "__main__":
    captions_file = "scene_captions.json"
    captions = load_captions(captions_file)

    # Set your threshold for similarity
    threshold = 70  # Adjust this value to control similarity sensitivity
    print(f"\nUsing threshold: {threshold}")

    # Prompt user for search input
    search_word = input("Search the video using a word: ").strip()

    # Perform advanced search with rapidfuzz
    matches = search_captions_advanced(captions, search_word, threshold)

    # Display results
    if matches:
        print(f"Scenes with similar captions to '{search_word}' (threshold={threshold}): {matches}")
    else:
        print(f"No scenes found matching '{search_word}' with the given threshold ({threshold}).")
