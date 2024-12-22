from abc import ABC, abstractmethod
from typing import List, Dict
import os
import requests
import urllib.request
from pathlib import Path
from datetime import datetime
import pygame
from logger_service import LoggerService
import replicate
import cv2  # Make sure to install opencv-python for video saving

logger = LoggerService()

class VideoGenerator(ABC):
    @abstractmethod
    def generate(self, movements: List[Dict]) -> str:
        """Generate video from movements and return the path to the video file"""
        pass

class ReplicateGenerator(VideoGenerator):
    def generate(self, movements: List[Dict]) -> str:
        """Generate video using Replicate API"""
        try:
            # Create videos directory if it doesn't exist
            video_dir = Path("videos")
            video_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            api_token = os.getenv("REPLICATE_API_TOKEN")
            if not api_token:
                raise ValueError("Missing Replicate API key")

            prompt = "A professional dancer in a red tank top and white sneakers performing: "
            for move in movements:
                prompt += f"{move['movement']} for {move['timing']} seconds, "
            
            logger.info(f"Generating video with Replicate: {prompt}")
            
            input = {
                "prompt": prompt,
                "negative_prompt": (
                    "blurry, distorted movements, unrealistic limbs, missing hands or feet, "
                    "low quality, grainy video, unnatural poses, async with beat"
                ),
                "seed": 42023,
                "duration": sum(float(m['timing']) for m in movements),
                "fps": 25
            }
            
            api = replicate.Client(api_token=api_token)
            output = api.run(
                "tencent/hunyuan-video:847dfa8b01e739637fc76f480ede0c1d76408e1d694b830b5dfb8e547bf98405",
                input=input
            )
            
            if output and output[0]:
                video_url = output[0]
                video_filename = f"dance_replicate_{timestamp}.mp4"
                video_path = video_dir / video_filename
                
                try:
                    response = requests.get(video_url, stream=True)
                    response.raise_for_status()
                    with open(video_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                except Exception as e:
                    logger.warning(f"Failed to download with requests, trying urllib: {e}")
                    urllib.request.urlretrieve(video_url, video_path)
                
                return str(video_path)
            return None
                
        except Exception as e:
            logger.error(f"Error in Replicate generation: {str(e)}", exc_info=True)
            raise

class PygameGenerator(VideoGenerator):
    def generate(self, movements: List[Dict]) -> str:
        """Generate a video using Pygame and OpenCV"""
        try:
            # Create output directory for videos
            video_dir = Path("videos")
            video_dir.mkdir(exist_ok=True)

            # Generate unique video filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"dance_pygame_{timestamp}.mp4"
            video_path = video_dir / video_filename

            logger.info("Generating video with Pygame")

            # Initialize Pygame
            pygame.init()
            width, height = 640, 480
            screen = pygame.Surface((width, height))

            # Set up OpenCV video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
            fps = 25
            out = cv2.VideoWriter(str(video_path), fourcc, fps, (width, height))

            # Process each movement
            for move in movements:
                # Draw frame content
                screen.fill((255, 255, 255))  # White background
                font = pygame.font.Font(None, 36)
                text = font.render(move['movement'], True, (0, 0, 0))
                screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))

                # Convert Pygame surface to OpenCV-compatible format
                frame = pygame.surfarray.array3d(screen)
                frame = cv2.transpose(frame)  # Transpose for correct orientation
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
                out.write(frame)  # Write frame to video

            # Finalize and clean up
            out.release()
            pygame.quit()

            logger.info(f"Video saved to {video_path}")
            return str(video_path)

        except Exception as e:
            logger.error(f"Error in Pygame video generation: {str(e)}", exc_info=True)
            raise

def get_video_generator(generator_type: str) -> VideoGenerator:
    """Factory function to get the appropriate video generator."""
    generators = {
        "replicate": None,  # Placeholder for other generator types
        "pygame": PygameGenerator(),
    }
    generator = generators.get(generator_type)
    if not generator:
        raise ValueError(f"Unknown generator type: {generator_type}")
    return generator

# if __name__ == "__main__":
#     # Example test for PygameGenerator
#     movements = [{"movement": "Spin"}, {"movement": "Jump"}, {"movement": "Slide"}]
#     generator = PygameGenerator()
#     video_path = generator.generate(movements)
#     print(f"Generated video path: {video_path}")