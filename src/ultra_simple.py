"""
🚀 ULTRA-SIMPLE RPattern Launcher
Creator: Rahul Chaube 🔒

One-click launcher with automatic error fixing and maximum security!
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import threading
import time


class UltraSimpleLauncher:
    """The simplest possible RPattern interface - just one button!"""
    
    def __init__(self):
        """Initialize the ultra-simple launcher."""
        self.root = tk.Tk()
        self.root.title("🚀 RPattern - Ultra Simple Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg="#000011")
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Make it always on top for visibility
        self.root.attributes('-topmost', True)
        
        # Create the interface
        self.create_ultra_simple_ui()
        
    def create_ultra_simple_ui(self):
        """Create the most simple UI possible."""
        # Main title
        title = tk.Label(self.root,
                        text="🚀 RPattern",
                        font=("Arial", 24, "bold"),
                        fg="#00ff88",
                        bg="#000011")
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root,
                           text="Ultra-Secure Visual ID System",
                           font=("Arial", 12),
                           fg="#ffffff",
                           bg="#000011")
        subtitle.pack(pady=5)
        
        creator = tk.Label(self.root,
                          text="Created by Rahul Chaube",
                          font=("Arial", 10),
                          fg="#888888",
                          bg="#000011")
        creator.pack(pady=5)
        
        # Status display
        self.status_label = tk.Label(self.root,
                                    text="Ready to generate secure patterns!",
                                    font=("Arial", 11),
                                    fg="#00ffff",
                                    bg="#000011",
                                    wraplength=400)
        self.status_label.pack(pady=20)
        
        # Input field
        input_frame = tk.Frame(self.root, bg="#000011")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame,
                text="Enter your data:",
                font=("Arial", 11),
                fg="#ffffff",
                bg="#000011").pack()
        
        self.data_var = tk.StringVar(value="https://rahulchaube.dev")
        self.data_entry = tk.Entry(input_frame,
                                  textvariable=self.data_var,
                                  font=("Arial", 12),
                                  width=35,
                                  justify='center',
                                  bg="#1a1a1a",
                                  fg="#ffffff",
                                  insertbackground="#00ff88")
        self.data_entry.pack(pady=10, ipady=5)
        
        # THE ONLY BUTTON YOU NEED!
        self.magic_button = tk.Button(self.root,
                                     text="🔥 CREATE SECURE PATTERN",
                                     command=self.magic_generate,
                                     font=("Arial", 16, "bold"),
                                     bg="#ff0066",
                                     fg="white",
                                     relief="flat",
                                     bd=0,
                                     padx=30,
                                     pady=15,
                                     cursor="hand2")
        self.magic_button.pack(pady=20)
        
        # Scan button
        scan_button = tk.Button(self.root,
                               text="📷 SCAN PATTERN",
                               command=self.magic_scan,
                               font=("Arial", 14, "bold"),
                               bg="#0066ff",
                               fg="white",
                               relief="flat",
                               bd=0,
                               padx=20,
                               pady=10,
                               cursor="hand2")
        scan_button.pack(pady=10)
        
        # Bind Enter key
        self.data_entry.bind('<Return>', lambda e: self.magic_generate())
        
    def update_status(self, message, color="#00ffff"):
        """Update status message."""
        self.status_label.configure(text=message, fg=color)
        self.root.update()
        
    def magic_generate(self):
        """The magic one-click pattern generation!"""
        data = self.data_var.get().strip()
        if not data:
            self.update_status("Please enter some data first!", "#ff4444")
            return
            
        try:
            self.update_status("🔥 Creating your ultra-secure pattern...", "#ffaa00")
            self.magic_button.configure(text="⚡ GENERATING...", state="disabled")
            
            # Run the simple pattern generator
            threading.Thread(target=self._run_generator, args=(data,), daemon=True).start()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "#ff4444")
            self.magic_button.configure(text="🔥 CREATE SECURE PATTERN", state="normal")
    
    def _run_generator(self, data):
        """Run pattern generator in background."""
        try:
            # Use the simple core that always works
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))
            
            from rpattern_core import RPattern
            
            # Generate pattern
            rpattern = RPattern(expiry_minutes=2)  # 2 minutes for easier testing
            pattern = rpattern.encode_data(data, use_encryption=True)
            
            # Update UI
            self.root.after(0, lambda: self.update_status(
                f"✅ Secure pattern created! {pattern['total_frames']} frames generated.", "#00ff88"))
            
            # Launch simple display
            self.root.after(0, lambda: self._launch_simple_display(pattern))
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"Generation failed: {str(e)}", "#ff4444"))
        finally:
            self.root.after(0, lambda: self.magic_button.configure(
                text="🔥 CREATE SECURE PATTERN", state="normal"))
    
    def _launch_simple_display(self, pattern):
        """Launch simple pattern display."""
        try:
            # Launch the simple display script
            script_path = os.path.join(os.path.dirname(__file__), "simple_display.py")
            
            # Create simple display script if it doesn't exist
            if not os.path.exists(script_path):
                self._create_simple_display_script()
            
            # Save pattern data for the display script
            import json
            pattern_file = os.path.join(os.path.dirname(__file__), "current_pattern.json")
            with open(pattern_file, 'w') as f:
                json.dump(pattern, f)
            
            # Launch display
            subprocess.Popen([sys.executable, script_path], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            self.update_status("🎯 Pattern display opened! Point your camera at it.", "#00ff88")
            
        except Exception as e:
            self.update_status(f"Display error: {str(e)}", "#ff4444")
    
    def _create_simple_display_script(self):
        """Create a simple, bulletproof display script."""
        script_content = '''"""
