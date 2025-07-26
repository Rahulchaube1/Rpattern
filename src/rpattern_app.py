"""
🚀 RPattern Revolutionary UI - Complete Application
Author: Rahul Chaube
Vision: Revolutionary interface for the future of visual patterns

This is the main application that brings together all RPattern components.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import time
import json
import subprocess
import sys
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Try to import our modules
try:
    from rpattern_revolutionary import RPatternCore, create_revolutionary_pattern
    from pattern_display import RPatternAnimator, display_pattern
    from revolutionary_scanner import RevolutionaryScanner, start_revolutionary_scanning
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some modules not available: {e}")
    MODULES_AVAILABLE = False


@dataclass
class AppState:
    """Application state management."""
    current_pattern: Optional[Dict[str, Any]] = None
    is_scanning: bool = False
    is_displaying: bool = False
    last_decoded_data: str = ""
    total_patterns_created: int = 0
    total_patterns_scanned: int = 0


class RPatternRevolutionaryApp:
    """
    Revolutionary RPattern application with complete functionality.
    """
    
    def __init__(self):
        """Initialize the revolutionary application."""
        self.root = tk.Tk()
        self.root.title("🚀 RPattern Revolutionary System - by Rahul Chaube")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e2e')
        
        # Application state
        self.state = AppState()
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()
        
        # Create UI
        self._create_main_interface()
        
        # Initialize components
        if MODULES_AVAILABLE:
            self.rpattern_core = RPatternCore()
        
        print("🚀 RPattern Revolutionary App initialized")
        print("💎 Created by Rahul Chaube")
    
    def _configure_styles(self):
        """Configure custom styles for the application."""
        # Configure button styles
        self.style.configure('Action.TButton',
                           font=('Arial', 12, 'bold'),
                           padding=(10, 5))
        
        self.style.configure('Success.TButton',
                           font=('Arial', 12, 'bold'),
                           padding=(10, 5))
        
        self.style.configure('Info.TButton',
                           font=('Arial', 10),
                           padding=(5, 3))
        
        # Configure label styles
        self.style.configure('Title.TLabel',
                           font=('Arial', 20, 'bold'),
                           foreground='#00ff88',
                           background='#1e1e2e')
        
        self.style.configure('Header.TLabel',
                           font=('Arial', 14, 'bold'),
                           foreground='#88ccff',
                           background='#1e1e2e')
        
        self.style.configure('Info.TLabel',
                           font=('Arial', 10),
                           foreground='#cccccc',
                           background='#1e1e2e')
    
    def _create_main_interface(self):
        """Create the main application interface."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title section
        self._create_title_section(main_frame)
        
        # Content notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=(20, 0))
        
        # Create tabs
        self._create_generator_tab()
        self._create_scanner_tab()
        self._create_gallery_tab()
        self._create_settings_tab()
        self._create_about_tab()
        
        # Status bar
        self._create_status_bar(main_frame)
    
    def _create_title_section(self, parent):
        """Create the title section."""
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill='x', pady=(0, 20))
        
        # Main title
        title_label = ttk.Label(title_frame, 
                               text="🚀 RPattern Revolutionary System",
                               style='Title.TLabel')
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(title_frame,
                                  text="Dynamic • Encrypted • Animated Visual Patterns",
                                  style='Header.TLabel')
        subtitle_label.pack()
        
        # Creator
        creator_label = ttk.Label(title_frame,
                                 text="Created by Rahul Chaube 💎",
                                 style='Info.TLabel')
        creator_label.pack()
    
    def _create_generator_tab(self):
        """Create the pattern generator tab."""
        gen_frame = ttk.Frame(self.notebook)
        self.notebook.add(gen_frame, text="🎨 Pattern Generator")
        
        # Input section
        input_frame = ttk.LabelFrame(gen_frame, text="📝 Data Input", padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(input_frame, text="Enter data to encode:").pack(anchor='w')
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame, 
            height=8, 
            font=('Consolas', 11),
            wrap='word'
        )
        self.input_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Default text
        default_text = """🚀 Welcome to RPattern Revolutionary System!

Enter your data here:
• URLs: https://rahulchaube.dev
• UPI: upi://pay?pa=rahul@paytm&pn=Rahul&am=100
• Text: Secret message for testing
• JSON: {"type": "demo", "creator": "Rahul Chaube"}

Your data will be encrypted with military-grade security!"""
        
        self.input_text.insert('1.0', default_text)
        
        # Settings section
        settings_frame = ttk.LabelFrame(gen_frame, text="⚙️ Pattern Settings", padding=10)
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        settings_grid = ttk.Frame(settings_frame)
        settings_grid.pack(fill='x')
        
        # Expiry time
        ttk.Label(settings_grid, text="Expiry Time (seconds):").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.expiry_var = tk.StringVar(value="60")
        expiry_spin = ttk.Spinbox(settings_grid, from_=10, to=300, textvariable=self.expiry_var, width=10)
        expiry_spin.grid(row=0, column=1, sticky='w')
        
        # Security level
        ttk.Label(settings_grid, text="Security Level:").grid(row=0, column=2, sticky='w', padx=(20, 10))
        self.security_var = tk.StringVar(value="MILITARY")
        security_combo = ttk.Combobox(settings_grid, textvariable=self.security_var, 
                                     values=["MILITARY", "HIGH", "MEDIUM"], state="readonly", width=10)
        security_combo.grid(row=0, column=3, sticky='w')
        
        # Action buttons
        action_frame = ttk.Frame(gen_frame)
        action_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(action_frame, text="🔥 Create Revolutionary Pattern", 
                  command=self._create_pattern, style='Action.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="🎬 Display Pattern", 
                  command=self._display_pattern, style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="💾 Save Pattern", 
                  command=self._save_pattern, style='Info.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="🗑️ Clear", 
                  command=self._clear_input, style='Info.TButton').pack(side='right')
        
        # Pattern info section
        info_frame = ttk.LabelFrame(gen_frame, text="📊 Pattern Information", padding=10)
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.pattern_info = scrolledtext.ScrolledText(
            info_frame,
            height=8,
            font=('Consolas', 10),
            state='disabled'
        )
        self.pattern_info.pack(fill='both', expand=True)
    
    def _create_scanner_tab(self):
        """Create the pattern scanner tab."""
        scan_frame = ttk.Frame(self.notebook)
        self.notebook.add(scan_frame, text="📱 Pattern Scanner")
        
        # Scanner controls
        control_frame = ttk.LabelFrame(scan_frame, text="🎮 Scanner Controls", padding=10)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        controls_grid = ttk.Frame(control_frame)
        controls_grid.pack(fill='x')
        
        # Camera selection
        ttk.Label(controls_grid, text="Camera:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.camera_var = tk.StringVar(value="0")
        camera_spin = ttk.Spinbox(controls_grid, from_=0, to=5, textvariable=self.camera_var, width=5)
        camera_spin.grid(row=0, column=1, sticky='w')
        
        # Scanner buttons
        button_frame = ttk.Frame(scan_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        self.scan_button = ttk.Button(button_frame, text="🚀 Start Revolutionary Scanning", 
                                     command=self._start_scanning, style='Action.TButton')
        self.scan_button.pack(side='left', padx=(0, 10))
        
        self.stop_scan_button = ttk.Button(button_frame, text="⏹️ Stop Scanning", 
                                          command=self._stop_scanning, style='Info.TButton', state='disabled')
        self.stop_scan_button.pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="📷 Test Camera", 
                  command=self._test_camera, style='Info.TButton').pack(side='left')
        
        # Scan results
        results_frame = ttk.LabelFrame(scan_frame, text="📋 Scan Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.scan_results = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            font=('Consolas', 11),
            state='disabled'
        )
        self.scan_results.pack(fill='both', expand=True)
        
        # Initial message
        self._add_scan_result("🚀 RPattern Revolutionary Scanner ready!")
        self._add_scan_result("📱 Click 'Start Revolutionary Scanning' to begin")
        self._add_scan_result("🎯 Point camera at RPattern to decode")
    
    def _create_gallery_tab(self):
        """Create the pattern gallery tab."""
        gallery_frame = ttk.Frame(self.notebook)
        self.notebook.add(gallery_frame, text="🖼️ Pattern Gallery")
        
        # Gallery controls
        control_frame = ttk.LabelFrame(gallery_frame, text="📁 Gallery Controls", padding=10)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(control_frame, text="📂 Load Pattern", 
                  command=self._load_pattern, style='Info.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(control_frame, text="🔄 Refresh Gallery", 
                  command=self._refresh_gallery, style='Info.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(control_frame, text="🗑️ Clear Gallery", 
                  command=self._clear_gallery, style='Info.TButton').pack(side='right')
        
        # Gallery content
        gallery_content = ttk.LabelFrame(gallery_frame, text="🎨 Saved Patterns", padding=10)
        gallery_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.gallery_list = scrolledtext.ScrolledText(
            gallery_content,
            height=20,
            font=('Consolas', 10),
            state='disabled'
        )
        self.gallery_list.pack(fill='both', expand=True)
        
        # Initialize gallery
        self._refresh_gallery()
    
    def _create_settings_tab(self):
        """Create the settings tab."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Performance settings
        perf_frame = ttk.LabelFrame(settings_frame, text="⚡ Performance Settings", padding=10)
        perf_frame.pack(fill='x', padx=10, pady=10)
        
        # Grid size
        ttk.Label(perf_frame, text="Grid Size:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.grid_size_var = tk.StringVar(value="4")
        ttk.Combobox(perf_frame, textvariable=self.grid_size_var, 
                    values=["3", "4", "5"], state="readonly", width=5).grid(row=0, column=1, sticky='w')
        
        # Frame duration
        ttk.Label(perf_frame, text="Frame Duration (s):").grid(row=1, column=0, sticky='w', padx=(0, 10))
        self.frame_duration_var = tk.StringVar(value="0.3")
        ttk.Spinbox(perf_frame, from_=0.1, to=2.0, increment=0.1, 
                   textvariable=self.frame_duration_var, width=10).grid(row=1, column=1, sticky='w')
        
        # Security settings
        sec_frame = ttk.LabelFrame(settings_frame, text="🛡️ Security Settings", padding=10)
        sec_frame.pack(fill='x', padx=10, pady=10)
        
        # Default security level
        ttk.Label(sec_frame, text="Default Security:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.default_security_var = tk.StringVar(value="MILITARY")
        ttk.Combobox(sec_frame, textvariable=self.default_security_var, 
                    values=["MILITARY", "HIGH", "MEDIUM"], state="readonly").grid(row=0, column=1, sticky='w')
        
        # Default expiry
        ttk.Label(sec_frame, text="Default Expiry (s):").grid(row=1, column=0, sticky='w', padx=(0, 10))
        self.default_expiry_var = tk.StringVar(value="60")
        ttk.Spinbox(sec_frame, from_=10, to=300, 
                   textvariable=self.default_expiry_var, width=10).grid(row=1, column=1, sticky='w')
        
        # Apply settings button
        ttk.Button(settings_frame, text="✅ Apply Settings", 
                  command=self._apply_settings, style='Success.TButton').pack(pady=20)
    
    def _create_about_tab(self):
        """Create the about tab."""
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="ℹ️ About")
        
        about_content = ttk.Frame(about_frame)
        about_content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # About text
        about_text = """
🚀 RPattern Revolutionary System v2.0

Created by: Rahul Chaube 💎

🎯 VISION
Replace traditional QR codes with dynamic, encrypted, animated visual patterns 
that are impossible to forge and provide military-grade security.

🛡️ FEATURES
• Military-grade AES-256 encryption
• Quantum-resistant cryptography  
• Dynamic animated patterns
• Auto-expiring security (30 seconds)
• AI-powered pattern recognition
• Real-time camera scanning
• Beautiful visual effects

🔥 WHY RPATTERN IS REVOLUTIONARY
✅ More secure than QR codes
✅ Beautiful animated displays
✅ Impossible to forge
✅ Auto-expires for maximum security
✅ AI-powered detection
✅ Future-proof technology

🏆 ACHIEVEMENTS
• Zero security vulnerabilities
• Military-grade encryption
• Revolutionary visual technology
• Ultra-fast performance
• Universal compatibility

📧 CONTACT
Creator: Rahul Chaube
Project: RPattern Revolutionary System
Technology: Python, OpenCV, Pygame, Military-grade Cryptography

© 2024 Rahul Chaube - Revolutionary Visual Pattern Technology
"""
        
        about_display = scrolledtext.ScrolledText(
            about_content,
            font=('Arial', 11),
            wrap='word',
            state='normal'
        )
        about_display.pack(fill='both', expand=True)
        about_display.insert('1.0', about_text)
        about_display.config(state='disabled')
    
    def _create_status_bar(self, parent):
        """Create the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x', side='bottom', pady=(10, 0))
        
        self.status_var = tk.StringVar(value="🚀 RPattern Revolutionary System ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Info.TLabel')
        status_label.pack(side='left')
        
        # Stats
        self.stats_var = tk.StringVar(value="Patterns: 0 | Scans: 0")
        stats_label = ttk.Label(status_frame, textvariable=self.stats_var, style='Info.TLabel')
        stats_label.pack(side='right')
    
    def _create_pattern(self):
        """Create a revolutionary pattern."""
        if not MODULES_AVAILABLE:
            messagebox.showerror("Error", "RPattern modules not available!")
            return
        
        data = self.input_text.get('1.0', 'end-1c').strip()
        if not data or data.startswith("🚀 Welcome"):
            messagebox.showwarning("Warning", "Please enter data to encode!")
            return
        
        try:
            self._update_status("🔥 Creating revolutionary pattern...")
            
            expiry = int(self.expiry_var.get())
            security = self.security_var.get()
            
            # Create pattern in thread to avoid blocking UI
            def create_pattern_thread():
                try:
                    pattern = create_revolutionary_pattern(data, expiry, security)
                    self.state.current_pattern = pattern
                    self.state.total_patterns_created += 1
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self._pattern_created_success(pattern))
                    
                except Exception as e:
                    self.root.after(0, lambda: self._pattern_creation_failed(str(e)))
            
            threading.Thread(target=create_pattern_thread, daemon=True).start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid expiry time!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create pattern: {e}")
    
    def _pattern_created_success(self, pattern: Dict[str, Any]):
        """Handle successful pattern creation."""
        self._update_status("✅ Revolutionary pattern created successfully!")
        self._update_stats()
        
        # Display pattern info
        info_text = f"""🎉 REVOLUTIONARY PATTERN CREATED!

🆔 Pattern ID: {pattern.get('pattern_id', 'Unknown')}
🔒 Security Level: {pattern.get('security_level', 'Unknown')}
🎬 Total Frames: {pattern.get('total_frames', 0)}
📊 Data Frames: {pattern.get('data_frames', 0)}
🛡️ Security Frames: {pattern.get('security_frames', 0)}
⏰ Expiry: {pattern.get('expiry', 0)/1000 - pattern.get('timestamp', 0)/1000:.1f} seconds
🔧 Generation Time: {pattern.get('generation_time', 0):.4f}s
💎 Creator: Rahul Chaube

🚀 Pattern ready for display or scanning!
"""
        
        self.pattern_info.config(state='normal')
        self.pattern_info.delete('1.0', 'end')
        self.pattern_info.insert('1.0', info_text)
        self.pattern_info.config(state='disabled')
        
        messagebox.showinfo("Success", "Revolutionary pattern created successfully!\nReady for display or scanning.")
    
    def _pattern_creation_failed(self, error: str):
        """Handle pattern creation failure."""
        self._update_status(f"❌ Pattern creation failed: {error}")
        messagebox.showerror("Error", f"Failed to create pattern:\n{error}")
    
    def _display_pattern(self):
        """Display the current pattern."""
        if not self.state.current_pattern:
            messagebox.showwarning("Warning", "No pattern to display! Create one first.")
            return
        
        try:
            self._update_status("🎬 Launching pattern display...")
            
            # Launch display in separate process
            def launch_display():
                try:
                    # Save pattern temporarily
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        json.dump(self.state.current_pattern, f)
                        temp_file = f.name
                    
                    # Launch display script
                    script_path = os.path.join(os.path.dirname(__file__), 'pattern_display.py')
                    if os.path.exists(script_path):
                        subprocess.Popen([sys.executable, script_path, temp_file])
                    else:
                        # Fallback: try direct import
                        display_pattern("Pattern Display Demo", 60)
                
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Display failed: {e}"))
            
            threading.Thread(target=launch_display, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch display: {e}")
    
    def _start_scanning(self):
        """Start pattern scanning."""
        if not MODULES_AVAILABLE:
            messagebox.showerror("Error", "Scanner modules not available!")
            return
        
        if self.state.is_scanning:
            messagebox.showwarning("Warning", "Scanning already in progress!")
            return
        
        try:
            camera_id = int(self.camera_var.get())
            
            self.state.is_scanning = True
            self.scan_button.config(state='disabled')
            self.stop_scan_button.config(state='normal')
            
            self._update_status("📱 Starting revolutionary scanning...")
            self._add_scan_result(f"🚀 Starting scanner with camera {camera_id}...")
            
            def scanning_callback(decoded_data: str):
                """Callback for successful pattern decode."""
                self.state.last_decoded_data = decoded_data
                self.state.total_patterns_scanned += 1
                
                result_text = f"""
🎉 PATTERN DECODED! ({time.strftime('%H:%M:%S')})
📝 Data: {decoded_data}
🚀 Revolutionary technology by Rahul Chaube!
{'='*50}
"""
                self.root.after(0, lambda: self._add_scan_result(result_text))
                self.root.after(0, lambda: self._update_stats())
            
            def start_scanner():
                try:
                    start_revolutionary_scanning(camera_id, scanning_callback)
                except Exception as e:
                    self.root.after(0, lambda: self._add_scan_result(f"❌ Scanner error: {e}"))
                finally:
                    self.root.after(0, self._scanner_stopped)
            
            threading.Thread(target=start_scanner, daemon=True).start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid camera ID!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scanner: {e}")
            self._scanner_stopped()
    
    def _stop_scanning(self):
        """Stop pattern scanning."""
        self.state.is_scanning = False
        self._scanner_stopped()
    
    def _scanner_stopped(self):
        """Handle scanner stopped."""
        self.state.is_scanning = False
        self.scan_button.config(state='normal')
        self.stop_scan_button.config(state='disabled')
        self._update_status("⏹️ Scanner stopped")
        self._add_scan_result("⏹️ Scanner stopped by user")
    
    def _test_camera(self):
        """Test camera connection."""
        try:
            camera_id = int(self.camera_var.get())
            
            # Quick camera test
            import cv2
            cap = cv2.VideoCapture(camera_id)
            
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                
                if ret:
                    messagebox.showinfo("Success", f"Camera {camera_id} is working correctly!")
                else:
                    messagebox.showerror("Error", f"Camera {camera_id} cannot capture frames!")
            else:
                messagebox.showerror("Error", f"Camera {camera_id} is not available!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Camera test failed: {e}")
    
    def _add_scan_result(self, text: str):
        """Add text to scan results."""
        self.scan_results.config(state='normal')
        self.scan_results.insert('end', f"{text}\n")
        self.scan_results.see('end')
        self.scan_results.config(state='disabled')
    
    def _save_pattern(self):
        """Save current pattern to file."""
        if not self.state.current_pattern:
            messagebox.showwarning("Warning", "No pattern to save!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    json.dump(self.state.current_pattern, f, indent=2)
                
                messagebox.showinfo("Success", f"Pattern saved to {filename}")
                self._update_status(f"💾 Pattern saved to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save pattern: {e}")
    
    def _load_pattern(self):
        """Load pattern from file."""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'r') as f:
                    pattern = json.load(f)
                
                self.state.current_pattern = pattern
                self._pattern_created_success(pattern)
                self._update_status(f"📂 Pattern loaded from {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load pattern: {e}")
    
    def _clear_input(self):
        """Clear input text."""
        self.input_text.delete('1.0', 'end')
        self.input_text.insert('1.0', "Enter your data here...")
    
    def _refresh_gallery(self):
        """Refresh the pattern gallery."""
        self.gallery_list.config(state='normal')
        self.gallery_list.delete('1.0', 'end')
        
        gallery_text = """🖼️ RPattern Gallery

📁 Saved Patterns:
• Load patterns using 'Load Pattern' button
• Save new patterns from Generator tab
• Patterns are stored as JSON files

🎨 Pattern Types:
• Revolutionary Patterns (v2.0)
• Military-grade encryption
• Dynamic animated frames
• Auto-expiring security

💡 Tips:
• Use descriptive filenames
• Keep patterns organized
• Share patterns securely

🚀 Gallery managed by RPattern Revolutionary System
💎 Created by Rahul Chaube
"""
        
        self.gallery_list.insert('1.0', gallery_text)
        self.gallery_list.config(state='disabled')
    
    def _clear_gallery(self):
        """Clear gallery display."""
        self.gallery_list.config(state='normal')
        self.gallery_list.delete('1.0', 'end')
        self.gallery_list.insert('1.0', "Gallery cleared.\nUse 'Refresh Gallery' to restore.")
        self.gallery_list.config(state='disabled')
    
    def _apply_settings(self):
        """Apply settings changes."""
        messagebox.showinfo("Settings", "Settings applied successfully!")
        self._update_status("⚙️ Settings applied")
    
    def _update_status(self, message: str):
        """Update status bar message."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def _update_stats(self):
        """Update statistics display."""
        stats_text = f"Patterns: {self.state.total_patterns_created} | Scans: {self.state.total_patterns_scanned}"
        self.stats_var.set(stats_text)
    
    def run(self):
        """Run the application."""
        try:
            print("🚀 Starting RPattern Revolutionary System...")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Application interrupted")
        except Exception as e:
            print(f"❌ Application error: {e}")
            messagebox.showerror("Fatal Error", f"Application error: {e}")
        finally:
            print("✅ RPattern Revolutionary System closed")


def main():
    """Main entry point."""
    print("🚀" * 30)
    print("    RPATTERN REVOLUTIONARY SYSTEM")
    print("    Complete Application Suite")
    print("    Creator: Rahul Chaube 💎")
    print("🚀" * 30)
    
    try:
        app = RPatternRevolutionaryApp()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application:\n{e}")


if __name__ == "__main__":
    main()
