"""
RPattern Quick Demo
Creator: Rahul Chaube 🚀

Quick demonstration of RPattern functionality
"""

import time
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rpattern_core import RPattern


def demo_rpattern():
    """Demonstrate RPattern encoding and decoding."""
    
    print("🚀 RPattern Quick Demo")
    print("=" * 50)
    print("Creator: Rahul Chaube")
    print()
    
    # Test data
    test_cases = [
        "https://rahulcodes.in",
        "RPattern Demo by Rahul",
        "SECRET_CODE_12345",
        "Payment ID: TXN_001_SECURE"
    ]
    
    for i, data in enumerate(test_cases, 1):
        print(f"📝 Test Case {i}: {data}")
        
        # Create RPattern
        rpattern = RPattern(expiry_minutes=5)
        
        # Encode with encryption
        print("🔐 Encoding with AES encryption...")
        start_time = time.time()
        pattern = rpattern.encode_data(data, use_encryption=True)
        encode_time = time.time() - start_time
        
        # Show pattern info
        info = rpattern.get_pattern_info(pattern)
        print(f"   ✅ Generated {info['total_frames']} frames in {encode_time:.3f}s")
        print(f"   ⏱️  Animation duration: {info['total_frames'] * info['frame_duration']:.1f}s")
        print(f"   🔒 Encrypted: {info['encrypted']}")
        
        # Decode pattern
        print("🔍 Decoding pattern...")
        start_time = time.time()
        decoded_data = rpattern.decode_frames(pattern['frames'])
        decode_time = time.time() - start_time
        
        if decoded_data == data:
            print(f"   ✅ Successfully decoded in {decode_time:.3f}s")
            print(f"   📤 Original: {data}")
            print(f"   📥 Decoded:  {decoded_data}")
        else:
            print(f"   ❌ Decoding failed!")
            
        print()
    
    print("🎯 Performance Summary:")
    print("• Encoding: ~0.1-0.2 seconds per pattern")
    print("• Decoding: ~0.001-0.01 seconds per pattern") 
    print("• Frame rate: 2 FPS (0.5s per frame)")
    print("• Security: AES-256 encryption with time expiry")
    print()
    
    print("🌟 RPattern Features:")
    print("• Dynamic color animations (cooler than QR codes!)")
    print("• Time-based expiry for security")
    print("• AES encryption for sensitive data")
    print("• Real-time camera scanning")
    print("• Collision-resistant patterns")
    print("• Futuristic visual appeal")
    print()
    
    print("🚀 Ready to revolutionize visual IDs!")
    print("Run 'python src/demo.py' for the full interactive demo.")


if __name__ == "__main__":
    demo_rpattern()
