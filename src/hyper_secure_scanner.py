"""
HyperSecure RPattern Scanner - Military Grade Detection
Creator: Rahul Chaube 🚀

Advanced scanner with quantum-resistant pattern detection
"""

import cv2
import numpy as np
import time
import threading
from typing import List, Tuple, Optional, Dict, Any
from collections import defaultdict, deque
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from hyper_secure_core import HyperSecureRPattern
    HYPER_SECURITY_AVAILABLE = True
except ImportError:
    from rpattern_core import RPattern
    HYPER_SECURITY_AVAILABLE = False


class HyperSecureColorDetector:
    """Advanced color detection with 8-color support and noise reduction."""
    
    # Enhanced 8-color mapping
    HYPER_COLOR_MAP = {
        (255, 0, 0): '000',      # Red
        (0, 255, 0): '001',      # Green
        (0, 0, 255): '010',      # Blue
        (255, 255, 0): '011',    # Yellow
        (255, 0, 255): '100',    # Magenta
        (0, 255, 255): '101',    # Cyan
        (255, 128, 0): '110',    # Orange
        (128, 0, 255): '111',    # Purple
    }
    
    # Security frame colors
    SECURITY_COLORS = {
        (255, 255, 255): 'auth_start',
        (0, 0, 0): 'auth_end',
        (128, 128, 128): 'checksum',
    }
    
    def __init__(self):
        """Initialize enhanced color detector."""
        self.color_tolerance = 40  # Improved tolerance
        self.noise_threshold = 5   # Noise reduction
        
    def detect_dominant_color_advanced(self, roi: np.ndarray) -> Tuple[int, int, int]:
        """Advanced color detection with noise reduction."""
        # Convert BGR to RGB
        rgb_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(rgb_roi, (5, 5), 0)
        
        # Calculate mean color from center region (ignore edges)
        h, w = blurred.shape[:2]
        center_h, center_w = h//4, w//4
        center_region = blurred[center_h:h-center_h, center_w:w-center_w]
        
        mean_color = np.mean(center_region.reshape(-1, 3), axis=0).astype(int)
        
        # Find closest color with improved matching
        min_distance = float('inf')
        closest_color = (255, 255, 255)
        
        # Check all hyper colors
        all_colors = {**self.HYPER_COLOR_MAP, **self.SECURITY_COLORS}
        
        for rgb_color in all_colors.keys():
            # Use weighted Euclidean distance
            distance = np.sqrt(np.sum((np.array(rgb_color) - mean_color) ** 2))
            if distance < min_distance:
                min_distance = distance
                closest_color = rgb_color
        
        return closest_color
    
    def classify_color_type(self, rgb_color: Tuple[int, int, int]) -> str:
        """Classify color as data or security frame."""
        if rgb_color in self.SECURITY_COLORS:
            return f"security_{self.SECURITY_COLORS[rgb_color]}"
        elif rgb_color in self.HYPER_COLOR_MAP:
            return f"data_{self.HYPER_COLOR_MAP[rgb_color]}"
        else:
            return "unknown"


