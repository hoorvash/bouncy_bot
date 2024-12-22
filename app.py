import os
from dotenv import load_dotenv
import replicate
from typing import List, Dict, Tuple
import gradio as gr
from logger_service import LoggerService
from dance_movements import DanceMovements
from pathlib import Path
import requests
from datetime import datetime
import urllib.request
from video_generators import get_video_generator

# Load environment variables from .env file
load_dotenv()
logger = LoggerService()


SAVED_VIDEOS = {
    "Tap Dance": "videos/tap.mp4",
    "Broadway": "videos/broadway.mp4",
    "Hip Hop": "videos/hiphop.mp4",
    "Contemporary": "videos/contemporary.mp4"
}

def get_dance_sequence(dance_style: str) -> List[Dict]:
    """Get the dance sequence for the specified style"""
    if dance_style == "Tap Dance":
        return DanceMovements.TAP_DANCE
    elif dance_style == "Broadway":
        return DanceMovements.BROADWAY
    elif dance_style == "Hip Hop":
        return DanceMovements.HIP_HOP
    elif dance_style == "Contemporary":
        return DanceMovements.CONTEMPORARY
    else:
        raise ValueError(f"Unknown dance style: {dance_style}")

def format_dance_sequence(movements: List[Dict]) -> str:
    """Format the dance sequence into readable text"""
    output = []
    for i, move in enumerate(movements, 1):
        output.append(f"Step {i}:")
        output.append(f"Position: {move['position']}")
        output.append(f"Movement: {move['movement']}")
        output.append(f"Duration: {move['timing']} seconds\n")
    return "\n".join(output)

def create_interface():
    # Custom CSS to reduce button width and increase height
    custom_css = """
    .my_button {
        width: 150px;            /* Smaller width */
        height: 50px;           /* Larger height */
        background-color: #ff6b6b;
        color: white;
        font-size: 14px;
        border-radius: 5px;
        cursor: pointer;
        border: none;
        display: inline-block;   /* Don't stretch to full row */
        text-align: center; 
        margin: 4px;            /* Optional margin around each button */
    }
    .my_button:hover {
        background-color: #ff4949;
    }
    """

    with gr.Blocks(css=custom_css) as dance_app:
        gr.Markdown("# AI Dance Sequence Generator")
        
        with gr.Row():
            with gr.Column():
                # Attach custom CSS class to each button
                tap_btn = gr.Button("Tap Dance", elem_classes="my_button")
                broadway_btn = gr.Button("Broadway", elem_classes="my_button")
                hiphop_btn = gr.Button("Hip Hop", elem_classes="my_button")
                contemporary_btn = gr.Button("Contemporary", elem_classes="my_button")
                
                generator_type = gr.Radio(
                    choices=["Sora", "replicate", "pygame"],
                    value="Sora",
                    label="Video Generator",
                    interactive=True
                )
        
        with gr.Row():
            text_output = gr.Markdown(
                label="Dance Description",
                visible=False
            )
            with gr.Column() as video_column:
                video_output = gr.Video(
                    label="Generated Dance",
                    format="mp4",
                    visible=True
                )
                loading_message = gr.Markdown(visible=False)
            
        status_message = gr.Markdown("Select a dance style to begin!")
        
        def update_text_and_status(dance_style):
            """First callback to immediately update text description"""
            try:
                movements = get_dance_sequence(dance_style)
                text_description = format_dance_sequence(movements)
                # Return: text, video (None), video visibility, loading visibility, loading text, status
                return [
            text_description,  # for a Textbox
            None,             # for a Video (if you want to clear it)
            "Loading your dance video...",  # for your Markdown
            ]
            except Exception as e:
                return [
                    None,
                    None,
                    f"❌ Error: {e}"
                ]

        # def generate_video(dance_style, generator_choice):
            # """Generate video using selected generator"""
            # try:
            #     movements = get_dance_sequence(dance_style)
            #     generator = get_video_generator(generator_choice)
            #     if not generator:
            #         raise ValueError(f"Unknown generator type: {generator_choice}")
                
            #     video_path = generator.generate(movements)
            #     if video_path and os.path.exists(video_path):
            #         return [
            #             video_path,
            #             True,
            #             False,
            #             "",
            #             f"✅ Video generated successfully using {generator_choice}!"
            #         ]
            #     else:
            #         return [None, False, False, "", "❌ Failed to generate video"]
            # except Exception as e:
            #     error_msg = f"❌ Error generating video: {str(e)}"
            #     logger.error(f"Error in video generation: {str(e)}", exc_info=True)
            #     return [None, False, False, "", error_msg]

        def show_saved_video(dance_style):
            """Return the path of the pre-saved video for the chosen dance style."""
            try:
                video_path = SAVED_VIDEOS[dance_style]
                # Check if file exists (optional)
                if not os.path.exists(video_path):
                    raise FileNotFoundError(f"Video not found for {dance_style} at {video_path}")
                
                return [
                    video_path,   # video output
                    f"✅ Loaded the pre-saved video for {dance_style}!"
                ]
            except Exception as e:
                error_msg = f"❌ Error showing video: {str(e)}"
                logger.error(error_msg)
                return [None, error_msg]
        # Connect buttons
        for btn, style in [(tap_btn, "Tap Dance"), 
                          (broadway_btn, "Broadway"),
                          (hiphop_btn, "Hip Hop"),
                          (contemporary_btn, "Contemporary")]:
            btn.click(
                fn=lambda s=style: update_text_and_status(s),
                outputs=[
                text_output,
                video_output,     # <-- Only for the actual video file
                status_message
                ],
                queue=False
            ).then(
                fn=lambda s=style: show_saved_video(s),
                outputs=[
                video_output,     # <-- Only for the actual video file
                status_message
                ],
                queue=True
            )
    
    return dance_app

if __name__ == "__main__":
    # Check for API key at startup
    if not os.getenv("REPLICATE_API_TOKEN"):
        logger.warning("REPLICATE_API_TOKEN not found in environment variables")
        print("Warning: REPLICATE_API_TOKEN not set. Please set it before generating videos.")
    
    logger.info("Starting BouncyBot application")
    app = create_interface()
    app.launch()
