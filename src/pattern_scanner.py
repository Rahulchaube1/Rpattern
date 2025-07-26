"""
RPattern Scanner - Camera-based Pattern Recognition
Creator: Rahul Chaube 🚀

Uses OpenCV to capture and decode RPatterns from camera input.
"""

import cv2
import numpy as np
import time
import threading
from typing import List, Tuple, Optional, Dict, Any
from collections import defaultdict, deque
from rpattern_core import RPattern


class ColorDetector:
    """Detects and classifies colors in RPattern frames."""
    
    # Color ranges in HSV for better detection
    COLOR_RANGES = {
        'red': [(0, 100, 100), (10, 255, 255)],
        'red2': [(170, 100, 100), (180, 255, 255)],  # Red wraps around in HSV
        'green': [(40, 100, 100), (80, 255, 255)],
        'blue': [(100, 100, 100), (130, 255, 255)],
        'yellow': [(20, 100, 100), (40, 255, 255)],
        'white': [(0, 0, 200), (180, 30, 255)],
        'black': [(0, 0, 0), (180, 255, 50)]
    }
    
    # RGB color mapping (same as in rpattern_core)
    RGB_COLORS = {
        (255, 0, 0): '00',      # Red
        (0, 255, 0): '01',      # Green
        (0, 0, 255): '10',      # Blue
        (255, 255, 0): '11',    # Yellow
        (255, 255, 255): 'sync_start',  # White (sync)
        (0, 0, 0): 'sync_end'           # Black (sync)
    }
    
    def __init__(self):
        """Initialize color detector."""
        self.tolerance = 50  # RGB tolerance for color matching
        
    def detect_dominant_color(self, roi: np.ndarray) -> Tuple[int, int, int]:
        """
        Detect the dominant color in a region of interest.
        
        Args:
            roi: Region of interest (BGR image patch)
            
        Returns:
            RGB tuple of dominant color
        """
        # Convert BGR to RGB
        rgb_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        
        # Calculate mean color
        mean_color = np.mean(rgb_roi.reshape(-1, 3), axis=0).astype(int)
        
        # Find closest predefined color
        min_distance = float('inf')
        closest_color = (255, 255, 255)  # Default to white
        
        for rgb_color in self.RGB_COLORS.keys():
            distance = np.sqrt(np.sum((np.array(rgb_color) - mean_color) ** 2))
            if distance < min_distance:
                min_distance = distance
                closest_color = rgb_color
                
        return closest_color
    
    def classify_color(self, rgb_color: Tuple[int, int, int]) -> str:
        """Classify RGB color to bit pattern or sync signal."""
        return self.RGB_COLORS.get(rgb_color, '00')


