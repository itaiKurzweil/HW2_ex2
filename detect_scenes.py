import os
import cv2
from scenedetect import SceneManager, open_video
from scenedetect.detectors import ContentDetector

def detect_and_save_scenes(video_path, output_folder="scene_images", min_scene_length=15, threshold=30.0):
    """
    Detects scenes in a video and saves scene images to a folder.

    Args:
        video_path (str): Path to the video file.
        output_folder (str): Path to save scene images.
        min_scene_length (int): Minimum scene length in seconds.
        threshold (float): Sensitivity of scene detection.

    Returns:
        list: A list of scenes as (start_time, end_time).
    """
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        video = open_video(video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=threshold, min_scene_len=min_scene_length))
        scene_manager.detect_scenes(video)
        scenes = scene_manager.get_scene_list()

        cap = cv2.VideoCapture(video_path)
        for i, (start_time, _) in enumerate(scenes):
            cap.set(cv2.CAP_PROP_POS_MSEC, start_time.get_seconds() * 1000)  # Convert to milliseconds
            success, frame = cap.read()
            if success:
                image_path = os.path.join(output_folder, f"scene_{i + 1}.jpg")
                cv2.imwrite(image_path, frame)
        
        cap.release()
        print(f"Saved {len(scenes)} scene images to {output_folder}.")
        return scenes
    except Exception as e:
        raise RuntimeError(f"Failed to detect and save scenes: {e}")

if __name__ == "__main__":
    video_path = "video.mp4"
    output_folder = "scene_images"
    scenes = detect_and_save_scenes(video_path, output_folder, min_scene_length=15, threshold=30.0)
    print(f"Scenes saved: {len(scenes)}")
