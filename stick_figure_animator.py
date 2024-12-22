import pygame
import numpy as np
from typing import List, Dict, Tuple
from dance_movements import DanceMovements, Position

class StickFigureAnimator:
    def __init__(self, width=400, height=400):
        pygame.init()
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.center = (width // 2, height // 2)
        self.positions = DanceMovements.calculate_positions(self.center)
        
        # Define style-specific timing characteristics
        self.style_timing = {
            "Tap Dance": {
                "frames_per_beat": 15,    # Quick, sharp movements
                "hold_frames": 3,         # Short holds between taps
                "transition_speed": 1.2,  # Fast transitions
                "easing": self._tap_ease  # Sharp, bouncy easing
            },
            "Broadway": {
                "frames_per_beat": 20,    # Theatrical, flowing movements
                "hold_frames": 8,         # Longer holds for dramatic effect
                "transition_speed": 1.0,  # Standard transitions
                "easing": self._theatrical_ease  # Smooth, dramatic easing
            },
            "Hip Hop": {
                "frames_per_beat": 12,    # Sharp, rhythmic movements
                "hold_frames": 5,         # Medium holds for emphasis
                "transition_speed": 1.5,  # Very quick transitions
                "easing": self._hip_hop_ease  # Sharp with holds
            },
            "Contemporary": {
                "frames_per_beat": 25,    # Slow, fluid movements
                "hold_frames": 10,        # Long holds for artistic effect
                "transition_speed": 0.8,  # Slower transitions
                "easing": self._contemporary_ease  # Very smooth easing
            }
        }

    def interpolate_position(self, start_pos: Position, end_pos: Position, progress: float) -> Position:
        """Interpolate between two positions"""
        def lerp(p1: Tuple[int, int], p2: Tuple[int, int], t: float) -> Tuple[int, int]:
            return (int(p1[0] + (p2[0] - p1[0]) * t),
                   int(p1[1] + (p2[1] - p1[1]) * t))
        
        return Position(
            head=lerp(start_pos.head, end_pos.head, progress),
            body=lerp(start_pos.body, end_pos.body, progress),
            arms=[lerp(start_pos.arms[0], end_pos.arms[0], progress),
                  lerp(start_pos.arms[1], end_pos.arms[1], progress)],
            legs=[lerp(start_pos.legs[0], end_pos.legs[0], progress),
                  lerp(start_pos.legs[1], end_pos.legs[1], progress)]
        )

    def _tap_ease(self, t: float) -> float:
        """Sharp, bouncy easing for tap dance"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2

    def _theatrical_ease(self, t: float) -> float:
        """Smooth, dramatic easing for broadway"""
        return t * t * (3 - 2 * t)

    def _hip_hop_ease(self, t: float) -> float:
        """Sharp with holds for hip hop"""
        if t < 0.2:
            return 5 * t
        elif t > 0.8:
            return 5 * (t - 0.8) + 0.8
        else:
            return 1.0

    def _contemporary_ease(self, t: float) -> float:
        """Very smooth easing for contemporary"""
        return t * t * t * (t * (6 * t - 15) + 10)

    def create_animation(self, movements: List[Dict], dance_style: str) -> List[np.ndarray]:
        """Create animation frames with style-specific timing"""
        frames = []
        style_params = self.style_timing[dance_style]
        
        for movement in movements:
            # Get frames for this movement
            movement_frames = movement["frames"]
            timing = int(movement["timing"].split()[0])  # Extract number from "X beats"
            
            # Calculate frames based on style timing
            frames_per_transition = style_params["frames_per_beat"] * timing
            frames_per_transition = int(frames_per_transition * style_params["transition_speed"])
            
            # Create transitions between each pair of frames
            for i in range(len(movement_frames) - 1):
                start_pos = self.positions[movement_frames[i]]
                end_pos = self.positions[movement_frames[i + 1]]
                
                # Generate interpolated frames
                for frame in range(frames_per_transition):
                    progress = frame / (frames_per_transition - 1)
                    
                    # Apply style-specific easing
                    progress = style_params["easing"](progress)
                    
                    interpolated_pos = self.interpolate_position(start_pos, end_pos, progress)
                    self.surface.fill((255, 255, 255))
                    self._draw_stick_figure(interpolated_pos)
                    frames.append(pygame.surfarray.array3d(self.surface))
                
                # Add style-specific hold frames
                for _ in range(style_params["hold_frames"]):
                    frames.append(frames[-1].copy())
        
        return frames

    def _draw_stick_figure(self, pos: Position):
        """Draw stick figure with smooth lines and joints"""
        # Draw body
        pygame.draw.line(self.surface, (0, 0, 0), pos.head, pos.body, 2)
        
        # Draw head with a slight tilt based on movement
        pygame.draw.circle(self.surface, (0, 0, 0), pos.head, 15, 2)
        
        # Draw arms with rounded joints
        for arm in pos.arms:
            pygame.draw.line(self.surface, (0, 0, 0), 
                           (pos.head[0], pos.head[1] + 5), arm, 2)
            pygame.draw.circle(self.surface, (0, 0, 0), 
                             (pos.head[0], pos.head[1] + 5), 3)
        
        # Draw legs with rounded joints
        for leg in pos.legs:
            pygame.draw.line(self.surface, (0, 0, 0), pos.body, leg, 2)
            pygame.draw.circle(self.surface, (0, 0, 0), pos.body, 3)