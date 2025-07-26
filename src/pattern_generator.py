"""
RPattern Generator and Display
Creator: Rahul Chaube 🚀

Generates and displays animated RPatterns using Pygame.
"""

import pygame
import sys
import time
import threading
from typing import Dict, Any, List, Tuple
from rpattern_core import RPattern, create_test_pattern


class RPatternDisplay:
    """Handles the visual display of RPatterns with animations."""
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600)):
        """Initialize the display window."""
        pygame.init()
        
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("🚀 RPattern Generator - by Rahul Chaube")
        
        # Pattern display area (centered square)
        self.pattern_size = min(window_size) - 100
        self.pattern_rect = pygame.Rect(
            (window_size[0] - self.pattern_size) // 2,
            (window_size[1] - self.pattern_size) // 2,
            self.pattern_size,
            self.pattern_size
        )
        
        # Cell size for pattern grid
        self.cell_size = self.pattern_size // 3  # 3x3 grid
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Colors
        self.bg_color = (20, 20, 30)  # Dark blue background
        self.text_color = (255, 255, 255)
        self.accent_color = (0, 255, 150)  # Bright green
        
        # Animation state
        self.current_frame = 0
        self.last_frame_time = 0
        self.pattern_data = None
        self.is_playing = False
        self.loop_pattern = True
        
    def load_pattern(self, pattern_data: Dict[str, Any]):
        """Load a pattern for display."""
        self.pattern_data = pattern_data
        self.current_frame = 0
        self.last_frame_time = time.time()
        
    def start_animation(self):
        """Start the pattern animation."""
        self.is_playing = True
        self.last_frame_time = time.time()
        
    def stop_animation(self):
        """Stop the pattern animation."""
        self.is_playing = False
        
    def update_animation(self):
        """Update the animation frame."""
        if not self.is_playing or not self.pattern_data:
            return
            
        current_time = time.time()
        frame_duration = self.pattern_data['frame_duration']
        
        if current_time - self.last_frame_time >= frame_duration:
            self.current_frame += 1
            if self.current_frame >= len(self.pattern_data['frames']):
                if self.loop_pattern:
                    self.current_frame = 0
                else:
                    self.stop_animation()
            self.last_frame_time = current_time
            
    def draw_pattern_frame(self):
        """Draw the current pattern frame."""
        if not self.pattern_data or self.current_frame >= len(self.pattern_data['frames']):
            return
            
        frame = self.pattern_data['frames'][self.current_frame]
        
        # Draw the 3x3 grid
        for row in range(3):
            for col in range(3):
                color = frame[row][col]
                
                # Calculate cell position
                x = self.pattern_rect.x + col * self.cell_size
                y = self.pattern_rect.y + row * self.cell_size
                
                # Draw cell with padding
                padding = 5
                cell_rect = pygame.Rect(x + padding, y + padding, 
                                      self.cell_size - 2*padding, 
                                      self.cell_size - 2*padding)
                
                pygame.draw.rect(self.screen, color, cell_rect)
                pygame.draw.rect(self.screen, (100, 100, 100), cell_rect, 2)
                
    def draw_info_panel(self):
        """Draw information panel."""
        if not self.pattern_data:
            return
            
        # RPattern info
        rpattern = RPattern()
        info = rpattern.get_pattern_info(self.pattern_data)
        
        # Title
        title_text = self.font_large.render("🚀 RPattern Active", True, self.accent_color)
        title_rect = title_text.get_rect(centerx=self.window_size[0]//2, y=20)
        self.screen.blit(title_text, title_rect)
        
        # Pattern info
        info_y = self.pattern_rect.bottom + 20
        
        frame_info = f"Frame: {self.current_frame + 1}/{info['total_frames']}"
        frame_text = self.font_medium.render(frame_info, True, self.text_color)
        frame_rect = frame_text.get_rect(centerx=self.window_size[0]//2, y=info_y)
        self.screen.blit(frame_text, frame_rect)
        
        # Time remaining
        time_info = f"Expires in: {info['time_remaining_seconds']}s"
        time_color = self.text_color if info['time_remaining_seconds'] > 30 else (255, 100, 100)
        time_text = self.font_small.render(time_info, True, time_color)
        time_rect = time_text.get_rect(centerx=self.window_size[0]//2, y=info_y + 40)
        self.screen.blit(time_text, time_rect)
        
        # Encryption status
        encrypt_info = "🔐 Encrypted" if info['encrypted'] else "📝 Plain Text"
        encrypt_text = self.font_small.render(encrypt_info, True, self.accent_color)
        encrypt_rect = encrypt_text.get_rect(centerx=self.window_size[0]//2, y=info_y + 70)
        self.screen.blit(encrypt_text, encrypt_rect)
        
        # Instructions
        instructions = [
            "🎯 Point camera at this pattern to scan",
            "⏸️  Press SPACE to pause/resume",
            "🔄 Press R to restart pattern",
            "❌ Press ESC to exit"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, (180, 180, 180))
            inst_rect = inst_text.get_rect(x=20, y=self.window_size[1] - 100 + i*20)
            self.screen.blit(inst_text, inst_rect)
            
    def draw_pattern_border(self):
        """Draw a futuristic border around the pattern."""
        # Outer glow effect
        for i in range(10):
            alpha = 255 - i * 20
            if alpha > 0:
                glow_rect = pygame.Rect(
                    self.pattern_rect.x - i,
                    self.pattern_rect.y - i,
                    self.pattern_rect.width + 2*i,
                    self.pattern_rect.height + 2*i
                )
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
                glow_surface.set_alpha(alpha // 10)
                glow_surface.fill(self.accent_color)
                self.screen.blit(glow_surface, glow_rect)
                
        # Main border
        pygame.draw.rect(self.screen, self.accent_color, self.pattern_rect, 3)
        
    def run(self, data: str = "https://rahulcodes.in"):
        """Run the pattern display application."""
        print(f"🚀 Generating RPattern for: {data}")
        
        # Generate pattern
        rpattern = RPattern(expiry_minutes=5)
        pattern_data = rpattern.encode_data(data, use_encryption=True)
        
        self.load_pattern(pattern_data)
        self.start_animation()
        
        print(f"✅ Pattern generated with {pattern_data['total_frames']} frames")
        print("🎯 Display window opened - point your camera at the pattern!")
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        if self.is_playing:
                            self.stop_animation()
                        else:
                            self.start_animation()
                    elif event.key == pygame.K_r:
                        self.current_frame = 0
                        self.start_animation()
                        
            # Update animation
            self.update_animation()
            
            # Clear screen
            self.screen.fill(self.bg_color)
            
            # Draw pattern border
            self.draw_pattern_border()
            
            # Draw pattern
            self.draw_pattern_frame()
            
            # Draw info
            self.draw_info_panel()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
            
        pygame.quit()


class RPatternGenerator:
    """Main class for generating RPatterns."""
    
    @staticmethod
    def generate_pattern(data: str, expiry_minutes: int = 5, use_encryption: bool = True) -> Dict[str, Any]:
        """Generate an RPattern for the given data."""
        rpattern = RPattern(expiry_minutes=expiry_minutes)
        return rpattern.encode_data(data, use_encryption=use_encryption)
    
    @staticmethod
    def display_pattern(data: str, window_size: Tuple[int, int] = (800, 600)):
        """Generate and display an RPattern."""
        display = RPatternDisplay(window_size)
        display.run(data)
    
    @staticmethod
    def save_pattern_info(pattern_data: Dict[str, Any], filename: str = "rpattern_info.json"):
        """Save pattern information to a file."""
        import json
        
        rpattern = RPattern()
        info = rpattern.get_pattern_info(pattern_data)
        
        with open(filename, 'w') as f:
            json.dump({
                'pattern_info': info,
                'total_frames': pattern_data['total_frames'],
                'frame_duration': pattern_data['frame_duration']
            }, f, indent=2)
            
        print(f"💾 Pattern info saved to {filename}")


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="🚀 RPattern Generator by Rahul Chaube")
    parser.add_argument("--data", "-d", default="https://rahulcodes.in", 
                       help="Data to encode in the pattern")
    parser.add_argument("--expiry", "-e", type=int, default=5,
                       help="Expiry time in minutes")
    parser.add_argument("--no-encryption", action="store_true",
                       help="Disable encryption")
    parser.add_argument("--size", "-s", nargs=2, type=int, default=[800, 600],
                       help="Window size (width height)")
    
    args = parser.parse_args()
    
    print("🚀 RPattern Generator - Next-Gen Visual ID System")
    print(f"Creator: Rahul Chaube")
    print(f"Data: {args.data}")
    print(f"Expiry: {args.expiry} minutes")
    print(f"Encryption: {'Enabled' if not args.no_encryption else 'Disabled'}")
    print("-" * 50)
    
    # Generate and display pattern
    RPatternGenerator.display_pattern(
        data=args.data,
        window_size=tuple(args.size)
    )


if __name__ == "__main__":
    main()