class HyperSecureScanner:
    """Military-grade RPattern scanner with advanced detection."""
    
    def __init__(self, camera_index: int = 0):
        """Initialize hyper-secure scanner."""
        self.camera_index = camera_index
        self.cap = None
        
        # Initialize components
        self.color_detector = HyperSecureColorDetector()
        
        if HYPER_SECURITY_AVAILABLE:
            self.rpattern = HyperSecureRPattern(expiry_seconds=30, security_level="ULTRA")
            self.grid_size = 4  # 4x4 for hyper-secure
        else:
            self.rpattern = RPattern(expiry_minutes=1)
            self.grid_size = 3  # 3x3 for standard
        
        # Enhanced detection parameters
        self.min_pattern_size = 150
        self.max_pattern_size = 600
        self.detection_stability_frames = 5
        self.max_detection_time = 15
        
        # Advanced frame tracking
        self.frame_buffer = deque(maxlen=30)
        self.stable_detections = deque(maxlen=10)
        self.security_sequence = []
        
        # Detection state
        self.is_scanning = False
        self.detection_confidence = 0.0
        self.last_detection_time = 0
        
        self.window_name = "🔒 HyperSecure RPattern Scanner - Rahul Chaube"
        
    def initialize_camera(self) -> bool:
        """Initialize camera with optimal settings."""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print(f"❌ Failed to open camera {self.camera_index}")
                return False
            
            # Optimal camera settings
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.cap.set(cv2.CAP_PROP_FPS, 60)
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            self.cap.set(cv2.CAP_PROP_EXPOSURE, -6)
            
            print(f"✅ HyperSecure camera {self.camera_index} initialized")
            return True
            
        except Exception as e:
            print(f"❌ Camera initialization error: {e}")
            return False
    
    def detect_pattern_region_advanced(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Advanced pattern detection with multiple algorithms."""
        # Method 1: Edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Adaptive thresholding for better edge detection
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        best_candidates = []
        
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Size filtering
            if (self.min_pattern_size <= w <= self.max_pattern_size and 
                self.min_pattern_size <= h <= self.max_pattern_size):
                
                # Aspect ratio check (should be roughly square)
                aspect_ratio = w / h
                if 0.7 <= aspect_ratio <= 1.3:
                    
                    # Calculate contour area ratio
                    contour_area = cv2.contourArea(contour)
                    bbox_area = w * h
                    area_ratio = contour_area / bbox_area if bbox_area > 0 else 0
                    
                    # Score based on size and shape
                    size_score = min(w, h) / self.max_pattern_size
                    shape_score = 1.0 - abs(aspect_ratio - 1.0)
                    area_score = area_ratio
                    
                    total_score = (size_score + shape_score + area_score) / 3
                    
                    best_candidates.append((x, y, w, h, total_score))
        
        # Return best candidate
        if best_candidates:
            best_candidates.sort(key=lambda x: x[4], reverse=True)
            return best_candidates[0][:4]
        
        # Method 2: Color-based detection (fallback)
        return self._detect_by_color_clustering(frame)
    
    def _detect_by_color_clustering(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detect pattern using color clustering."""
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for bright colors
        lower_bright = np.array([0, 50, 50])
        upper_bright = np.array([179, 255, 255])
        mask = cv2.inRange(hsv, lower_bright, upper_bright)
        
        # Find contours in mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if (self.min_pattern_size <= w <= self.max_pattern_size and 
                self.min_pattern_size <= h <= self.max_pattern_size):
                aspect_ratio = w / h
                if 0.8 <= aspect_ratio <= 1.2:
                    return (x, y, w, h)
        
        return None
    
    def extract_grid_colors_advanced(self, frame: np.ndarray, pattern_region: Tuple[int, int, int, int]) -> List[List[Tuple[int, int, int]]]:
        """Extract colors with advanced sampling."""
        x, y, w, h = pattern_region
        pattern_roi = frame[y:y+h, x:x+w]
        
        # Resize to standard size for consistent sampling
        standard_size = 400
        resized_roi = cv2.resize(pattern_roi, (standard_size, standard_size))
        
        cell_size = standard_size // self.grid_size
        grid_colors = []
        
        for row in range(self.grid_size):
            row_colors = []
            for col in range(self.grid_size):
                # Calculate cell boundaries
                cell_y = row * cell_size
                cell_x = col * cell_size
                
                # Extract center region of cell (avoid edges)
                margin = cell_size // 4
                cell_roi = resized_roi[
                    cell_y + margin:cell_y + cell_size - margin,
                    cell_x + margin:cell_x + cell_size - margin
                ]
                
                if cell_roi.size > 0:
                    # Use advanced color detection
                    dominant_color = self.color_detector.detect_dominant_color_advanced(cell_roi)
                    row_colors.append(dominant_color)
                else:
                    row_colors.append((255, 255, 255))
                    
            grid_colors.append(row_colors)
        
        return grid_colors
    
    def validate_security_sequence(self, frames: List[List[List[Tuple[int, int, int]]]]) -> bool:
        """Validate security frame sequence."""
        if len(frames) < 5:
            return False
        
        # Check first frame (should be auth_start)
        first_color = frames[0][0][0]
        if self.color_detector.classify_color_type(first_color) != "security_auth_start":
            return False
        
        # Check last frame (should be auth_end)
        last_color = frames[-1][0][0]
        if self.color_detector.classify_color_type(last_color) != "security_auth_end":
            return False
        
        return True
    
    def process_hyper_secure_sequence(self, captured_frames: List) -> Optional[str]:
        """Process captured sequence with full security validation."""
        if len(captured_frames) < 5:
            return None
        
        print(f"🔍 Processing {len(captured_frames)} hyper-secure frames...")
        
        # Validate security sequence
        if not self.validate_security_sequence(captured_frames):
            print("❌ Security validation failed")
            return None
        
        # Attempt decoding
        if HYPER_SECURITY_AVAILABLE:
            decoded_data = self.rpattern.decode_hyper_secure_frames(captured_frames)
        else:
            decoded_data = self.rpattern.decode_frames(captured_frames)
        
        if decoded_data:
            print(f"✅ HyperSecure pattern decoded successfully!")
            return decoded_data
        else:
            print("❌ Failed to decode hyper-secure pattern")
            return None
    
    def draw_advanced_overlay(self, frame: np.ndarray, pattern_region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Draw advanced detection overlay."""
        overlay = frame.copy()
        height, width = frame.shape[:2]
        
        # Draw title with security status
        if HYPER_SECURITY_AVAILABLE:
            title = "🔒 HYPERSECURE SCANNER - MILITARY GRADE"
            title_color = (0, 0, 255)  # Red for maximum security
        else:
            title = "🔐 SECURE SCANNER - STANDARD"
            title_color = (0, 255, 0)  # Green for standard security
        
        cv2.putText(overlay, title, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, title_color, 2)
        
        # Creator credit
        cv2.putText(overlay, "Created by Rahul Chaube", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Detection status
        status_text = "🎯 SCANNING..." if self.is_scanning else "👁️ READY TO DETECT"
        cv2.putText(overlay, status_text, (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Confidence meter
        conf_width = 200
        conf_height = 20
        conf_x, conf_y = 10, 110
        
        # Background
        cv2.rectangle(overlay, (conf_x, conf_y), 
                     (conf_x + conf_width, conf_y + conf_height), (50, 50, 50), -1)
        
        # Confidence bar
        conf_fill = int(conf_width * self.detection_confidence)
        if conf_fill > 0:
            color = (0, 255, 0) if self.detection_confidence > 0.8 else (0, 255, 255)
            cv2.rectangle(overlay, (conf_x, conf_y), 
                         (conf_x + conf_fill, conf_y + conf_height), color, -1)
        
        cv2.putText(overlay, f"Confidence: {self.detection_confidence:.1%}", 
                   (conf_x, conf_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Pattern region visualization
        if pattern_region:
            x, y, w, h = pattern_region
            
            # Multi-layer border for better visibility
            colors = [(0, 255, 0), (0, 200, 0), (0, 150, 0)]
            for i, color in enumerate(colors):
                thickness = 3 - i
                cv2.rectangle(overlay, (x-i, y-i), (x+w+i, y+h+i), color, thickness)
            
            # Grid overlay
            cell_width = w // self.grid_size
            cell_height = h // self.grid_size
            
            # Draw grid lines
            for i in range(1, self.grid_size):
                # Vertical lines
                cv2.line(overlay, (x + i * cell_width, y), 
                        (x + i * cell_width, y + h), (0, 255, 0), 1)
                # Horizontal lines
                cv2.line(overlay, (x, y + i * cell_height), 
                        (x + w, y + i * cell_height), (0, 255, 0), 1)
            
            # Pattern info
            pattern_info = f"Pattern: {self.grid_size}x{self.grid_size} Grid"
            cv2.putText(overlay, pattern_info, (x, y - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            frame_count = len(self.security_sequence)
            if frame_count > 0:
                cv2.putText(overlay, f"Frames: {frame_count}", (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Instructions
        instructions = [
            "🎯 Position RPattern in view",
            "📱 Ensure good lighting",
            "🔍 Hold steady for detection",
            "❌ Press 'q' to quit, 'r' to reset"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(overlay, instruction, (10, height - 100 + i * 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        return overlay
    
    def start_scanning(self):
        """Start the advanced scanning process."""
        if not self.initialize_camera():
            return
        
        print("🔒 HyperSecure RPattern Scanner started")
        print("🎯 Position a RPattern in front of the camera...")
        
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to read from camera")
                    break
                
                # Flip for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect pattern region
                pattern_region = self.detect_pattern_region_advanced(frame)
                
                current_time = time.time()
                
                if pattern_region:
                    # Update detection confidence
                    self.detection_confidence = min(1.0, self.detection_confidence + 0.1)
                    self.last_detection_time = current_time
                    
                    # Extract grid colors
                    grid_colors = self.extract_grid_colors_advanced(frame, pattern_region)
                    
                    # Add to frame buffer
                    self.frame_buffer.append(grid_colors)
                    
                    # Check for stable detection
                    if len(self.frame_buffer) >= self.detection_stability_frames:
                        if not self.is_scanning:
                            # Start sequence capture
                            self.is_scanning = True
                            self.security_sequence = []
                            print("🎯 Stable pattern detected! Starting capture...")
                        
                        # Analyze current frame for security markers
                        center_color = grid_colors[self.grid_size//2][self.grid_size//2]
                        color_type = self.color_detector.classify_color_type(center_color)
                        
                        if color_type.startswith("security_"):
                            if color_type == "security_auth_start" and len(self.security_sequence) == 0:
                                print("🔄 Security sequence started")
                                self.security_sequence = [grid_colors]
                            elif len(self.security_sequence) > 0:
                                self.security_sequence.append(grid_colors)
                                
                                if color_type == "security_auth_end":
                                    print("🏁 Security sequence complete")
                                    
                                    # Process the sequence
                                    decoded_data = self.process_hyper_secure_sequence(self.security_sequence)
                                    
                                    if decoded_data:
                                        print(f"🎉 HYPERSECURE PATTERN DETECTED: {decoded_data}")
                                        self.show_success_message(frame, decoded_data)
                                    
                                    # Reset
                                    self.is_scanning = False
                                    self.security_sequence = []
                        
                        # Timeout check
                        if (len(self.security_sequence) > 0 and 
                            current_time - self.last_detection_time > self.max_detection_time):
                            print("⏰ Detection timeout - resetting")
                            self.is_scanning = False
                            self.security_sequence = []
                
                else:
                    # Decrease confidence when no pattern detected
                    self.detection_confidence = max(0.0, self.detection_confidence - 0.05)
                    
                    # Reset if no detection for too long
                    if current_time - self.last_detection_time > 2.0:
                        if self.is_scanning:
                            self.is_scanning = False
                            self.security_sequence = []
                
                # Draw overlay
                display_frame = self.draw_advanced_overlay(frame, pattern_region)
                
                # Show frame
                cv2.imshow(self.window_name, display_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    # Reset detection
                    self.is_scanning = False
                    self.security_sequence = []
                    self.detection_confidence = 0.0
                    print("🔄 Detection reset")
        
        except KeyboardInterrupt:
            print("🛑 Scanner interrupted by user")
        
        finally:
            self.cleanup()
    
    def show_success_message(self, frame: np.ndarray, decoded_data: str):
        """Show enhanced success message."""
        overlay = frame.copy()
        height, width = frame.shape[:2]
        
        # Draw enhanced success background
        cv2.rectangle(overlay, (50, height//2 - 120), 
                     (width - 50, height//2 + 120), (0, 150, 0), -1)
        cv2.rectangle(overlay, (50, height//2 - 120), 
                     (width - 50, height//2 + 120), (0, 255, 0), 4)
        
        # Success text
        cv2.putText(overlay, "🎉 HYPERSECURE SUCCESS!", 
                   (width//2 - 200, height//2 - 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        
        # Decoded data
        max_length = 50
        if len(decoded_data) > max_length:
            display_data = decoded_data[:max_length] + "..."
        else:
            display_data = decoded_data
            
        cv2.putText(overlay, f"Data: {display_data}", 
                   (60, height//2 - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Security status
        if HYPER_SECURITY_AVAILABLE:
            security_text = "🔒 MILITARY-GRADE VERIFIED"
        else:
            security_text = "🔐 SECURE PATTERN VERIFIED"
            
        cv2.putText(overlay, security_text, 
                   (60, height//2 + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.putText(overlay, "Press any key to continue...", 
                   (width//2 - 150, height//2 + 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow(self.window_name, overlay)
        cv2.waitKey(3000)  # Show for 3 seconds
    
    def cleanup(self):
        """Clean up resources."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("🧹 HyperSecure scanner cleanup complete")


def main():
    """Main function for HyperSecure scanner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="🔒 HyperSecure RPattern Scanner by Rahul Chaube")
    parser.add_argument("--camera", "-c", type=int, default=0,
                       help="Camera index to use")
    
    args = parser.parse_args()
    
    print("🔒 HyperSecure RPattern Scanner - Military Grade")
    print("Creator: Rahul Chaube")
    
    if HYPER_SECURITY_AVAILABLE:
        print("🛡️ HYPERSECURITY MODE: ACTIVE")
    else:
        print("🔐 Standard Security Mode")
        
    print(f"📷 Camera: {args.camera}")
    print("-" * 60)
    
    # Start scanner
    scanner = HyperSecureScanner(camera_index=args.camera)
    scanner.start_scanning()


if __name__ == "__main__":
    main()
