"""
📱 RPattern Revolutionary Scanner v2.0 - AI-Powered Visual Detection
Author: Rahul Chaube
Vision: Advanced computer vision to decode dynamic patterns

This module uses OpenCV to scan and decode RPatterns in real-time.
"""

import cv2
import numpy as np
import time
import threading
import json
from typing import Dict, Any, List, Tuple, Optional, Callable
from rpattern_revolutionary import RPatternCore


class RevolutionaryScanner:
    """
    Revolutionary AI-powered scanner for RPatterns.
    Uses advanced computer vision to detect and decode dynamic patterns.
    """
    
    def __init__(self, camera_id: int = 0):
        """Initialize the revolutionary scanner."""
        self.camera_id = camera_id
        self.cap = None
        self.is_scanning = False
        self.decoder = RPatternCore()
        
        # Pattern detection state
        self.detected_frames = []
        self.frame_buffer_size = 100  # Store last 100 frames
        self.detection_threshold = 0.8
        self.pattern_region = None
        
        # Color detection configuration
        self.color_tolerance = 30
        self.min_pattern_size = 100  # Minimum pattern size in pixels
        self.max_pattern_size = 600  # Maximum pattern size
        
        # Scanning statistics
        self.total_scans = 0
        self.successful_decodes = 0
        self.last_decode_time = 0
        
        print("📱 Revolutionary Scanner initialized")
        print(f"🎥 Camera ID: {camera_id}")
        print(f"🔍 Detection threshold: {self.detection_threshold}")
        
    def _initialize_camera(self) -> bool:
        """Initialize the camera."""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                print(f"❌ Cannot open camera {self.camera_id}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Test frame
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Cannot read from camera")
                return False
            
            self.frame_height, self.frame_width = frame.shape[:2]
            print(f"✅ Camera initialized: {self.frame_width}x{self.frame_height}")
            return True
            
        except Exception as e:
            print(f"❌ Camera initialization failed: {e}")
            return False
    
    def _detect_pattern_region(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect potential pattern region in frame.
        Returns (x, y, width, height) of detected region.
        """
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create masks for bright colors (potential pattern colors)
        lower_bright = np.array([0, 100, 100])
        upper_bright = np.array([179, 255, 255])
        bright_mask = cv2.inRange(hsv, lower_bright, upper_bright)
        
        # Find contours
        contours, _ = cv2.findContours(bright_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find largest contour that could be a pattern
        for contour in sorted(contours, key=cv2.contourArea, reverse=True):
            area = cv2.contourArea(contour)
            
            if self.min_pattern_size**2 < area < self.max_pattern_size**2:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Check if region is roughly square (patterns should be square)
                aspect_ratio = w / h
                if 0.7 < aspect_ratio < 1.3:  # Roughly square
                    return (x, y, w, h)
        
        return None
    
    def _extract_pattern_colors(self, frame: np.ndarray, region: Tuple[int, int, int, int]) -> Optional[List[List[Tuple[int, int, int]]]]:
        """
        Extract color grid from detected pattern region.
        """
        x, y, w, h = region
        
        # Extract pattern region
        pattern_region = frame[y:y+h, x:x+w]
        
        # Resize to standard grid size (4x4)
        grid_size = 4
        cell_width = w // grid_size
        cell_height = h // grid_size
        
        color_grid = []
        
        for row in range(grid_size):
            color_row = []
            for col in range(grid_size):
                # Calculate cell boundaries
                cell_x = col * cell_width
                cell_y = row * cell_height
                
                # Extract cell region
                cell = pattern_region[cell_y:cell_y+cell_height, cell_x:cell_x+cell_width]
                
                if cell.size == 0:
                    color_row.append((128, 128, 128))  # Gray fallback
                    continue
                
                # Get average color of cell
                avg_color = np.mean(cell, axis=(0, 1))
                
                # Convert BGR to RGB
                r, g, b = avg_color[2], avg_color[1], avg_color[0]
                color_row.append((int(r), int(g), int(b)))
            
            color_grid.append(color_row)
        
        return color_grid
    
    def _is_valid_pattern_frame(self, color_grid: List[List[Tuple[int, int, int]]]) -> bool:
        """
        Check if extracted colors represent a valid pattern frame.
        """
        if not color_grid or len(color_grid) != 4:
            return False
        
        # Check for security frame markers
        first_color = color_grid[0][0]
        
        # Check for start frame (white-ish)
        if self._color_distance(first_color, (255, 255, 255)) < 50:
            return True
        
        # Check for end frame (black-ish)
        if self._color_distance(first_color, (0, 0, 0)) < 50:
            return True
        
        # Check for data frames (should have distinct colors)
        unique_colors = set()
        for row in color_grid:
            for color in row:
                unique_colors.add(color)
        
        # Pattern frames should have some color variation
        return len(unique_colors) > 1
    
    def _color_distance(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
        """Calculate Euclidean distance between two colors."""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return np.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)
    
    def _add_frame_to_buffer(self, color_grid: List[List[Tuple[int, int, int]]]):
        """Add detected frame to buffer."""
        self.detected_frames.append({
            'timestamp': time.time(),
            'colors': color_grid
        })
        
        # Keep buffer size manageable
        if len(self.detected_frames) > self.frame_buffer_size:
            self.detected_frames.pop(0)
    
    def _attempt_decode(self) -> Optional[str]:
        """
        Attempt to decode pattern from collected frames.
        """
        if len(self.detected_frames) < 4:  # Need minimum frames
            return None
        
        try:
            # Extract just the color grids
            color_frames = [frame['colors'] for frame in self.detected_frames]
            
            # Try to decode
            decoded_data = self.decoder.decode_revolutionary_pattern(color_frames)
            
            if decoded_data:
                self.successful_decodes += 1
                self.last_decode_time = time.time()
                
                # Clear buffer after successful decode
                self.detected_frames.clear()
                
                return decoded_data
        
        except Exception as e:
            print(f"🔍 Decode attempt failed: {e}")
        
        return None
    
    def _draw_scanning_ui(self, frame: np.ndarray) -> np.ndarray:
        """Draw scanning UI overlay on frame."""
        overlay = frame.copy()
        
        # Draw title
        cv2.putText(overlay, "RPattern Revolutionary Scanner v2.0", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.putText(overlay, "by Rahul Chaube", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        
        # Draw scanning info
        info_y = 100
        cv2.putText(overlay, f"Frames Detected: {len(self.detected_frames)}", 
                   (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        info_y += 30
        cv2.putText(overlay, f"Total Scans: {self.total_scans}", 
                   (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        info_y += 30
        cv2.putText(overlay, f"Successful Decodes: {self.successful_decodes}", 
                   (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Draw pattern region if detected
        if self.pattern_region:
            x, y, w, h = self.pattern_region
            cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(overlay, "PATTERN DETECTED", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw crosshair in center
        center_x, center_y = self.frame_width // 2, self.frame_height // 2
        cv2.line(overlay, (center_x - 20, center_y), (center_x + 20, center_y), (255, 0, 0), 2)
        cv2.line(overlay, (center_x, center_y - 20), (center_x, center_y + 20), (255, 0, 0), 2)
        
        # Draw instructions
        instructions = [
            "Point camera at RPattern",
            "Press 'q' to quit",
            "Press 's' to save frame",
            "Press 'r' to reset buffer"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(overlay, instruction, (10, self.frame_height - 100 + i*25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return overlay
    
    def scan_revolutionary_patterns(self, on_decode: Callable[[str], None] = None) -> bool:
        """
        Start revolutionary pattern scanning.
        
        Args:
            on_decode: Callback function called when pattern is decoded
            
        Returns:
            True if scanning completed successfully
        """
        if not self._initialize_camera():
            return False
        
        self.is_scanning = True
        self.total_scans = 0
        self.successful_decodes = 0
        
        print("🚀 Starting Revolutionary RPattern scanning...")
        print("📱 Point camera at RPattern to decode")
        print("🎮 Press 'q' to quit, 's' to save frame, 'r' to reset")
        
        try:
            while self.is_scanning:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to read frame")
                    break
                
                self.total_scans += 1
                
                # Detect pattern region
                self.pattern_region = self._detect_pattern_region(frame)
                
                if self.pattern_region:
                    # Extract colors from pattern
                    color_grid = self._extract_pattern_colors(frame, self.pattern_region)
                    
                    if color_grid and self._is_valid_pattern_frame(color_grid):
                        self._add_frame_to_buffer(color_grid)
                        
                        # Attempt decode every few frames
                        if len(self.detected_frames) % 5 == 0:
                            decoded_data = self._attempt_decode()
                            
                            if decoded_data:
                                print(f"\n🎉 REVOLUTIONARY PATTERN DECODED!")
                                print(f"📝 Data: {decoded_data}")
                                print(f"⏰ Decode time: {time.time() - self.last_decode_time:.3f}s")
                                
                                if on_decode:
                                    on_decode(decoded_data)
                                
                                # Show success overlay
                                success_frame = frame.copy()
                                cv2.putText(success_frame, "DECODE SUCCESS!", 
                                           (50, self.frame_height//2), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                                cv2.imshow('Revolutionary Scanner', success_frame)
                                cv2.waitKey(2000)  # Show for 2 seconds
                
                # Draw UI overlay
                display_frame = self._draw_scanning_ui(frame)
                
                # Show frame
                cv2.imshow('Revolutionary Scanner', display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save current frame
                    filename = f"rpattern_frame_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"💾 Frame saved: {filename}")
                elif key == ord('r'):
                    # Reset frame buffer
                    self.detected_frames.clear()
                    print("🔄 Frame buffer reset")
        
        except KeyboardInterrupt:
            print("\n🛑 Scanning interrupted by user")
        
        except Exception as e:
            print(f"❌ Scanning error: {e}")
        
        finally:
            self.is_scanning = False
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            
            print(f"\n📊 Revolutionary Scanning Statistics:")
            print(f"   🎬 Total frames scanned: {self.total_scans}")
            print(f"   ✅ Successful decodes: {self.successful_decodes}")
            print(f"   📈 Success rate: {(self.successful_decodes/max(1,self.total_scans)*100):.1f}%")
            print("✅ Revolutionary Scanner closed")
        
        return True


def start_revolutionary_scanning(camera_id: int = 0, on_decode: Callable[[str], None] = None) -> bool:
    """
    Quick function to start revolutionary pattern scanning.
    
    Args:
        camera_id: Camera index to use
        on_decode: Function to call when pattern is decoded
        
    Returns:
        True if scanning completed successfully
    """
    scanner = RevolutionaryScanner(camera_id)
    return scanner.scan_revolutionary_patterns(on_decode)


if __name__ == "__main__":
    print("📱" * 20)
    print("    RPATTERN REVOLUTIONARY SCANNER v2.0")
    print("    Creator: Rahul Chaube")
    print("    AI-Powered Visual Detection!")
    print("📱" * 20)
    
    def pattern_decoded_callback(data: str):
        """Callback for when pattern is decoded."""
        print(f"\n🎊 REVOLUTIONARY PATTERN DECODED! 🎊")
        print(f"📝 Decoded Data: {data}")
        print(f"🚀 RPattern revolutionary technology by Rahul Chaube works!")
        print("-" * 50)
    
    print("\n🚀 Starting Revolutionary Pattern Scanner v2.0...")
    print("📱 Make sure you have a camera connected")
    print("🎯 Point camera at RPattern to decode")
    
    try:
        # Start revolutionary scanning
        success = start_revolutionary_scanning(camera_id=0, on_decode=pattern_decoded_callback)
        
        if success:
            print("\n🎉 Revolutionary scanning completed successfully!")
        else:
            print("\n❌ Revolutionary scanning failed - check camera connection")
    
    except KeyboardInterrupt:
        print("\n👋 Revolutionary scanner interrupted by user")
    
    except Exception as e:
        print(f"\n❌ Revolutionary scanner error: {e}")
        print("💡 Try checking camera permissions and connections")
    
    print("\n🎉 Thank you for using RPattern Revolutionary Scanner v2.0!")
    print("💎 Created by Rahul Chaube")
