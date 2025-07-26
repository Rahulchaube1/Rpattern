"""
Super Simple HyperSecure RPattern Interface
Creator: Rahul Chaube 🚀

One-click secure pattern generation and scanning
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import threading
import time
from typing import Optional
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    from hyper_secure_core import HyperSecureRPattern
    HYPER_SECURITY_AVAILABLE = True
except ImportError:
    from rpattern_core import RPattern
    HYPER_SECURITY_AVAILABLE = False


class SuperSimpleRPattern:
    """Ultra-simple interface for RPattern creation and scanning."""
    
    def __init__(self):
        """Initialize the super simple interface."""
        self.root = tk.Tk()
        self.root.title("🚀 RPattern - Super Simple & Hyper Secure")
        self.root.geometry("600x500")
        self.root.configure(bg="#0a0a0a")
        
        # Configure style
        self.setup_modern_style()
        
        # Pattern generator
        if HYPER_SECURITY_AVAILABLE:
            self.rpattern = HyperSecureRPattern(expiry_seconds=30, security_level="ULTRA")
        else:
            self.rpattern = RPattern(expiry_minutes=1)
            
        self.current_pattern = None
        self.display_thread = None
        self.is_displaying = False
        
        # Create interface
        self.create_simple_interface()
        
    def setup_modern_style(self):
        """Setup modern dark theme."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark theme colors
        style.configure('Modern.TLabel',
                       foreground='#00ff88',
                       background='#0a0a0a',
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('Title.TLabel',
                       foreground='#00ffff',
                       background='#0a0a0a',
                       font=('Segoe UI', 20, 'bold'))
        
        style.configure('Hyper.TButton',
                       foreground='white',
                       background='#ff0066',
                       font=('Segoe UI', 12, 'bold'),
                       borderwidth=0)
        
        style.configure('Secure.TButton',
                       foreground='white',
                       background='#0066ff',
                       font=('Segoe UI', 12, 'bold'),
                       borderwidth=0)
        
    def create_simple_interface(self):
        """Create ultra-simple user interface."""
        # Main title
        title = ttk.Label(self.root,
                         text="🚀 RPattern - Hyper Secure Visual ID",
                         style='Title.TLabel')
        title.pack(pady=30)
        
        # Creator credit
        creator = ttk.Label(self.root,
                           text="Created by Rahul Chaube",
                           style='Modern.TLabel')
        creator.pack(pady=10)
        
        # Security status
        if HYPER_SECURITY_AVAILABLE:
            security_text = "🔒 MILITARY-GRADE SECURITY ACTIVE"
            security_color = "#00ff88"
        else:
            security_text = "🔐 STANDARD SECURITY MODE"
            security_color = "#ffaa00"
            
        security_label = tk.Label(self.root,
                                text=security_text,
                                fg=security_color,
                                bg="#0a0a0a",
                                font=('Segoe UI', 12, 'bold'))
        security_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#0a0a0a")
        input_frame.pack(pady=30, padx=50, fill='x')
        
        tk.Label(input_frame,
                text="Enter your data to secure:",
                fg="#ffffff",
                bg="#0a0a0a",
                font=('Segoe UI', 12)).pack(pady=10)
        
        self.data_var = tk.StringVar(value="https://rahulchaube.dev")
        self.data_entry = tk.Entry(input_frame,
                                  textvariable=self.data_var,
                                  font=('Segoe UI', 14),
                                  width=40,
                                  justify='center',
                                  bg="#1a1a1a",
                                  fg="#ffffff",
                                  insertbackground="#00ff88",
                                  relief='flat',
                                  bd=10)
        self.data_entry.pack(pady=10, ipady=8)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#0a0a0a")
        buttons_frame.pack(pady=30)
        
        # Generate button
        generate_btn = tk.Button(buttons_frame,
                               text="🔥 GENERATE HYPER-SECURE PATTERN",
                               command=self.generate_pattern,
                               bg="#ff0066",
                               fg="white",
                               font=('Segoe UI', 14, 'bold'),
                               relief='flat',
                               bd=0,
                               padx=20,
                               pady=15,
                               cursor='hand2')
        generate_btn.pack(pady=10)
        
        # Scan button
        scan_btn = tk.Button(buttons_frame,
                           text="📷 SCAN PATTERN WITH CAMERA",
                           command=self.start_scanning,
                           bg="#0066ff",
                           fg="white",
                           font=('Segoe UI', 14, 'bold'),
                           relief='flat',
                           bd=0,
                           padx=20,
                           pady=15,
                           cursor='hand2')
        scan_btn.pack(pady=10)
        
        # Status display
        self.status_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.status_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        self.status_text = tk.Text(self.status_frame,
                                  height=8,
                                  bg="#1a1a1a",
                                  fg="#00ff88",
                                  font=('Consolas', 11),
                                  relief='flat',
                                  bd=0,
                                  wrap='word')
        self.status_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initial status
        self.update_status("🚀 RPattern ready! Enter data and click GENERATE.")
        
        # Bind events
        self.data_entry.bind('<Return>', lambda e: self.generate_pattern())
        
    def update_status(self, message: str):
        """Update status display."""
        self.status_text.insert('end', f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see('end')
        self.root.update()
        
    def generate_pattern(self):
        """Generate hyper-secure pattern with one click."""
        data = self.data_var.get().strip()
        if not data:
            messagebox.showerror("Error", "Please enter some data to secure!")
            return
            
        try:
            self.update_status("🔐 Generating hyper-secure pattern...")
            
            # Generate pattern
            start_time = time.time()
            if HYPER_SECURITY_AVAILABLE:
                self.current_pattern = self.rpattern.encode_hyper_secure_data(data)
                security_report = self.rpattern.get_security_report(self.current_pattern)
                
                self.update_status(f"✅ ULTRA-SECURE pattern generated!")
                self.update_status(f"🛡️  Security: {security_report['security_level']}")
                self.update_status(f"🔒 Encryption: {security_report['encryption_layers']} layers")
                self.update_status(f"⚡ Features: {len(security_report['security_features'])} security features")
                
            else:
                self.current_pattern = self.rpattern.encode_data(data, use_encryption=True)
                self.update_status("✅ Secure pattern generated!")
                
            encode_time = time.time() - start_time
            
            frames = self.current_pattern['total_frames']
            duration = frames * self.current_pattern['frame_duration']
            
            self.update_status(f"📊 Stats: {frames} frames, {duration:.1f}s animation")
            self.update_status(f"⚡ Generated in {encode_time:.3f} seconds")
            self.update_status("🎯 Click below to display animated pattern!")
            
            # Auto-display pattern
            self.display_pattern()
            
        except Exception as e:
            self.update_status(f"❌ Generation failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate pattern: {str(e)}")
    
    def display_pattern(self):
        """Display the animated pattern."""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "Generate a pattern first!")
            return
            
        if self.is_displaying:
            self.update_status("📺 Pattern already displaying!")
            return
            
        # Start display in separate thread
        self.display_thread = threading.Thread(target=self._run_pattern_display, daemon=True)
        self.display_thread.start()
        self.is_displaying = True
        
        self.update_status("📺 Animated pattern window opened!")
        self.update_status("🎯 Point your camera at the pattern to scan!")
        
    def _run_pattern_display(self):
        """Run pattern display with enhanced visuals."""
        try:
            pygame.init()
            
            # Create window
            window_size = (700, 700)
            screen = pygame.display.set_mode(window_size)
            pygame.display.set_caption("🚀 HyperSecure RPattern - Rahul Chaube")
            
            # Pattern area
            pattern_size = 500
            pattern_rect = pygame.Rect(
                (window_size[0] - pattern_size) // 2,
                (window_size[1] - pattern_size) // 2,
                pattern_size,
                pattern_size
            )
            
            # Determine grid size
            if HYPER_SECURITY_AVAILABLE:
                grid_size = 4  # 4x4 for hyper-secure
            else:
                grid_size = 3  # 3x3 for standard
                
            cell_size = pattern_size // grid_size
            
            # Fonts
            font_large = pygame.font.Font(None, 48)
            font_medium = pygame.font.Font(None, 32)
            
            # Animation state
            current_frame = 0
            last_frame_time = time.time()
            frame_duration = self.current_pattern['frame_duration']
            
            clock = pygame.time.Clock()
            running = True
            
            while running and self.is_displaying:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                
                # Update animation
                current_time = time.time()
                if current_time - last_frame_time >= frame_duration:
                    current_frame = (current_frame + 1) % len(self.current_pattern['frames'])
                    last_frame_time = current_time
                
                # Clear screen with dark background
                screen.fill((10, 10, 20))
                
                # Draw glowing border
                for i in range(15):
                    alpha = 255 - i * 15
                    if alpha > 0:
                        glow_rect = pygame.Rect(
                            pattern_rect.x - i,
                            pattern_rect.y - i,
                            pattern_rect.width + 2*i,
                            pattern_rect.height + 2*i
                        )
                        pygame.draw.rect(screen, (0, 255, 136, alpha//4), glow_rect, 2)
                
                # Draw main border
                pygame.draw.rect(screen, (0, 255, 136), pattern_rect, 4)
                
                # Draw pattern grid
                frame_data = self.current_pattern['frames'][current_frame]
                
                for row in range(grid_size):
                    for col in range(grid_size):
                        color = frame_data[row][col]
                        
                        x = pattern_rect.x + col * cell_size
                        y = pattern_rect.y + row * cell_size
                        
                        # Cell with padding
                        padding = 8
                        cell_rect = pygame.Rect(
                            x + padding, y + padding,
                            cell_size - 2*padding,
                            cell_size - 2*padding
                        )
                        
                        pygame.draw.rect(screen, color, cell_rect)
                        pygame.draw.rect(screen, (100, 100, 100), cell_rect, 2)
                
                # Draw title
                if HYPER_SECURITY_AVAILABLE:
                    title_text = font_large.render("🔒 HYPER-SECURE RPATTERN", True, (0, 255, 255))
                else:
                    title_text = font_large.render("🔐 SECURE RPATTERN", True, (0, 255, 136))
                    
                title_rect = title_text.get_rect(centerx=window_size[0]//2, y=30)
                screen.blit(title_text, title_rect)
                
                # Draw frame info
                frame_info = f"Frame {current_frame + 1}/{len(self.current_pattern['frames'])}"
                frame_text = font_medium.render(frame_info, True, (255, 255, 255))
                frame_rect = frame_text.get_rect(centerx=window_size[0]//2, y=pattern_rect.bottom + 30)
                screen.blit(frame_text, frame_rect)
                
                # Draw security info
                if HYPER_SECURITY_AVAILABLE:
                    security_text = "🛡️ MILITARY-GRADE ENCRYPTION ACTIVE"
                    color = (255, 100, 100)
                else:
                    security_text = "🔐 AES-256 ENCRYPTION ACTIVE"
                    color = (100, 255, 100)
                    
                security_surface = font_medium.render(security_text, True, color)
                security_rect = security_surface.get_rect(centerx=window_size[0]//2, y=pattern_rect.bottom + 70)
                screen.blit(security_surface, security_rect)
                
                # Draw instructions
                instructions = [
                    "📱 Point camera at this pattern",
                    "🎯 Auto-detection enabled",
                    "❌ Press ESC to close"
                ]
                
                for i, instruction in enumerate(instructions):
                    inst_text = pygame.font.Font(None, 24).render(instruction, True, (180, 180, 180))
                    inst_rect = inst_text.get_rect(x=20, y=window_size[1] - 80 + i*25)
                    screen.blit(inst_text, inst_rect)
                
                pygame.display.flip()
                clock.tick(60)
            
            pygame.quit()
            
        except Exception as e:
            print(f"Display error: {e}")
        finally:
            self.is_displaying = False
    
    def start_scanning(self):
        """Start camera scanning."""
        try:
            self.update_status("📷 Starting camera scanner...")
            
            # Import and start scanner
            if HYPER_SECURITY_AVAILABLE:
                from hyper_secure_scanner import HyperSecureScanner
                scanner = HyperSecureScanner()
            else:
                from pattern_scanner import RPatternScanner
                scanner = RPatternScanner()
            
            self.update_status("🎯 Camera scanner launched!")
            self.update_status("📱 Point camera at RPattern to scan")
            
            # Start scanner in background
            scanner_thread = threading.Thread(target=scanner.start_scanning, daemon=True)
            scanner_thread.start()
            
        except Exception as e:
            self.update_status(f"❌ Scanner failed: {str(e)}")
            messagebox.showerror("Scanner Error", f"Failed to start scanner: {str(e)}")
    
    def run(self):
        """Run the super simple interface."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self.is_displaying = False


def main():
    """Launch the super simple RPattern interface."""
    print("🚀 Launching Super Simple HyperSecure RPattern...")
    
    if HYPER_SECURITY_AVAILABLE:
        print("🔒 MILITARY-GRADE SECURITY LOADED")
    else:
        print("🔐 Standard security mode (install pycryptodome for hyper-security)")
    
    app = SuperSimpleRPattern()
    app.run()


if __name__ == "__main__":
    main()
