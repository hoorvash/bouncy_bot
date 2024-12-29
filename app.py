import librosa
import numpy as np
import os
from logger_service import LoggerService
from pathlib import Path
import numpy as np
import gradio as gr


UPLOAD_DIR = "uploaded_audio"
VIDEO_DIR = "generated_videos"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

logger = LoggerService()

def extract_audio_features(audio_file: str) -> dict:
    """
    Extract audio features from a file using librosa.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        dict: Extracted audio features, including BPM and key.
    """
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Extract tempo (BPM)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    # Ensure tempo is a scalar (numpy.ndarray to float)
    if isinstance(tempo, np.ndarray):  # Check if tempo is an array
        tempo = tempo[0]  # Extract the first element if it's an array

    # Estimate the key using chroma features
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_index = chroma.mean(axis=1).argmax()
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = keys[key_index]

    # Infer emotional tone (basic heuristic based on BPM)
    emotion = "Energetic" if tempo > 120 else "Calm" if tempo < 80 else "Moderate"

    # Infer tempo label
    tempo_label = "Fast" if tempo > 120 else "Slow" if tempo < 80 else "Moderate"

    return {
        "bpm": round(tempo, 2),
        "key": key,
        "tempo": tempo_label,
        "emotion": emotion
    }

def format_prompt(genre: str, tempo: str, bpm: float, key: str, emotion: str) -> str:
    """
    Format the prompt dynamically based on audio features.

    Args:
        genre (str): The dance genre (e.g., Hip Hop, Contemporary).
        tempo (str): The tempo of the music (e.g., Slow, Moderate, Fast).
        bpm (float): Beats per minute of the audio.
        key (str): The musical key (e.g., C Major, D Minor).
        emotion (str): The emotional tone of the music (e.g., Energetic, Dramatic).

    Returns:
        str: The formatted prompt.
    """
    prompt_template = """
    Generate a JSON object that represents a professional 5-second dance sequence, suitable for use in text-to-video generation.

    Here are the requirements:
    1. The output must always follow the same JSON format, including a `dance_sequence` array and `metadata`.
    2. Each entry in the `dance_sequence` must:
       - Have a `timestamp` (start time of the pose in HH:MM:SS format) and a `duration` (duration of the pose in HH:MM:SS format).
       - Include a `pose_name` (brief, professional name of the pose).
       - Contain a `pose_description` (detailed explanation of the pose and movements).
       - Specify `movement_type` as either "static" or "dynamic".
       - Include `transition_to_next` (a clear description of how to move into the next pose seamlessly).
    3. The total duration of the sequence must not exceed 5 seconds.
    4. The sequence should focus on professional dance movements, with smooth transitions and precise details.
    5. The JSON must include a `metadata` section that specifies:
       - `dance_style`: {genre}
       - `tempo`: {tempo}
       - `starting_point`: Whether the snippet represents the start, middle, or end of the dance.
       - `music_features`: The musical context, including:
         - BPM = {bpm}
         - Key = {key}
         - Emotion = {emotion}.
       - `video_generation_notes`: Any important considerations for generating the video accurately.

    For this request, use the following music details:
    - Dance Style: {genre}
    - Tempo: {tempo}
    - BPM: {bpm}
    - Key: {key}
    - Emotion: {emotion}

    Generate smooth, professional, and creative movements that fit the style and tone of the specified music. Ensure logical and seamless transitions between poses.
    """
    return prompt_template.format(
        genre=genre, tempo=tempo, bpm=bpm, key=key, emotion=emotion
    )

def create_interface(api_key: str):
    with gr.Blocks() as ui:
        gr.Markdown("# AI Dance Sequence Generator")

        with gr.Row():
            genre_dropdown = gr.Dropdown(
                label="Select Dance Genre",
                choices=["Tap Dance", "Broadway", "Hip Hop", "Contemporary"],
                value="Hip Hop"
            )
            audio_input = gr.Audio(label="Upload Audio", type="filepath")
        
        generate_button = gr.Button("Generate Video")

        with gr.Row():
            status_message = gr.Markdown(label="Status")
            json_output = gr.Textbox(label="Generated JSON", lines=20, interactive=False)
            video_output = gr.Video(label="Generated Video", format="mp4", visible=True)

        def handle_generate(genre, audio_path):
            return process_audio(api_key, genre, audio_path)

        generate_button.click(
            handle_generate,
            inputs=[genre_dropdown, audio_input],
            outputs=[status_message, json_output, video_output]
        )

    return ui

def process_audio(api_key: str, genre: str, audio_path: str):
    """
    Process the uploaded audio, extract features, and generate a JSON sequence via OpenAI API.

    Args:
        api_key (str): OpenAI API key.
        genre (str): Selected genre.
        audio_path (str): Path to the uploaded audio file.

    Returns:
        tuple: Status message, JSON output, and video path.
    """
    try:
        # Call OpenAI API to generate JSON sequence
        json_response = call_openai_api(api_key, genre, audio_path)
    except Exception as e:
        return f"Error while calling OpenAI API: {e}", None, None

    # Save JSON to a file for reference
    json_path = os.path.join(VIDEO_DIR, f"{Path(audio_path).stem}_{genre}.json")
    with open(json_path, "w") as json_file:
        json_file.write(json_response)

    # Simulate video generation based on the JSON
    video_path = generate_video({}, audio_path, genre)

    # Return status, JSON response, and video path
    return (
        f"Video generated successfully! JSON saved at: {json_path}, Video saved at: {video_path}",
        json_response,
        video_path
    )

from openai import OpenAI

def call_openai_api(api_key: str, genre: str, audio_file: str) -> str:
    """
    Call OpenAI API to generate a JSON dance sequence based on audio features and genre.

    Args:
        api_key (str): OpenAI API key.
        genre (str): Selected dance genre.
        audio_file (str): Path to the uploaded audio file.

    Returns:
        str: JSON response from the API.
    """
    # Extract audio features using the provided function
    features = extract_audio_features(audio_file)
    print(features)
    # Format the prompt dynamically
    prompt = format_prompt(
        genre=genre,
        tempo=features["tempo"],
        bpm=features["bpm"],
        key=features["key"],
        emotion=features["emotion"]
    )

    #Call the OpenAI API
    client = OpenAI(api_key=api_key)
    chat_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a JSON generator for professional dance sequences."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the generated JSON
    return chat_response.choices[0].message.content
    # return "This is working"

def generate_video(features: dict, audio_file: str, genre: str) -> str:
    """
    Generate a video based on audio features.

    Args:
        features (dict): Extracted audio features.
        audio_file (str): Path to the uploaded audio file.
        genre (str): Selected genre.

    Returns:
        str: Path to the generated video file.
    """
    # Simulate video generation
    video_path = os.path.join(VIDEO_DIR, f"{Path(audio_file).stem}_{genre}.mp4")
    with open(video_path, "w") as f:
        f.write("Generated video content")
    return video_path #Generate video from the dance sequence and audio using the video generator

def generateVideoFromText(text: str) -> str:
    """Generate a video from the text"""
    return None #Generate video from the text using the video generator


if __name__ == "__main__":
    # Check for API key at startup
    if not os.getenv("REPLICATE_API_TOKEN"):
        logger.warning("REPLICATE_API_TOKEN not found in environment variables")
        print("Warning: REPLICATE_API_TOKEN not set. Please set it before generating videos.")

    logger.info("Starting BouncyBot application")
    app = create_interface(api_key)
    app.launch()