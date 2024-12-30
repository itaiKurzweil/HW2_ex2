import os
import re
import time
import google.generativeai as genai
import subprocess

# Configure the Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    print("Uploading video to Gemini API...")
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

def search_in_gemini(video_path, user_query):
    """Uses Gemini API to find timestamps matching the user query in the video."""
    # Upload video to Gemini
    files = [upload_to_gemini(video_path, mime_type="video/mp4")]
    wait_for_files_active(files)

    # Start a chat session
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
    chat_session = model.start_chat(history=[])

    # Send the query to Gemini
    prompt = {
        "role": "user",
        "parts": [
            f"This is the video. Give me the timestamps of all frames where you see '{user_query}' in the video.",
            files[0],
        ],
    }
    response = chat_session.send_message(prompt)
    print(f"Received response to check: {response.text}")
    
    # Extract timestamps from response
    pattern = r"(\d{1,2}:\d{2}:\d{2})"
    matches_time = re.findall(pattern, response.text)
    print(f"Found timestamps: {matches_time}")

    return matches_time



def extract_frames(matches_time, frame_folder, video_path):
    """Extracts frames from the video at the given timestamps."""
    extracted_frames = []
    os.makedirs(frame_folder, exist_ok=True)
    for idx, timestamp in enumerate(matches_time):
        output_image_path = os.path.join(frame_folder, f"frame_{idx:03d}.jpg")
        command = [
            "ffmpeg", "-y", 
            "-ss", str(timestamp), "-i", video_path,
            "-frames:v", "1", "-q:v", "2", output_image_path
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Extracted frame at {timestamp} -> {output_image_path}")
            extracted_frames.append(output_image_path)
        except subprocess.CalledProcessError as e:
            print(f"Error extracting frame at {timestamp}: {e}")
    return extracted_frames

