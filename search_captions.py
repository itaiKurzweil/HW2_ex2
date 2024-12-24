import json
from rapidfuzz import process, fuzz
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

class CaptionCompleter(Completer):
    def __init__(self, captions):
        """Initialize the completer with a list of captions."""
        self.words = set()
        for caption in captions.values():
            self.words.update(caption.lower().split())

    def get_completions(self, document, complete_event):
        """Yield auto-complete suggestions based on the current input."""
        word = document.text.lower()
        for w in sorted(self.words):
            if w.startswith(word):
                yield Completion(w, start_position=-len(word))

def load_captions(captions_file):
    """Load captions from a JSON file."""
    with open(captions_file, "r") as f:
        return json.load(f)


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







# if __name__ == "__main__":
#     captions_file = "scene_captions.json"
#     captions = load_captions(captions_file)

#     # Set your threshold for similarity
#     threshold = 60  # Adjust this value to control similarity sensitivity
#     print(f"\nUsing threshold: {threshold}")

#     # Prompt user for search input
#     search_word = input("Search the video using a word: ").strip()

#     # Perform advanced search with rapidfuzz
#     matches = search_captions_advanced(captions, search_word, threshold)

#     # Display results
#     if matches:
#         print(f"Scenes with similar captions to '{search_word}' (threshold={threshold}): {matches}")
#     else:
#         print(f"No scenes found matching '{search_word}' with the given threshold ({threshold}).")
