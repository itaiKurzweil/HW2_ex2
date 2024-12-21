import json
import os
import moondream as md
from PIL import Image




def generate_captions(scene_images, model_path, output_file="scene_captions.json"):
    """
    Generates captions for a list of scene images and saves them to a JSON file.

    Args:
        scene_images (dict): Dictionary of scene numbers and image paths.
        model_path (str): Path to the moondream model file.
        output_file (str): Path to save the captions JSON file.

    Returns:
        dict: Scene captions as {scene_number: caption}.
    """
    # Check if the JSON file already exists
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping caption generation.")
        with open(output_file, "r") as f:
            captions = json.load(f)
        return captions

    # Initialize the model
    model = md.vl(model=model_path)

    captions = {}
    try:
        for scene, image_path in scene_images.items():
            print(f"Processing scene {scene}...")
            # Load and process image
            image = Image.open(image_path)
            encoded_image = model.encode_image(image)

            # Generate caption
            caption = model.caption(encoded_image)["caption"]
            captions[scene] = caption

        # Save captions to JSON
        with open(output_file, "w") as f:
            json.dump(captions, f)

        print(f"Captions saved to {output_file}.")
        return captions
    except Exception as e:
        raise RuntimeError(f"Failed to generate captions: {e}")


if __name__ == "__main__":
    # Example usage
    scene_images = {
        1: "scene_images/scene_1.jpg",
        2: "scene_images/scene_2.jpg",
        3: "scene_images/scene_3.jpg",
    }
    # Use one of the options to define the correct file path
    model_path = "C:\Users\itaik\Downloads\moondream-2b-int8.mf"
    captions = generate_captions(scene_images, model_path)
    print(f"Generated captions: {captions}")
