import os
from download_video import download_video
from detect_scenes import detect_and_save_scenes
from generate_captions import generate_captions
from search_captions import load_captions, search_captions_advanced, CaptionCompleter
from create_collage import create_collage
from prompt_toolkit import prompt

def main():
    # Step 1: Download the video
    video_file = "downloaded_video.mp4"
    if not os.path.exists(video_file):
        video_url = "https://www.youtube.com/results?search_query=super+mario+movie+trailer"  # Super Mario movie trailer
        download_video(video_url, video_file)
        print(f"Video downloaded to {video_file}")
    else:
        print(f"Video already exists: {video_file}")

    # Step 2: Detect scenes in the video
    scene_images_folder = "scene_images"
    os.makedirs(scene_images_folder, exist_ok=True)
    if not os.listdir(scene_images_folder):
        detect_and_save_scenes(video_file, scene_images_folder)
        print(f"Scenes saved in {scene_images_folder}")
    else:
        print(f"Scenes already detected and saved in {scene_images_folder}")

    # Step 3: Generate captions for the detected scenes
    model_path = "path_to_moondream_model"  # Update with the correct model path
    captions_file = "scene_captions.json"
    if not os.path.exists(captions_file):
        generate_captions(scene_images_folder, model_path, captions_file)
        print(f"Captions generated and saved to {captions_file}")
    else:
        print(f"Captions already exist in {captions_file}")

    # Step 4: Search captions dynamically with auto-complete
    captions = load_captions(captions_file)
    completer = CaptionCompleter(captions)  # Use the completer for suggestions
    search_word = prompt("Search the video using a word: ", completer=completer).strip()
    
    if not search_word:
        print("No search word provided. Exiting.")
        return
    
    threshold = 60  # Adjust similarity threshold
    matches = search_captions_advanced(captions, search_word, threshold)


    if not matches:
        print(f"No scenes found matching '{search_word}' with the given threshold ({threshold}).")
        return
    else:
        print(f"Found scenes: {matches}")

    # Step 5: Create a collage of the matched scenes
    image_paths = [os.path.join(scene_images_folder, f"scene_{scene}.jpg") for scene in matches]
    collage_file = "collage.png"
    create_collage(image_paths, collage_file)
    print(f"Collage created and saved to {collage_file}")

if __name__ == "__main__":
    main()
