"""
RPattern Demo - Complete Demonstration Application
Creator: Rahul Chaube 🚀

A comprehensive demo showcasing RPattern generation, display, and scanning.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import sys
import time
from typing import Dict, Any, Optional
from rpattern_core import RPattern
from pattern_generator import RPatternDisplay
from pattern_scanner import RPatternScanner
import pygame


class RPatternDemoGUI:
    """Main GUI application for RPattern demonstration."""
    
    def __init__(self):
        """Initialize the demo GUI."""
        self.root = tk.Tk()
        self.root.title("🚀 RPattern Demo - by Rahul Chaube")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        
        # Style configuration
        self.setup_styles()
        
        # State variables
        self.current_pattern = None
        self.display_thread = None
        self.scanner_thread = None
        self.is_display_running = False
        self.is_scanner_running = False
        
        # Create GUI components
        self.create_widgets()
        
        # Initialize pygame for pattern display
        pygame.init()
        
    def setup_styles(self):
        """Setup custom styles for the GUI."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       foreground='#00ff96', 
                       background='#1a1a2e',
                       font=('Arial', 16, 'bold'))
        
        style.configure('Accent.TButton',
                       foreground='white',
                       background='#00ff96',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Demo.TFrame',
                       background='#1a1a2e')
        
    def create_widgets(self):
        """Create and layout GUI widgets."""
        # Main title
        title_label = ttk.Label(self.root, 
                               text="🚀 RPattern - Next-Gen Visual ID System",
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Creator label
        creator_label = ttk.Label(self.root,
                                 text="Created by Rahul Chaube",
                                 foreground='#888888',
                                 background='#1a1a2e',
                                 font=('Arial', 10))
        creator_label.pack(pady=(0, 20))
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_generator_tab()
        self.create_scanner_tab()
        self.create_info_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, 
                              textvariable=self.status_var,
                              relief='sunken',
                              background='#16213e',
                              foreground='white')
        status_bar.pack(side='bottom', fill='x')
        
    def create_generator_tab(self):
        """Create the pattern generator tab."""
        generator_frame = ttk.Frame(self.notebook, style='Demo.TFrame')
        self.notebook.add(generator_frame, text="🎨 Pattern Generator")
        
        # Input section
        input_frame = ttk.LabelFrame(generator_frame, text="Pattern Configuration", padding=20)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Data input
        ttk.Label(input_frame, text="Data to Encode:").grid(row=0, column=0, sticky='w', pady=5)
        self.data_var = tk.StringVar(value="https://rahulcodes.in")
        data_entry = ttk.Entry(input_frame, textvariable=self.data_var, width=50)
        data_entry.grid(row=0, column=1, columnspan=2, sticky='ew', pady=5)
        
        # Expiry time
        ttk.Label(input_frame, text="Expiry (minutes):").grid(row=1, column=0, sticky='w', pady=5)
        self.expiry_var = tk.StringVar(value="5")
        expiry_spin = ttk.Spinbox(input_frame, from_=1, to=60, textvariable=self.expiry_var, width=10)
        expiry_spin.grid(row=1, column=1, sticky='w', pady=5)
        
        # Encryption option
        self.encryption_var = tk.BooleanVar(value=True)
        encryption_check = ttk.Checkbutton(input_frame, text="Enable Encryption", 
                                          variable=self.encryption_var)
        encryption_check.grid(row=1, column=2, sticky='w', pady=5)
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        
        # Buttons section
        button_frame = ttk.Frame(generator_frame)
        button_frame.pack(fill='x', padx=20, pady=10)
        
        generate_btn = ttk.Button(button_frame, text="🎨 Generate Pattern",
                                 command=self.generate_pattern, style='Accent.TButton')
        generate_btn.pack(side='left', padx=5)
        
        display_btn = ttk.Button(button_frame, text="📺 Display Pattern",
                                command=self.display_pattern, style='Accent.TButton')
        display_btn.pack(side='left', padx=5)
        
        stop_display_btn = ttk.Button(button_frame, text="⏹️ Stop Display",
                                     command=self.stop_display)
        stop_display_btn.pack(side='left', padx=5)
        
        # Pattern info section
        info_frame = ttk.LabelFrame(generator_frame, text="Pattern Information", padding=20)
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.pattern_info_text = scrolledtext.ScrolledText(info_frame, height=15, width=70,
                                                          bg='#16213e', fg='white',
                                                          font=('Consolas', 10))
        self.pattern_info_text.pack(fill='both', expand=True)
        
    def create_scanner_tab(self):
        """Create the pattern scanner tab."""
        scanner_frame = ttk.Frame(self.notebook, style='Demo.TFrame')
        self.notebook.add(scanner_frame, text="📷 Pattern Scanner")
        
        # Scanner controls
        control_frame = ttk.LabelFrame(scanner_frame, text="Scanner Controls", padding=20)
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Camera selection
        ttk.Label(control_frame, text="Camera Index:").grid(row=0, column=0, sticky='w', pady=5)
        self.camera_var = tk.StringVar(value="0")
        camera_spin = ttk.Spinbox(control_frame, from_=0, to=5, textvariable=self.camera_var, width=10)
        camera_spin.grid(row=0, column=1, sticky='w', pady=5)
        
        # Scanner buttons
        scan_btn = ttk.Button(control_frame, text="📷 Start Scanner",
                             command=self.start_scanner, style='Accent.TButton')
        scan_btn.grid(row=0, column=2, padx=20, pady=5)
        
        stop_scan_btn = ttk.Button(control_frame, text="⏹️ Stop Scanner",
                                  command=self.stop_scanner)
        stop_scan_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Scanner output
        output_frame = ttk.LabelFrame(scanner_frame, text="Scanner Output", padding=20)
        output_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.scanner_output_text = scrolledtext.ScrolledText(output_frame, height=20, width=70,
                                                            bg='#16213e', fg='white',
                                                            font=('Consolas', 10))
        self.scanner_output_text.pack(fill='both', expand=True)
        
    def create_info_tab(self):
        """Create the information tab."""
        info_frame = ttk.Frame(self.notebook, style='Demo.TFrame')
        self.notebook.add(info_frame, text="ℹ️ About RPattern")
        
        # About text
        about_text = """
🚀 RPattern - Next-Generation Visual ID System
Created by Rahul Chaube

RPattern is a revolutionary visual identification system that replaces traditional QR codes with dynamic, animated patterns. Unlike static QR codes, RPatterns use color-based animations that are both more visually appealing and more secure.

🎯 Key Features:
• Dynamic color-pulse animations for visual appeal
• Time-based expiry for enhanced security  
• AES encryption for secure data encoding
• Real-time camera scanning with OpenCV
• Collision-resistant pattern generation
• Error correction capabilities
• Futuristic GUI with visual feedback

🔧 Technical Architecture:
• Pattern Encoding: Data → Encryption → Binary → Color Frames
• Pattern Display: Animated color sequences in 3x3 grid
• Pattern Scanning: Camera capture → Color detection → Decoding
• Security: AES encryption + time-based expiry

🎨 Visual Design:
RPatterns use a 3x3 grid where each cell displays one of four colors:
• Red (00) - Binary representation
• Green (01) - Binary representation  
• Blue (10) - Binary representation
• Yellow (11) - Binary representation
• White - Start synchronization frame
• Black - End synchronization frame

⚡ Performance:
• Frame rate: 2 FPS (0.5s per frame)
• Maximum pattern length: 10 frames
• Detection range: 100-800 pixels pattern size
• Encryption: AES-256 with random IV

🌟 Use Cases:
• Contactless payments and transactions
• Smart login and authentication
• Secure information sharing
• Digital business cards
• Event tickets and access control
• IoT device pairing
• Marketing and promotional campaigns

🔮 Future Enhancements:
• Machine learning for improved detection
• 3D pattern animations
• Multi-device synchronization
• Blockchain integration for verification
• AR/VR compatibility
• Mobile app development

Made with ❤️ by Rahul Chaube
GitHub: https://github.com/rahulchaube
        """
        
        about_text_widget = scrolledtext.ScrolledText(info_frame, wrap='word',
                                                     bg='#16213e', fg='white',
                                                     font=('Arial', 11))
        about_text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        about_text_widget.insert('1.0', about_text)
        about_text_widget.configure(state='disabled')
        
    def generate_pattern(self):
        """Generate an RPattern with current settings."""
        try:
            data = self.data_var.get().strip()
            if not data:
                messagebox.showerror("Error", "Please enter data to encode")
                return
                
            expiry_minutes = int(self.expiry_var.get())
            use_encryption = self.encryption_var.get()
            
            self.status_var.set("Generating pattern...")
            self.root.update()
            
            # Generate pattern
            rpattern = RPattern(expiry_minutes=expiry_minutes)
            self.current_pattern = rpattern.encode_data(data, use_encryption=use_encryption)
            
            # Display pattern information
            self.display_pattern_info()
            
            self.status_var.set("Pattern generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate pattern: {str(e)}")
            self.status_var.set("Pattern generation failed")
            
    def display_pattern_info(self):
        """Display information about the current pattern."""
        if not self.current_pattern:
            return
            
        rpattern = RPattern()
        info = rpattern.get_pattern_info(self.current_pattern)
        
        info_text = f"""
🚀 RPattern Generated Successfully!

📊 Pattern Statistics:
• Total Frames: {info['total_frames']}
• Frame Duration: {info['frame_duration']} seconds
• Total Animation Time: {info['total_frames'] * info['frame_duration']:.1f} seconds
• Encryption: {'🔐 Enabled' if info['encrypted'] else '📝 Disabled'}

⏰ Timing Information:
• Created: {info['created_at']}
• Time Remaining: {info['time_remaining_seconds']} seconds
• Status: {'⚠️ EXPIRED' if info['is_expired'] else '✅ ACTIVE'}

🎨 Pattern Structure:
• Grid Size: 3x3 cells
• Color Encoding: 4 colors (Red, Green, Blue, Yellow)
• Synchronization: White (start) + Black (end) frames
• Error Correction: Built-in frame validation

📱 Usage Instructions:
1. Click 'Display Pattern' to show the animated pattern
2. Point your camera at the pattern using the Scanner tab
3. The pattern will be automatically detected and decoded
4. Ensure good lighting and stable camera positioning

🔧 Technical Details:
• Binary encoding: 2 bits per color (4 combinations)
• Data flow: Text → JSON → Encryption → Binary → Colors
• Frame rate: {1/info['frame_duration']:.1f} FPS
• Security: Time-based expiry + optional AES encryption
        """
        
        self.pattern_info_text.delete('1.0', 'end')
        self.pattern_info_text.insert('1.0', info_text)
        
    def display_pattern(self):
        """Display the current pattern in a new window."""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "Please generate a pattern first")
            return
            
        if self.is_display_running:
            messagebox.showinfo("Info", "Pattern display is already running")
            return
            
        # Start display in separate thread
        self.display_thread = threading.Thread(target=self._run_pattern_display, daemon=True)
        self.display_thread.start()
        
        self.is_display_running = True
        self.status_var.set("Pattern display started")
        
    def _run_pattern_display(self):
        """Run pattern display in separate thread."""
        try:
            display = RPatternDisplay()
            display.load_pattern(self.current_pattern)
            display.start_animation()
            
            # Simple display loop (simplified version for threading)
            pygame.display.set_mode((800, 600))
            pygame.display.set_caption("🚀 RPattern Display - by Rahul Chaube")
            
            clock = pygame.time.Clock()
            running = True
            
            while running and self.is_display_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                display.update_animation()
                
                # Clear and draw
                display.screen.fill(display.bg_color)
                display.draw_pattern_border()
                display.draw_pattern_frame()
                display.draw_info_panel()
                
                pygame.display.flip()
                clock.tick(60)
                
            pygame.quit()
            
        except Exception as e:
            print(f"Display error: {e}")
        finally:
            self.is_display_running = False
            
    def stop_display(self):
        """Stop the pattern display."""
        self.is_display_running = False
        self.status_var.set("Pattern display stopped")
        
    def start_scanner(self):
        """Start the pattern scanner."""
        if self.is_scanner_running:
            messagebox.showinfo("Info", "Scanner is already running")
            return
            
        camera_index = int(self.camera_var.get())
        
        # Start scanner in separate thread
        self.scanner_thread = threading.Thread(
            target=self._run_scanner, 
            args=(camera_index,), 
            daemon=True
        )
        self.scanner_thread.start()
        
        self.is_scanner_running = True
        self.status_var.set("Scanner started")
        
    def _run_scanner(self, camera_index: int):
        """Run scanner in separate thread."""
        try:
            scanner = RPatternScanner(camera_index=camera_index)
            
            # Redirect scanner output to GUI
            original_print = print
            def gui_print(*args, **kwargs):
                message = ' '.join(str(arg) for arg in args)
                self.root.after(0, self._add_scanner_output, message)
                original_print(*args, **kwargs)
            
            # Temporarily replace print
            import builtins
            builtins.print = gui_print
            
            try:
                scanner.start_scanning()
            finally:
                builtins.print = original_print
                
        except Exception as e:
            self.root.after(0, self._add_scanner_output, f"Scanner error: {e}")
        finally:
            self.is_scanner_running = False
            self.root.after(0, lambda: self.status_var.set("Scanner stopped"))
            
    def _add_scanner_output(self, message: str):
        """Add message to scanner output."""
        self.scanner_output_text.insert('end', f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.scanner_output_text.see('end')
        
    def stop_scanner(self):
        """Stop the pattern scanner."""
        self.is_scanner_running = False
        self.status_var.set("Stopping scanner...")
        
    def run(self):
        """Run the demo application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Demo interrupted by user")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources."""
        self.is_display_running = False
        self.is_scanner_running = False
        
        if pygame.get_init():
            pygame.quit()


def run_standalone_generator():
    """Run standalone pattern generator."""
    from pattern_generator import main as generator_main
    generator_main()


def run_standalone_scanner():
    """Run standalone pattern scanner."""  
    from pattern_scanner import main as scanner_main
    scanner_main()


def main():
    """Main demo function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="🚀 RPattern Demo by Rahul Chaube")
    parser.add_argument("--mode", "-m", choices=['demo', 'generator', 'scanner'], 
                       default='demo', help="Application mode")
    
    args = parser.parse_args()
    
    print("🚀 RPattern - Next-Gen Visual ID System")
    print("Creator: Rahul Chaube")
    print(f"Mode: {args.mode}")
    print("-" * 50)
    
    if args.mode == 'demo':
        # Run full demo GUI
        demo = RPatternDemoGUI()
        demo.run()
    elif args.mode == 'generator':
        # Run standalone generator
        run_standalone_generator()
    elif args.mode == 'scanner':
        # Run standalone scanner
        run_standalone_scanner()


if __name__ == "__main__":
    main()
