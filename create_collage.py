from PIL import Image
from search_captions import load_captions, search_captions_advanced
import os


def create_collage(image_paths, output_file="collage.png", thumbnail_size=(200, 200)):
    """
    Creates a collage of images and saves it as a single image.

    Args:
        image_paths (list): List of paths to image files to include in the collage.
        output_file (str): Path to save the collage image.
        thumbnail_size (tuple): Size of each thumbnail in the collage (width, height).
    """
    if not image_paths:
        print("No images to create a collage.")
        return

    # Create thumbnails for all images
    images = []
    for image_path in image_paths:
        try:
            img = Image.open(image_path)
            img.thumbnail(thumbnail_size)  # Resize to thumbnail size
            images.append(img)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")

    if not images:
        print("No valid images loaded. Cannot create a collage.")
        return

    # Calculate the collage grid size
    num_images = len(images)
    num_cols = int(num_images**0.5) + 1  # Number of columns in the grid
    num_rows = (num_images // num_cols) + (num_images % num_cols > 0)  # Number of rows

    # Determine collage size
    collage_width = num_cols * thumbnail_size[0]
    collage_height = num_rows * thumbnail_size[1]
    collage = Image.new("RGB", (collage_width, collage_height), (255, 255, 255))  # White background

    # Place images in the collage
    x_offset = 0
    y_offset = 0
    for i, img in enumerate(images):
        collage.paste(img, (x_offset, y_offset))
        x_offset += thumbnail_size[0]
        if (i + 1) % num_cols == 0:  # Move to the next row
            x_offset = 0
            y_offset += thumbnail_size[1]

    # Save the collage
    collage.save(output_file)
    print(f"Collage saved as {output_file}")
    
    # Display the collage
    collage.show()


if __name__ == "__main__":
    # Load captions
    captions_file = "scene_captions.json"
    captions = load_captions(captions_file)

    # Set search parameters
    threshold = 60  # Adjust similarity sensitivity
    search_word = input("Search the video using a word: ").strip()

    # Search for matching scenes
    matches = search_captions_advanced(captions, search_word, threshold)

    # Ensure matches are valid
    if not matches:
        print(f"No scenes found matching '{search_word}' with the given threshold ({threshold}).")
    else:
        print(f"Found scenes: {matches}")

        # Create the collage using matching scenes
        scene_images_folder = "scene_images"
        image_paths = [os.path.join(scene_images_folder, f"scene_{scene}.jpg") for scene in matches]
        create_collage(image_paths)
