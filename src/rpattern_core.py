"""
RPattern Core - Encoding and Decoding Logic
Creator: Rahul Chaube 🚀
"""

import time
import hashlib
import json
from typing import List, Tuple, Optional, Dict, Any
from crypto_utils import encrypt_data, decrypt_data


class RPattern:
    """Core RPattern class for encoding and decoding visual patterns."""
    
    # Pattern configuration
    FRAME_DURATION = 0.5  # seconds per frame
    PATTERN_SIZE = 3  # 3x3 grid for simplicity
    MAX_FRAMES = 10  # Maximum frames in a pattern
    
    # Color mapping for encoding (RGB values)
    COLOR_MAP = {
        '00': (255, 0, 0),      # Red
        '01': (0, 255, 0),      # Green  
        '10': (0, 0, 255),      # Blue
        '11': (255, 255, 0),    # Yellow
    }
    
    # Reverse mapping for decoding
    REVERSE_COLOR_MAP = {v: k for k, v in COLOR_MAP.items()}
    
    def __init__(self, expiry_minutes: int = 5):
        """Initialize RPattern with expiry time."""
        self.expiry_minutes = expiry_minutes
        
    def encode_data(self, data: str, use_encryption: bool = True) -> Dict[str, Any]:
        """
        Encode data into RPattern format.
        
        Args:
            data: String data to encode (URL, ID, etc.)
            use_encryption: Whether to encrypt the data
            
        Returns:
            Dictionary containing pattern data and metadata
        """
        # Create timestamp for expiry
        timestamp = int(time.time())
        expiry_time = timestamp + (self.expiry_minutes * 60)
        
        # Prepare payload
        payload = {
            'data': data,
            'timestamp': timestamp,
            'expiry': expiry_time,
            'creator': 'RPattern by Rahul Chaube'
        }
        
        # Convert to JSON
        json_data = json.dumps(payload)
        
        # Encrypt if requested
        if use_encryption:
            encoded_data = encrypt_data(json_data)
        else:
            encoded_data = json_data.encode('utf-8')
            
        # Convert to binary string
        binary_data = ''.join(format(byte, '08b') for byte in encoded_data)
        
        # Add padding to ensure even number of bits (for 2-bit color encoding)
        if len(binary_data) % 2 != 0:
            binary_data += '0'
            
        # Generate color frames
        frames = self._binary_to_frames(binary_data)
        
        # Add error correction and synchronization frames
        frames = self._add_error_correction(frames)
        
        return {
            'frames': frames,
            'frame_duration': self.FRAME_DURATION,
            'total_frames': len(frames),
            'timestamp': timestamp,
            'expiry': expiry_time,
            'encrypted': use_encryption
        }
    
    def decode_frames(self, color_frames: List[List[List[Tuple[int, int, int]]]]) -> Optional[str]:
        """
        Decode color frames back to original data.
        
        Args:
            color_frames: List of color frames captured from camera
            
        Returns:
            Decoded data string or None if decoding fails
        """
        try:
            # Remove error correction frames
            cleaned_frames = self._remove_error_correction(color_frames)
            
            # Convert frames back to binary
            binary_data = self._frames_to_binary(cleaned_frames)
            
            # Convert binary to bytes
            if len(binary_data) % 8 != 0:
                # Remove padding
                binary_data = binary_data[:-(len(binary_data) % 8)]
                
            byte_data = bytes(int(binary_data[i:i+8], 2) 
                            for i in range(0, len(binary_data), 8))
            
            # Try to decrypt (assume encrypted first)
            try:
                json_str = decrypt_data(byte_data)
            except:
                # If decryption fails, try as plain text
                json_str = byte_data.decode('utf-8')
                
            # Parse JSON
            payload = json.loads(json_str)
            
            # Check expiry
            current_time = int(time.time())
            if current_time > payload['expiry']:
                raise ValueError("RPattern has expired")
                
            return payload['data']
            
        except Exception as e:
            print(f"Decoding error: {e}")
            return None
    
    def _binary_to_frames(self, binary_data: str) -> List[List[List[Tuple[int, int, int]]]]:
        """Convert binary data to color frames."""
        frames = []
        
        # Process binary data in chunks of 2 bits
        for i in range(0, len(binary_data), 2):
            if i + 1 < len(binary_data):
                bit_pair = binary_data[i:i+2]
            else:
                bit_pair = binary_data[i] + '0'  # Pad with 0
                
            color = self.COLOR_MAP.get(bit_pair, (255, 255, 255))  # White as fallback
            
            # Create a frame (3x3 grid with the same color)
            frame = [[color for _ in range(self.PATTERN_SIZE)] 
                    for _ in range(self.PATTERN_SIZE)]
            frames.append(frame)
            
        return frames
    
    def _frames_to_binary(self, frames: List[List[List[Tuple[int, int, int]]]]) -> str:
        """Convert color frames back to binary data."""
        binary_data = ""
        
        for frame in frames:
            # Get the dominant color from the center of the frame
            center_color = frame[1][1]  # Middle cell of 3x3 grid
            
            # Find closest color match
            closest_color = min(self.COLOR_MAP.values(), 
                              key=lambda c: sum((a-b)**2 for a, b in zip(c, center_color)))
            
            # Get the corresponding bit pair
            bit_pair = self.REVERSE_COLOR_MAP.get(closest_color, '00')
            binary_data += bit_pair
            
        return binary_data
    
    def _add_error_correction(self, frames: List[List[List[Tuple[int, int, int]]]]) -> List[List[List[Tuple[int, int, int]]]]:
        """Add error correction and synchronization frames."""
        corrected_frames = []
        
        # Add start synchronization frame (all white)
        sync_frame = [[(255, 255, 255) for _ in range(self.PATTERN_SIZE)] 
                     for _ in range(self.PATTERN_SIZE)]
        corrected_frames.append(sync_frame)
        
        # Add data frames
        corrected_frames.extend(frames)
        
        # Add end synchronization frame (all black)
        end_frame = [[(0, 0, 0) for _ in range(self.PATTERN_SIZE)] 
                    for _ in range(self.PATTERN_SIZE)]
        corrected_frames.append(end_frame)
        
        return corrected_frames
    
    def _remove_error_correction(self, frames: List[List[List[Tuple[int, int, int]]]]) -> List[List[List[Tuple[int, int, int]]]]:
        """Remove error correction and synchronization frames."""
        if len(frames) < 2:
            return frames
            
        # Remove first (start sync) and last (end sync) frames
        return frames[1:-1]
    
    def is_expired(self, pattern_data: Dict[str, Any]) -> bool:
        """Check if a pattern has expired."""
        current_time = int(time.time())
        return current_time > pattern_data.get('expiry', 0)
    
    def get_pattern_info(self, pattern_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get human-readable pattern information."""
        expiry_time = pattern_data.get('expiry', 0)
        current_time = int(time.time())
        time_remaining = max(0, expiry_time - current_time)
        
        return {
            'total_frames': pattern_data.get('total_frames', 0),
            'frame_duration': pattern_data.get('frame_duration', 0),
            'encrypted': pattern_data.get('encrypted', False),
            'time_remaining_seconds': time_remaining,
            'is_expired': time_remaining == 0,
            'created_at': time.ctime(pattern_data.get('timestamp', 0))
        }


def create_test_pattern(data: str = "https://rahulcodes.in") -> Dict[str, Any]:
    """Create a test RPattern for the given data."""
    rpattern = RPattern(expiry_minutes=5)
    return rpattern.encode_data(data, use_encryption=True)


if __name__ == "__main__":
    # Test the RPattern encoding/decoding
    test_data = "https://rahulcodes.in"
    
    print("🚀 RPattern Core Test")
    print(f"Original data: {test_data}")
    
    # Create pattern
    rpattern = RPattern(expiry_minutes=5)
    pattern = rpattern.encode_data(test_data)
    
    print(f"Generated pattern with {pattern['total_frames']} frames")
    print(f"Pattern info: {rpattern.get_pattern_info(pattern)}")
    
    # Test decoding (simulate captured frames)
    decoded_data = rpattern.decode_frames(pattern['frames'])
    print(f"Decoded data: {decoded_data}")
    
    if decoded_data == test_data:
        print("✅ Encoding/Decoding test passed!")
    else:
        print("❌ Encoding/Decoding test failed!")
