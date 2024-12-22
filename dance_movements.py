from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Position:
    head: Tuple[int, int]
    body: Tuple[int, int]
    arms: List[Tuple[int, int]]
    legs: List[Tuple[int, int]]

class DanceMovements:
    @staticmethod
    def calculate_positions(center: Tuple[int, int], head_radius: int = 15, 
                          body_length: int = 40, limb_length: int = 30) -> Dict[str, Position]:
        """Calculate all possible positions based on center point"""
        x, y = center
        positions = {
            # === TAP DANCE POSITIONS ===
            # Step 1
            "tap_feet_together": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length)]
            ),
            "tap_right_forward": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 30, y + body_length + limb_length - 10)]
            ),
            
            # Step 2
            "right_foot_forward": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 25, y + body_length + limb_length)]
            ),
            "left_side_tap": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 30, y + body_length + limb_length),
                     (x + 25, y + body_length + limb_length)]
            ),
            
            # Step 3
            "left_foot_side": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 30, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length)]
            ),
            "right_back_tap": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length + 20)]
            ),
            
            # Step 4
            "right_foot_back": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length + 15)]
            ),
            "left_tap_in_place": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 10, y + body_length + limb_length - 10),
                     (x + 10, y + body_length + limb_length + 15)]
            ),
            
            # Step 5
            "heels_click": Position(
                head=(x, y - 15),  # Jump height
                body=(x, y - 15 + body_length),
                arms=[(x - limb_length * 1.1, y - 15), (x + limb_length * 1.1, y - 15)],
                legs=[(x - 5, y - 15 + body_length + limb_length),
                     (x + 5, y - 15 + body_length + limb_length)]
            ),

            # === BROADWAY POSITIONS ===
            # Step 1
            "feet_hip_width": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 20, y + body_length + limb_length),
                     (x + 20, y + body_length + limb_length)]
            ),
            "left_step_right_arm": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 0.5, y), (x + limb_length * 1.2, y - 10)],
                legs=[(x - 20, y + body_length + limb_length),
                     (x + 30, y + body_length + limb_length)]
            ),
            
            # Step 2
            "left_forward_arm_extended": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 0.5, y), (x + limb_length * 1.2, y)],
                legs=[(x - 30, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length)]
            ),
            "right_step_slide": Position(
                head=(x, y),
                body=(x + 10, y + body_length),
                arms=[(x - limb_length, y + 10), (x + limb_length * 0.8, y + 15)],
                legs=[(x - 15, y + body_length + limb_length),
                     (x + 25, y + body_length + limb_length - 5)]
            ),
            
            # Step 3
            "body_twist_left": Position(
                head=(x - 5, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 1.2, y), (x + limb_length * 0.8, y - 10)],
                legs=[(x - 20, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length)]
            ),
            "arm_swing": Position(
                head=(x - 5, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 0.8, y), (x + limb_length * 1.2, y - 15)],
                legs=[(x - 20, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length)]
            ),
            
            # Step 4
            "spin_prep": Position(
                head=(x - 5, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y - 5), (x + limb_length, y - 5)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length)]
            ),
            "spin_180": Position(
                head=(x, y - 10),
                body=(x, y - 10 + body_length),
                arms=[(x - limb_length * 1.1, y - 10), (x + limb_length * 1.1, y - 10)],
                legs=[(x - 5, y - 10 + body_length + limb_length),
                     (x + 5, y - 10 + body_length + limb_length)]
            ),
            
            # Step 5
            "arms_up_leap": Position(
                head=(x, y - 20),
                body=(x, y - 20 + body_length),
                arms=[(x - limb_length * 1.1, y - 25), (x + limb_length * 1.1, y - 25)],
                legs=[(x - 30, y - 20 + body_length + limb_length),
                     (x + 30, y - 20 + body_length + limb_length)]
            ),

            # === HIP HOP POSITIONS ===
            # Step 1
            "cross_right_swing": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x + limb_length * 0.8, y), (x + limb_length * 1.2, y)],
                legs=[(x + 15, y + body_length + limb_length),
                     (x - 20, y + body_length + limb_length)]
            ),
            
            # Step 2
            "jump_apart_clap": Position(
                head=(x, y - 15),
                body=(x, y - 15 + body_length),
                arms=[(x - limb_length * 0.5, y - 25), (x + limb_length * 0.5, y - 25)],
                legs=[(x - 25, y - 15 + body_length + limb_length),
                     (x + 25, y - 15 + body_length + limb_length)]
            ),
            
            # Step 3
            "right_back_arms_down": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 0.8, y + 20), (x + limb_length * 0.8, y + 20)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 25, y + body_length + limb_length)]
            ),
            
            # Step 4
            "slide_push": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 0.5, y - 5), (x + limb_length * 0.5, y - 5)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length)]
            ),
            
            # Step 5
            "jump_apart_arms_side": Position(
                head=(x, y - 15),
                body=(x, y - 15 + body_length),
                arms=[(x - limb_length * 1.2, y - 15), (x + limb_length * 1.2, y - 15)],
                legs=[(x - 25, y - 15 + body_length + limb_length),
                     (x + 25, y - 15 + body_length + limb_length)]
            ),

            # === CONTEMPORARY POSITIONS ===
            # Step 1
            "feet_shoulder_width": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length, y), (x + limb_length, y)],
                legs=[(x - 15, y + body_length + limb_length),
                     (x + 15, y + body_length + limb_length)]
            ),
            "raise_arm_pivot": Position(
                head=(x - 5, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 0.5, y), (x + limb_length * 0.8, y - 20)],
                legs=[(x - 15, y + body_length + limb_length),
                     (x + 15, y + body_length + limb_length)]
            ),
            
            # Step 2
            "step_back_extend": Position(
                head=(x - 5, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 0.5, y), (x + limb_length * 1.2, y - 10)],
                legs=[(x - 30, y + body_length + limb_length),
                     (x + 10, y + body_length + limb_length)]
            ),
            
            # Step 3
            "weight_shift": Position(
                head=(x - 10, y),
                body=(x - 5, y + body_length),
                arms=[(x - limb_length * 1.2, y + 10), (x + limb_length * 0.8, y - 15)],
                legs=[(x - 20, y + body_length + limb_length - 5),
                     (x + 5, y + body_length + limb_length)]
            ),
            
            # Step 4
            "step_right_arms_side": Position(
                head=(x, y),
                body=(x, y + body_length),
                arms=[(x - limb_length * 1.1, y), (x + limb_length * 1.1, y)],
                legs=[(x - 10, y + body_length + limb_length),
                     (x + 25, y + body_length + limb_length)]
            ),
            
            # Step 5
            "leap_execute": Position(
                head=(x, y - 20),
                body=(x, y - 20 + body_length),
                arms=[(x - limb_length * 1.1, y - 25), (x + limb_length * 1.1, y - 25)],
                legs=[(x - 30, y - 20 + body_length + limb_length),
                     (x + 30, y - 20 + body_length + limb_length)]
            ),
        }
        return positions

    TAP_DANCE = [
        {
            "position": "Standing with feet together, arms relaxed at sides",
            "movement": "Tap right foot forward twice with precise, sharp movements, keeping upper body straight and arms steady",
            "timing": "2.0",
            "frames": ["tap_feet_together", "tap_right_forward", "tap_feet_together", "tap_right_forward"]
        },
        {
            "position": "Right foot forward, weight balanced",
            "movement": "Maintain posture while tapping left foot to the side twice, creating clear rhythmic sounds",
            "timing": "2.0",
            "frames": ["right_foot_forward", "left_side_tap", "right_foot_forward", "left_side_tap"]
        },
        {
            "position": "Left foot to the side",
            "movement": "Bring left foot back in and tap right foot back twice",
            "timing": "2.0",
            "frames": ["left_foot_side", "right_back_tap", "left_foot_side", "right_back_tap"]
        },
        {
            "position": "Right foot back",
            "movement": "Tap left foot in place twice",
            "timing": "2.0",
            "frames": ["right_foot_back", "left_tap_in_place", "right_foot_back", "left_tap_in_place"]
        },
        {
            "position": "Left foot in place",
            "movement": "Jump and click heels together twice",
            "timing": "2.0",
            "frames": ["tap_feet_together", "heels_click", "tap_feet_together", "heels_click"]
        }
    ]

    BROADWAY = [
        {
            "position": "Standing confidently with feet hip-width apart, shoulders back",
            "movement": "Step left foot forward with theatrical flair while extending right arm forward in a smooth, dramatic gesture",
            "timing": "2.0",
            "frames": ["feet_hip_width", "left_step_right_arm"]
        },
        {
            "position": "Left foot forward, right arm extended",
            "movement": "Bring right arm down and step right foot forward, sliding left foot back",
            "timing": "2.0",
            "frames": ["left_forward_arm_extended", "right_step_slide"]
        },
        {
            "position": "Right foot forward, left foot back",
            "movement": "Twist body to left while swinging right arm around",
            "timing": "3.0",
            "frames": ["body_twist_left", "arm_swing"]
        },
        {
            "position": "Twisted to left, right arm extended",
            "movement": "Jump and spin 180 degrees to the right, landing with feet together",
            "timing": "4.0",
            "frames": ["spin_prep", "spin_180"]
        },
        {
            "position": "Standing with feet together",
            "movement": "Extend both arms up and leap forward with right foot",
            "timing": "3.0",
            "frames": ["spin_180", "arms_up_leap"]
        }
    ]

    HIP_HOP = [
        {
            "position": "Athletic stance with feet hip-width apart, knees slightly bent",
            "movement": "Cross right foot over left with swagger, while swinging both arms to the right in a smooth, controlled motion",
            "timing": "2.0",
            "frames": ["feet_hip_width", "cross_right_swing"]
        },
        {
            "position": "Right foot crossed over left",
            "movement": "Jump feet apart and clap hands above head",
            "timing": "2.0",
            "frames": ["cross_right_swing", "jump_apart_clap"]
        },
        {
            "position": "Standing with feet apart, hands clapped above head",
            "movement": "Step right foot back and swing arms down",
            "timing": "2.0",
            "frames": ["jump_apart_clap", "right_back_arms_down"]
        },
        {
            "position": "Right foot back, arms down",
            "movement": "Slide left foot to meet right and push hands forward",
            "timing": "2.0",
            "frames": ["right_back_arms_down", "slide_push"]
        },
        {
            "position": "Feet together, hands pushed forward",
            "movement": "Jump feet apart and swing arms to the sides",
            "timing": "2.0",
            "frames": ["slide_push", "jump_apart_arms_side"]
        }
    ]

    CONTEMPORARY = [
        {
            "position": "Grounded stance with feet shoulder-width apart, body centered",
            "movement": "Fluidly raise right arm overhead while pivoting body left, maintaining graceful control",
            "timing": "2.0",
            "frames": ["feet_shoulder_width", "raise_arm_pivot"]
        },
        {
            "position": "Standing with body pivoted left",
            "movement": "Step left foot back and extend right arm forward",
            "timing": "2.0",
            "frames": ["raise_arm_pivot", "step_back_extend"]
        },
        {
            "position": "Standing with left foot behind right",
            "movement": "Swing right arm back and left arm forward, shift weight to left foot",
            "timing": "3.0",
            "frames": ["step_back_extend", "weight_shift"]
        },
        {
            "position": "Standing with weight on left foot",
            "movement": "Step right foot forward, swing arms to the sides",
            "timing": "2.0",
            "frames": ["weight_shift", "step_right_arms_side"]
        },
        {
            "position": "Standing with right foot forward",
            "movement": "Leap forward, extending both arms upward",
            "timing": "4.0",
            "frames": ["step_right_arms_side", "leap_execute"]
        }
    ] 