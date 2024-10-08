import random, math
from src.Brick import Brick
from src.constants import WIDTH, HEIGHT

# Define phase ranges
PHASE_1 = (1, 10)
PHASE_2 = (11, 20)
PHASE_3 = (21, float('inf'))  # Levels 21+

class LevelMaker:
    previous_strength = 5  # Track strength from the previous level

    @classmethod
    def control_strength_increase(cls, current_strength, max_increase=random.randint(5, 20)):
        """Control the increase in total brick strength."""
        min_strength = cls.previous_strength
        max_strength = min_strength + max_increase
        if current_strength < min_strength:
            current_strength = min_strength
        elif current_strength > max_strength:
            current_strength = max_strength
        return current_strength
    
    @classmethod
    def CreateMap(cls, level):
        while True:
            bricks = []
            current_strength = 0  # Track total strength for the current level
            
            # Adjust for Level 1 and ensure bricks are generated
            if level == 1:
                num_rows = random.randint(1,3)  # Ensure minimum rows for level 1
                num_cols = random.randint(4,7)  # Ensure minimum columns for level 1
                patterns = ['normal', 'staggered']  # Default patterns for phase 1
            else:
                num_rows, num_cols, patterns = cls.get_phase_params(level)

            # Ensure odd number of columns for symmetry
            if num_cols % 2 == 0:
                num_cols += 1

            highest_tier = min(3, math.floor(level / 5.0))  # max tier = 3
            highest_color = min(5, level % 5 + 3)  # max color = 5

            # Choose a pattern based on the phase
            pattern = random.choice(patterns)

            print(f"Level: {level}, Rows: {num_rows}, Cols: {num_cols}, Pattern: {pattern}")

            # Calculate center offset
            center_x = WIDTH // 2
            center_y = HEIGHT // 2
            map_width = num_cols * 96
            map_height = num_rows * 48

            offset_x = center_x - (map_width // 2)
            offset_y = center_y - (map_height // 2)

            for y in range(num_rows):
                for x in range(num_cols):
                    if pattern == 'normal':
                        brick = cls.generate_normal_patterns(x, y, highest_tier, highest_color)
                        if brick:
                            # Center the brick
                            brick.x += offset_x
                            brick.y += offset_y
                            bricks.append(brick)
                    elif pattern == 'staggered':
                        # Create staggered brick row (every other brick offset)
                        offset_x_staggered = x + (y % 2) * 48
                        brick = cls.generate_solid_pattern(offset_x_staggered, y, highest_tier, highest_color)
                        if brick:
                            # Center the brick
                            brick.x += offset_x
                            brick.y += offset_y
                            bricks.append(brick)
                    elif pattern == 'hollow_rectangle' and cls.in_rectangle_bounds(x, y, num_rows, num_cols):
                        brick = cls.generate_solid_pattern(x, y, highest_tier, highest_color)
                        if brick:
                            # Center the brick
                            brick.x += offset_x
                            brick.y += offset_y
                            bricks.append(brick)
                    elif pattern == 'zigzag' and y % 2 == 0:
                        brick = cls.generate_solid_pattern(x, y, highest_tier, highest_color)
                        if brick:
                            # Center the brick
                            brick.x += offset_x
                            brick.y += offset_y
                            bricks.append(brick)
                    elif pattern == 'random_scatter' and random.choice([True, False]):
                        brick = cls.generate_solid_pattern(x, y, highest_tier, highest_color)
                        if brick:
                            # Center the brick
                            brick.x += offset_x
                            brick.y += offset_y
                            bricks.append(brick)
                    elif pattern == 'maze_like' and (x + y) % 3 == 0:
                        brick = cls.generate_solid_pattern(x, y, highest_tier, highest_color)
                        if brick:
                            # Center the brick
                            brick.x += offset_x
                            brick.y += offset_y
                            bricks.append(brick)
                    
                    # Track the total strength for each brick added
                    if bricks:
                        brick = bricks[-1]
                        brick_strength = cls.calculate_brick_strength(brick.tier, brick.color)
                        current_strength += brick_strength

            # Ensure total block strength has increased within controlled limits
            current_strength = cls.control_strength_increase(current_strength)
            if current_strength <= cls.previous_strength and level > 1:
                print(f"Retrying level {level} due to insufficient strength.")
            else:
                print(f"prev: {cls.previous_strength}, curr: {current_strength}")
                cls.previous_strength = current_strength
                return bricks

    @classmethod
    def get_phase_params(cls, level):
        """Determines number of rows, columns, and available patterns based on the level."""
        if PHASE_1[0] <= level <= PHASE_1[1]:
            num_rows = random.randint(1, 5)
            num_cols = random.randint(7, 13)
            patterns = ['normal', 'staggered']
        elif PHASE_2[0] <= level <= PHASE_2[1]:
            num_rows = random.randint(3, 6)
            num_cols = random.randint(9, 13)
            patterns = ['normal', 'staggered', 'hollow_rectangle', 'zigzag']
        else:  # PHASE_3 (Levels 21+)
            num_rows = random.randint(4, 7)
            num_cols = random.randint(11, 15)
            patterns = ['normal', 'staggered', 'hollow_rectangle', 'zigzag', 'random_scatter', 'maze_like']
        return num_rows, num_cols, patterns

    @classmethod
    def calculate_brick_strength(cls, tier, color):
        total_hits = 0
        
        # If tier is 0, the brick only has color hits, no additional tier-based strength
        if tier == 0:
            total_hits = color  # Just the color strength
        else:
            # For tiers greater than 0, we calculate hits based on tier and color
            for t in range(tier, -1, -1):  # Start from the current tier down to 0
                if t == tier:
                    total_hits += color  # For the top tier, use the current color
                else:
                    total_hits += 5  # For each lower tier, assume maximum color strength

        return total_hits
    
    @staticmethod
    def generate_normal_patterns(x, y, highest_tier, highest_color):
        """Generates bricks based on normal patterns."""
        patterns = ['solid', 'alternate', 'skip']
        pattern = random.choice(patterns)
        if pattern == 'solid':
            return LevelMaker.generate_solid_pattern(x, y, highest_tier, highest_color)
        elif pattern == 'alternate':
            return LevelMaker.generate_alternate_pattern(x, y, highest_tier, highest_color)
        elif pattern == 'skip':
            if x % 2 == 0:
                return None  # Skip this brick
            return LevelMaker.generate_solid_pattern(x, y, highest_tier, highest_color)

    @classmethod
    def generate_solid_pattern(cls, x, y, highest_tier, highest_color):
        """Generates a brick with a solid color and tier."""
        brick = Brick(x * 96 + 24, y * 48)
        brick.color = random.randint(1, highest_color)
        brick.tier = random.randint(0, highest_tier)
        return brick

    @classmethod
    def generate_alternate_pattern(cls, x, y, highest_tier, highest_color):
        """Generates bricks with alternating colors and tiers.""" 
        brick = Brick(x * 96 + 24, y * 48)
        if x % 2 == 0:
            brick.color = random.randint(1, highest_color)
            brick.tier = random.randint(0, highest_tier)
        else:
            brick.color = random.randint(1, highest_color)
            brick.tier = random.randint(0, highest_tier)
        return brick

    @classmethod
    def in_rectangle_bounds(cls, x, y, num_rows, num_cols):
        """Helper method to define the hollow rectangle bounds.""" 
        return (y == 0 or y == num_rows - 1 or x == 0 or x == num_cols - 1)

