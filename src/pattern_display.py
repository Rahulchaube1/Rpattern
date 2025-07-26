"""
🎨 RPattern Dynamic Display - Animated Visual Patterns
Author: Rahul Chaube
Vision: Beautiful, animated patterns that pulse and dance

This module handles the real-time display of dynamic RPatterns.
"""

import pygame
import sys
import time
import threading
import math
from typing import Dict, Any, List, Tuple, Optional
from rpattern_revolutionary import RPatternCore, create_revolutionary_pattern


class RPatternAnimator:
    """
    Revolutionary animated display system for RPatterns.
    Creates beautiful, pulsing, dynamic visual patterns.
    """
    
    def __init__(self, window_size: Tuple[int, int] = (900, 700)):
        """Initialize the revolutionary display."""
        pygame.init()
        
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("🚀 RPattern Revolutionary Display - by Rahul Chaube")
        
        # Set icon
        pygame.display.set_icon(pygame.Surface((32, 32)))
        
        # Pattern display area
        self.pattern_size = 500  # Large pattern area
        self.pattern_rect = pygame.Rect(
            (window_size[0] - self.pattern_size) // 2,
            50,  # Top margin
            self.pattern_size,
            self.pattern_size
        )
        
        # Grid configuration
        self.grid_size = 4  # 4x4 grid
        self.cell_size = self.pattern_size // self.grid_size
        self.cell_margin = 4  # Space between cells
        
        # Fonts
        try:
            self.font_title = pygame.font.Font(None, 36)
            self.font_info = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)
        except:
            self.font_title = pygame.font.SysFont('Arial', 36, bold=True)
            self.font_info = pygame.font.SysFont('Arial', 24)
            self.font_small = pygame.font.SysFont('Arial', 18)
        
        # Colors
        self.bg_color = (10, 10, 20)  # Dark space blue
        self.text_color = (255, 255, 255)
        self.accent_color = (0, 255, 150)  # Bright green
        self.info_color = (100, 200, 255)  # Light blue
        
        # Animation state
        self.current_frame = 0
        self.animation_time = 0
        self.is_playing = False
        self.pattern_data = None
        self.last_frame_time = 0
        
        # Visual effects
        self.pulse_amplitude = 0.2  # Pulsing effect
        self.glow_intensity = 0
        self.rainbow_shift = 0
        
        # Performance tracking
        self.fps_counter = 0
        self.last_fps_time = time.time()
        self.current_fps = 0
        
        print("🎨 RPattern Animator initialized")
        print(f"📺 Display Size: {window_size}")
        print(f"🎬 Pattern Area: {self.pattern_size}x{self.pattern_size}")
    
    def load_pattern(self, pattern_data: Dict[str, Any]):
        """Load a revolutionary pattern for display."""
        self.pattern_data = pattern_data
        self.current_frame = 0
        self.animation_time = 0
        self.is_playing = True
        
        print(f"🎬 Pattern loaded: {pattern_data.get('pattern_id', 'Unknown')}")
        print(f"📊 Frames: {pattern_data.get('total_frames', 0)}")
        print(f"⏱️ Duration: {pattern_data.get('frame_duration', 0.3)}s per frame")
    
    def create_and_load_pattern(self, data: str, expiry_seconds: int = 60):
        """Create and load a pattern in one step."""
        print(f"🔥 Creating pattern for: {data[:50]}...")
        
        try:
            pattern = create_revolutionary_pattern(data, expiry_seconds, "MILITARY")
            self.load_pattern(pattern)
            return True
        except Exception as e:
            print(f"❌ Failed to create pattern: {e}")
            return False
    
    def _apply_visual_effects(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Apply visual effects to colors."""
        r, g, b = color
        
        # Pulsing effect
        pulse_factor = 1 + self.pulse_amplitude * math.sin(self.animation_time * 3)
        
        # Glow effect
        glow_factor = 1 + self.glow_intensity * 0.3
        
        # Apply effects
        r = min(255, int(r * pulse_factor * glow_factor))
        g = min(255, int(g * pulse_factor * glow_factor))
        b = min(255, int(b * pulse_factor * glow_factor))
        
        return (r, g, b)
    
    def _draw_pattern_cell(self, cell_color: Tuple[int, int, int], x: int, y: int):
        """Draw a single pattern cell with effects."""
        # Calculate cell position
        cell_x = self.pattern_rect.x + x * self.cell_size + self.cell_margin
        cell_y = self.pattern_rect.y + y * self.cell_size + self.cell_margin
        cell_w = self.cell_size - 2 * self.cell_margin
        cell_h = self.cell_size - 2 * self.cell_margin
        
        # Apply visual effects
        enhanced_color = self._apply_visual_effects(cell_color)
        
        # Create cell rectangle
        cell_rect = pygame.Rect(cell_x, cell_y, cell_w, cell_h)
        
        # Draw cell with rounded corners effect
        pygame.draw.rect(self.screen, enhanced_color, cell_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), cell_rect, 2)  # White border
        
        # Add glow effect for bright colors
        if sum(enhanced_color) > 400:  # Bright colors
            glow_rect = pygame.Rect(cell_x - 2, cell_y - 2, cell_w + 4, cell_h + 4)
            glow_color = tuple(min(255, c + 30) for c in enhanced_color)
            pygame.draw.rect(self.screen, glow_color, glow_rect, 4)
    
    def _draw_pattern_frame(self):
        """Draw the current pattern frame."""
        if not self.pattern_data or not self.pattern_data.get('frames'):
            return
        
        frames = self.pattern_data['frames']
        if self.current_frame >= len(frames):
            return
        
        current_pattern = frames[self.current_frame]
        
        # Draw each cell in the pattern
        for y in range(len(current_pattern)):
            for x in range(len(current_pattern[y])):
                cell_color = current_pattern[y][x]
                self._draw_pattern_cell(cell_color, x, y)
    
    def _draw_ui_info(self):
        """Draw UI information and controls."""
        y_offset = self.pattern_rect.bottom + 20
        
        if self.pattern_data:
            # Pattern info
            pattern_id = self.pattern_data.get('pattern_id', 'Unknown')
            title_text = self.font_title.render(f"🚀 RPattern: {pattern_id}", True, self.accent_color)
            self.screen.blit(title_text, (20, y_offset))
            y_offset += 40
            
            # Frame info
            total_frames = self.pattern_data.get('total_frames', 0)
            frame_info = f"Frame: {self.current_frame + 1}/{total_frames}"
            frame_text = self.font_info.render(frame_info, True, self.text_color)
            self.screen.blit(frame_text, (20, y_offset))
            y_offset += 30
            
            # Security info
            security_level = self.pattern_data.get('security_level', 'UNKNOWN')
            encryption = self.pattern_data.get('encryption', 'UNKNOWN')
            security_text = f"🛡️ Security: {security_level} | 🔒 Encryption: {encryption}"
            security_surface = self.font_info.render(security_text, True, self.info_color)
            self.screen.blit(security_surface, (20, y_offset))
            y_offset += 30
            
            # Timing info
            current_time = int(time.time() * 1000)
            expiry_time = self.pattern_data.get('expiry', 0)
            time_left = max(0, (expiry_time - current_time) / 1000)
            
            if time_left > 0:
                time_text = f"⏰ Expires in: {time_left:.1f}s"
                time_color = self.accent_color if time_left > 10 else (255, 150, 0)
            else:
                time_text = "⏰ EXPIRED"
                time_color = (255, 50, 50)
            
            time_surface = self.font_info.render(time_text, True, time_color)
            self.screen.blit(time_surface, (20, y_offset))
        else:
            # No pattern loaded
            no_pattern_text = self.font_title.render("No Pattern Loaded", True, (150, 150, 150))
            self.screen.blit(no_pattern_text, (20, y_offset))
        
        # FPS counter
        fps_text = self.font_small.render(f"FPS: {self.current_fps:.1f}", True, (150, 150, 150))
        self.screen.blit(fps_text, (self.window_size[0] - 100, 20))
        
        # Controls
        controls = [
            "SPACE: Play/Pause",
            "R: Reset",
            "ESC: Exit",
            "Created by Rahul Chaube 🚀"
        ]
        
        y_pos = self.window_size[1] - 100
        for control in controls:
            color = self.accent_color if "Rahul" in control else (150, 150, 150)
            control_text = self.font_small.render(control, True, color)
            self.screen.blit(control_text, (20, y_pos))
            y_pos += 20
    
    def _update_animation(self, dt: float):
        """Update animation state."""
        if not self.is_playing or not self.pattern_data:
            return
        
        self.animation_time += dt
        
        # Update visual effects
        self.pulse_amplitude = 0.1 + 0.1 * math.sin(self.animation_time * 2)
        self.glow_intensity = 0.5 + 0.3 * math.sin(self.animation_time * 1.5)
        self.rainbow_shift += dt * 50
        
        # Frame advancement
        frame_duration = self.pattern_data.get('frame_duration', 0.3)
        
        if time.time() - self.last_frame_time >= frame_duration:
            total_frames = self.pattern_data.get('total_frames', 1)
            self.current_frame = (self.current_frame + 1) % total_frames
            self.last_frame_time = time.time()
    
    def _update_fps(self):
        """Update FPS counter."""
        self.fps_counter += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:  # Update every second
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.last_fps_time = current_time
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif event.key == pygame.K_SPACE:
                    self.is_playing = not self.is_playing
                    print(f"{'▶️' if self.is_playing else '⏸️'} Animation {'playing' if self.is_playing else 'paused'}")
                
                elif event.key == pygame.K_r:
                    self.current_frame = 0
                    self.animation_time = 0
                    print("🔄 Animation reset")
                
                elif event.key == pygame.K_n:
                    # Next frame
                    if self.pattern_data:
                        total_frames = self.pattern_data.get('total_frames', 1)
                        self.current_frame = (self.current_frame + 1) % total_frames
                
                elif event.key == pygame.K_p:
                    # Previous frame
                    if self.pattern_data:
                        total_frames = self.pattern_data.get('total_frames', 1)
                        self.current_frame = (self.current_frame - 1) % total_frames
        
        return True
    
    def run_display(self, pattern_data: Dict[str, Any] = None):
        """Run the main display loop."""
        if pattern_data:
            self.load_pattern(pattern_data)
        
        clock = pygame.time.Clock()
        running = True
        last_time = time.time()
        
        print("🎬 Starting RPattern display...")
        print("🎮 Controls: SPACE=Play/Pause, R=Reset, N=Next Frame, P=Prev Frame, ESC=Exit")
        
        while running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Handle events
            running = self.handle_events()
            
            # Update animation
            self._update_animation(dt)
            
            # Clear screen
            self.screen.fill(self.bg_color)
            
            # Draw pattern
            self._draw_pattern_frame()
            
            # Draw UI
            self._draw_ui_info()
            
            # Update display
            pygame.display.flip()
            
            # Update FPS
            self._update_fps()
            
            # Control frame rate
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
        print("✅ RPattern display closed")


def display_pattern(data: str, expiry_seconds: int = 60):
    """Quick function to create and display a pattern."""
    animator = RPatternAnimator()
    
    if animator.create_and_load_pattern(data, expiry_seconds):
        animator.run_display()
    else:
        print("❌ Failed to create pattern")


if __name__ == "__main__":
    print("🎨" * 20)
    print("    RPATTERN REVOLUTIONARY DISPLAY")
    print("    Creator: Rahul Chaube")
    print("    Dynamic, Animated, Beautiful!")
    print("🎨" * 20)
    
    # Demo patterns
    demo_patterns = [
        "https://rahulchaube.dev - Revolutionary Portfolio",
        "upi://pay?pa=rahul@paytm&pn=Rahul%20Chaube&am=1000",
        "Welcome to RPattern Revolution! 🚀🔥",
        "DEMO: Military-Grade Visual Patterns by Rahul Chaube",
        "SECRET_ACCESS_CODE_2024_RPATTERN_DEMO"
    ]
    
    print("\n🚀 Select a demo pattern:")
    for i, pattern in enumerate(demo_patterns, 1):
        print(f"  {i}. {pattern[:60]}...")
    
    print(f"  0. Enter custom data")
    
    try:
        choice = input("\n🔥 Choose pattern (1-5, 0 for custom): ").strip()
        
        if choice == "0":
            custom_data = input("💬 Enter your data: ")
            data_to_display = custom_data
        elif choice.isdigit() and 1 <= int(choice) <= len(demo_patterns):
            data_to_display = demo_patterns[int(choice) - 1]
        else:
            print("🎯 Using default demo...")
            data_to_display = demo_patterns[0]
        
        print(f"\n🔥 Creating revolutionary pattern for: {data_to_display}")
        display_pattern(data_to_display, expiry_seconds=120)
        
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n🎉 Thank you for experiencing RPattern Revolution!")
    print("💎 Created by Rahul Chaube")