class RPatternScanner:
    """Main scanner class for detecting and decoding RPatterns."""
    
    def __init__(self, camera_index: int = 0):
        """Initialize the scanner."""
        self.camera_index = camera_index
        self.cap = None
        self.color_detector = ColorDetector()
        self.rpattern = RPattern()
        
        # Detection state
        self.is_scanning = False
        self.captured_frames = []
        self.frame_timestamps = []
        self.detection_start_time = None
        
        # Pattern detection parameters
        self.min_pattern_size = 100  # Minimum pattern size in pixels
        self.max_detection_time = 30  # Maximum time to capture pattern (seconds)
        self.grid_size = 3  # 3x3 pattern grid
        
        # Frame sequence buffer
        self.frame_buffer = deque(maxlen=20)  # Keep last 20 frames
        self.sync_detected = False
        
        # GUI elements
        self.window_name = "🚀 RPattern Scanner - by Rahul Chaube"
        
    def initialize_camera(self) -> bool:
        """Initialize camera capture."""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print(f"❌ Failed to open camera {self.camera_index}")
                return False
                
            # Set camera properties for better detection
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"✅ Camera {self.camera_index} initialized")
            return True
            
        except Exception as e:
            print(f"❌ Camera initialization error: {e}")
            return False
    
    def detect_pattern_region(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect the RPattern region in the frame.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            (x, y, width, height) of detected pattern region or None
        """
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detect edges
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Look for rectangular contours that could be the pattern
        for contour in contours:
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's roughly rectangular (4 vertices)
            if len(approx) >= 4:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Check size constraints
                if w >= self.min_pattern_size and h >= self.min_pattern_size:
                    # Check aspect ratio (should be roughly square)
                    aspect_ratio = w / h
                    if 0.8 <= aspect_ratio <= 1.2:
                        return (x, y, w, h)
                        
        return None
    
    def extract_grid_colors(self, frame: np.ndarray, pattern_region: Tuple[int, int, int, int]) -> List[List[Tuple[int, int, int]]]:
        """
        Extract colors from the 3x3 grid pattern.
        
        Args:
            frame: Input frame
            pattern_region: (x, y, width, height) of pattern region
            
        Returns:
            3x3 grid of RGB colors
        """
        x, y, w, h = pattern_region
        
        # Extract pattern ROI
        pattern_roi = frame[y:y+h, x:x+w]
        
        # Divide into 3x3 grid
        cell_height = h // self.grid_size
        cell_width = w // self.grid_size
        
        grid_colors = []
        
        for row in range(self.grid_size):
            row_colors = []
            for col in range(self.grid_size):
                # Calculate cell boundaries
                cell_y = row * cell_height
                cell_x = col * cell_width
                
                # Extract cell ROI (use center portion to avoid edge effects)
                margin = min(cell_width, cell_height) // 4
                cell_roi = pattern_roi[
                    cell_y + margin:cell_y + cell_height - margin,
                    cell_x + margin:cell_x + cell_width - margin
                ]
                
                if cell_roi.size > 0:
                    # Detect dominant color in this cell
                    dominant_color = self.color_detector.detect_dominant_color(cell_roi)
                    row_colors.append(dominant_color)
                else:
                    row_colors.append((255, 255, 255))  # Default to white
                    
            grid_colors.append(row_colors)
            
        return grid_colors
    
    def process_frame_sequence(self) -> Optional[str]:
        """
        Process captured frame sequence to decode RPattern.
        
        Returns:
            Decoded data string or None if decoding fails
        """
        if len(self.captured_frames) < 3:  # Need at least start sync + data + end sync
            return None
            
        print(f"🔍 Processing {len(self.captured_frames)} captured frames...")
        
        # Try to decode the captured frames
        decoded_data = self.rpattern.decode_frames(self.captured_frames)
        
        if decoded_data:
            print(f"✅ RPattern decoded successfully!")
            return decoded_data
        else:
            print("❌ Failed to decode RPattern")
            return None
    
    def draw_detection_overlay(self, frame: np.ndarray, pattern_region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Draw detection overlay on the frame."""
        overlay = frame.copy()
        height, width = frame.shape[:2]
        
        # Draw title
        cv2.putText(overlay, "RPattern Scanner by Rahul Chaube", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 150), 2)
        
        # Draw scanning status
        status_text = "🎯 SCANNING..." if self.is_scanning else "👁️  Looking for pattern..."
        cv2.putText(overlay, status_text, 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw pattern region if detected
        if pattern_region:
            x, y, w, h = pattern_region
            
            # Draw bounding rectangle
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Draw grid lines
            cell_width = w // self.grid_size
            cell_height = h // self.grid_size
            
            for i in range(1, self.grid_size):
                # Vertical lines
                cv2.line(overlay, (x + i * cell_width, y), 
                        (x + i * cell_width, y + h), (0, 255, 0), 1)
                # Horizontal lines
                cv2.line(overlay, (x, y + i * cell_height), 
                        (x + w, y + i * cell_height), (0, 255, 0), 1)
                        
            # Draw detection progress
            if self.is_scanning:
                progress = len(self.captured_frames)
                cv2.putText(overlay, f"Frames captured: {progress}", 
                           (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Draw instructions
        instructions = [
            "Position RPattern in camera view",
            "Pattern will be auto-detected",
            "Press 'r' to reset detection",
            "Press 'q' to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(overlay, instruction, 
                       (10, height - 100 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        return overlay
    
    def start_scanning(self):
        """Start the scanning process."""
        if not self.initialize_camera():
            return
            
        print("🚀 RPattern Scanner started")
        print("🎯 Position an RPattern in front of the camera...")
        
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to read from camera")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect pattern region
                pattern_region = self.detect_pattern_region(frame)
                
                if pattern_region and not self.is_scanning:
                    # Start pattern detection
                    self.is_scanning = True
                    self.captured_frames = []
                    self.frame_timestamps = []
                    self.detection_start_time = time.time()
                    self.sync_detected = False
                    print("🎯 Pattern detected! Starting capture...")
                
                if self.is_scanning and pattern_region:
                    # Extract colors from current frame
                    grid_colors = self.extract_grid_colors(frame, pattern_region)
                    
                    # Check for synchronization frames
                    center_color = grid_colors[1][1]  # Middle cell
                    color_class = self.color_detector.classify_color(center_color)
                    
                    if color_class == 'sync_start' and not self.sync_detected:
                        print("🔄 Start sync detected")
                        self.sync_detected = True
                        self.captured_frames = [grid_colors]
                        self.frame_timestamps = [time.time()]
                    elif self.sync_detected:
                        self.captured_frames.append(grid_colors)
                        self.frame_timestamps.append(time.time())
                        
                        if color_class == 'sync_end':
                            print("🏁 End sync detected")
                            # Try to decode the pattern
                            decoded_data = self.process_frame_sequence()
                            
                            if decoded_data:
                                print(f"🎉 RPattern Detected: {decoded_data}")
                                # Show success message
                                self.show_success_message(frame, decoded_data)
                            
                            # Reset detection
                            self.is_scanning = False
                            self.sync_detected = False
                            
                    # Check timeout
                    if time.time() - self.detection_start_time > self.max_detection_time:
                        print("⏰ Detection timeout")
                        self.is_scanning = False
                        self.sync_detected = False
                
                # Draw overlay
                display_frame = self.draw_detection_overlay(frame, pattern_region)
                
                # Show frame
                cv2.imshow(self.window_name, display_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    # Reset detection
                    self.is_scanning = False
                    self.sync_detected = False
                    self.captured_frames = []
                    print("🔄 Detection reset")
                    
        except KeyboardInterrupt:
            print("🛑 Scanner interrupted by user")
            
        finally:
            self.cleanup()
    
    def show_success_message(self, frame: np.ndarray, decoded_data: str):
        """Show success message overlay."""
        overlay = frame.copy()
        height, width = frame.shape[:2]
        
        # Draw green background
        cv2.rectangle(overlay, (50, height//2 - 100), (width - 50, height//2 + 100), (0, 255, 0), -1)
        
        # Draw success text
        cv2.putText(overlay, "SUCCESS!", 
                   (width//2 - 100, height//2 - 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
        
        cv2.putText(overlay, f"Detected: {decoded_data}", 
                   (60, height//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        cv2.putText(overlay, "Press any key to continue...", 
                   (width//2 - 150, height//2 + 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        cv2.imshow(self.window_name, overlay)
        cv2.waitKey(3000)  # Show for 3 seconds or until key press
    
    def cleanup(self):
        """Clean up resources."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("🧹 Scanner cleanup complete")


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="🚀 RPattern Scanner by Rahul Chaube")
    parser.add_argument("--camera", "-c", type=int, default=0,
                       help="Camera index to use")
    
    args = parser.parse_args()
    
    print("🚀 RPattern Scanner - Next-Gen Visual ID Recognition")
    print(f"Creator: Rahul Chaube")
    print(f"Camera: {args.camera}")
    print("-" * 50)
    
    # Start scanner
    scanner = RPatternScanner(camera_index=args.camera)
    scanner.start_scanning()


if __name__ == "__main__":
    main()
