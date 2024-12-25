import json
import os
import moondream as md
from PIL import Image


def generate_captions(scene_images_folder, model_path, output_file="scene_captions.json"):
    """
    Generates captions for a list of scene images and saves them to a JSON file.

    Args:
        scene_images_folder (str): Path to the folder containing scene images.
        model_path (str): Path to the moondream model file.
        output_file (str): Path to save the captions JSON file.

    Returns:
        dict: Scene captions as {scene_number: caption}.
    """
    # Load existing captions if the JSON file exists
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Loading existing captions...")
        with open(output_file, "r") as f:
            captions = json.load(f)
    else:
        captions = {}

    # Get all scene images
    scene_images = {
        int(os.path.splitext(file)[0].split('_')[1]): os.path.join(scene_images_folder, file)
        for file in os.listdir(scene_images_folder)
        if file.endswith(".jpg") and file.startswith("scene_")
    }

    # Check if all scenes are already captioned
    if set(captions.keys()) == set(map(str, scene_images.keys())):
        print("All scenes already captioned. Skipping caption generation.")
        return captions

    # Initialize the model
    print("Initializing moondream model...")
    model = md.vl(model=model_path)

    # Generate captions for missing scenes
    try:
        for scene, image_path in scene_images.items():
            if str(scene) in captions:
                print(f"Scene {scene} already captioned. Skipping...")
                continue

            print(f"Processing scene {scene}...")
            image = Image.open(image_path)
            encoded_image = model.encode_image(image)
            caption = model.caption(encoded_image)["caption"]
            captions[str(scene)] = caption

        # Save captions to JSON
        with open(output_file, "w") as f:
            json.dump(captions, f)

        print(f"Captions saved to {output_file}.")
        return captions

    except Exception as e:
        raise RuntimeError(f"Failed to generate captions: {e}")


# if __name__ == "__main__":
#     # Example usage
#     scene_images_folder = "scene_images"  # Folder where scene images are saved
#     model_path = r"C:\Users\itaik\Downloads\moondream-2b-int8.mf\moondream-2b-int8.mf"  # Path to model
#     captions = generate_captions(scene_images_folder, model_path)
#     print(f"Generated captions: {captions}")