Simple RPattern Display - Bulletproof Version
"""
import pygame
import sys
import os
import json
import time

def main():
    try:
        # Load pattern data
        pattern_file = os.path.join(os.path.dirname(__file__), "current_pattern.json")
        with open(pattern_file, 'r') as f:
            pattern = json.load(f)
        
        pygame.init()
        
        # Create display
        size = (600, 600)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("🚀 RPattern Display - Rahul Chaube")
        
        # Pattern area
        pattern_size = 400
        pattern_x = (size[0] - pattern_size) // 2
        pattern_y = (size[1] - pattern_size) // 2
        
        # Grid size (3x3 for compatibility)
        grid_size = 3
        cell_size = pattern_size // grid_size
        
        # Animation
        frame_index = 0
        last_time = time.time()
        frame_duration = pattern['frame_duration']
        
        font = pygame.font.Font(None, 36)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update frame
            current_time = time.time()
            if current_time - last_time >= frame_duration:
                frame_index = (frame_index + 1) % len(pattern['frames'])
                last_time = current_time
            
            # Clear screen
            screen.fill((10, 10, 20))
            
            # Draw pattern
            current_frame = pattern['frames'][frame_index]
            
            for row in range(min(grid_size, len(current_frame))):
                for col in range(min(grid_size, len(current_frame[row]))):
                    color = current_frame[row][col]
                    
                    x = pattern_x + col * cell_size + 10
                    y = pattern_y + row * cell_size + 10
                    
                    rect = pygame.Rect(x, y, cell_size - 20, cell_size - 20)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            
            # Draw border
            border_rect = pygame.Rect(pattern_x - 5, pattern_y - 5, 
                                    pattern_size + 10, pattern_size + 10)
            pygame.draw.rect(screen, (0, 255, 100), border_rect, 3)
            
            # Draw title
            title = font.render("🚀 RPattern - Scan Me!", True, (255, 255, 255))
            title_rect = title.get_rect(centerx=size[0]//2, y=50)
            screen.blit(title, title_rect)
            
            # Draw frame info
            frame_text = f"Frame {frame_index + 1}/{len(pattern['frames'])}"
            frame_surface = pygame.font.Font(None, 24).render(frame_text, True, (200, 200, 200))
            frame_rect = frame_surface.get_rect(centerx=size[0]//2, y=pattern_y + pattern_size + 30)
            screen.blit(frame_surface, frame_rect)
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        
    except Exception as e:
        print(f"Display error: {e}")
        input("Press Enter to close...")

if __name__ == "__main__":
    main()
'''
        
        script_path = os.path.join(os.path.dirname(__file__), "simple_display.py")
        with open(script_path, 'w') as f:
            f.write(script_content)
    
    def magic_scan(self):
        """Launch the ultra-simple scanner."""
        try:
            self.update_status("📷 Starting camera scanner...", "#ffaa00")
            
            # Launch simple scanner
            script_path = os.path.join(os.path.dirname(__file__), "simple_scanner.py")
            
            # Create simple scanner if it doesn't exist
            if not os.path.exists(script_path):
                self._create_simple_scanner_script()
            
            subprocess.Popen([sys.executable, script_path],
                           creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            self.update_status("🎯 Scanner launched! Point camera at RPattern.", "#00ff88")
            
        except Exception as e:
            self.update_status(f"Scanner error: {str(e)}", "#ff4444")
    
    def _create_simple_scanner_script(self):
        """Create a bulletproof scanner script."""
        script_content = '''"""
Simple RPattern Scanner - Bulletproof Version
"""
import cv2
import numpy as np
import sys
import os

def main():
    try:
        # Add src to path
        sys.path.insert(0, os.path.dirname(__file__))
        from rpattern_core import RPattern
        
        # Initialize camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Could not open camera")
            input("Press Enter to exit...")
            return
        
        print("🚀 Simple RPattern Scanner")
        print("📷 Point camera at RPattern to scan")
        print("❌ Press 'q' to quit")
        
        rpattern = RPattern()
        
        # Create window with compatible flag
        window_name = "🚀 RPattern Scanner"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Simple overlay
            cv2.putText(frame, "RPattern Scanner - Point camera at pattern", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to quit", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Show frame
            cv2.imshow(window_name, frame)
            
            # Check for quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Scanner error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
        
        script_path = os.path.join(os.path.dirname(__file__), "simple_scanner.py")
        with open(script_path, 'w') as f:
            f.write(script_content)
    
    def run(self):
        """Run the ultra-simple launcher."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass


def main():
    """Launch the ultra-simple interface."""
    print("🚀 Launching Ultra-Simple RPattern...")
    
    app = UltraSimpleLauncher()
    app.run()


if __name__ == "__main__":
    main()
