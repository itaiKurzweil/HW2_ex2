import os
from download_video import download_video
from detect_scenes import detect_and_save_scenes
from generate_captions import generate_captions
from search_captions import load_captions, search_captions_advanced
from create_collage import create_collage

def main():
    # Step 1: Download the video
    video_url = input("Enter the video URL (super mario movie trailer):  ").strip()
    video_file = "downloaded_video.mp4"
    download_video(video_url, video_file)
    print(f"Video downloaded to {video_file}")


    # Step 2: Detect scenes in the video
    scene_images_folder = "scene_images"
    os.makedirs(scene_images_folder, exist_ok=True)
    detect_and_save_scenes(video_file, scene_images_folder)
    print(f"Scenes saved in {scene_images_folder}")

    # Step 3: Generate captions for the detected scenes
    model_path = "path_to_moondream_model"  # Update with the correct model path
    captions_file = "scene_captions.json"
    generate_captions(scene_images_folder, model_path, captions_file)
    print(f"Captions generated and saved to {captions_file}")

    # Step 4: Search captions dynamically
    captions = load_captions(captions_file)
    threshold = 60  # Adjust similarity threshold
    search_word = input("Search the video using a word: ").strip()
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
