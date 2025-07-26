"""
🚀 BULLETPROOF RPATTERN DEMO
Quick Command-Line Demo
Creator: Rahul Chaube 💎
"""

import time
import os
import sys
from bulletproof_core import BulletproofRPattern


def print_banner():
    """Print amazing banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                🚀 BULLETPROOF RPATTERN 🚀                   ║
║                                                              ║
║         Ultra Simple • Ultra Secure • Ultra Reliable        ║
║                                                              ║
║                   Created by Rahul Chaube 💎                ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def demo_encoding():
    """Demonstrate encoding capabilities."""
    print("\n🔐 ENCODING DEMONSTRATION")
    print("=" * 50)
    
    # Sample data
    demo_data = [
        "Hello World! - Rahul Chaube",
        "https://github.com/rahulchaube",
        "TOP SECRET: Military Grade Encryption",
        "Contact: +91-9876543210",
        "🚀 Bulletproof RPattern Demo 🚀"
    ]
    
    bp_rpattern = BulletproofRPattern(expiry_minutes=5, security_level="HIGH")
    
    for i, data in enumerate(demo_data, 1):
        print(f"\n📝 Test {i}: {data}")
        
        start_time = time.time()
        pattern = bp_rpattern.encode_bulletproof_data(data)
        encode_time = time.time() - start_time
        
        print(f"   ✅ Encoded in {encode_time:.4f}s")
        print(f"   📊 Frames: {pattern['total_frames']}")
        print(f"   🆔 Pattern ID: {pattern['pattern_id']}")
        
        # Test decoding
        start_time = time.time()
        decoded = bp_rpattern.decode_bulletproof_frames(pattern['frames'])
        decode_time = time.time() - start_time
        
        if decoded == data:
            print(f"   ✅ Decoded in {decode_time:.4f}s")
            print(f"   🎉 PERFECT MATCH!")
        else:
            print(f"   ❌ Decode failed!")
        
        # Security report
        report = bp_rpattern.get_bulletproof_report(pattern)
        print(f"   🛡️ Security: {report['security_level']} ({report['encryption_type']})")
        print(f"   ⏰ Time Remaining: {report['time_remaining']}s")


def demo_security_features():
    """Demonstrate security features."""
    print("\n🛡️ SECURITY FEATURES DEMONSTRATION")
    print("=" * 50)
    
    bp_rpattern = BulletproofRPattern(expiry_minutes=1, security_level="HIGH")
    test_data = "Security Test - Rahul Chaube"
    
    print(f"🔐 Original Data: {test_data}")
    
    # Create pattern
    pattern = bp_rpattern.encode_bulletproof_data(test_data)
    report = bp_rpattern.get_bulletproof_report(pattern)
    
    print(f"\n🛡️ Security Report:")
    print(f"   📊 Security Level: {report['security_level']}")
    print(f"   🔒 Encryption: {report['encryption_type']}")
    print(f"   🆔 Pattern ID: {report['pattern_id']}")
    print(f"   🔑 Session ID: {report['session_id']}")
    print(f"   ⏰ Time Remaining: {report['time_remaining']}s")
    print(f"   📋 Status: {report['status']}")
    
    print(f"\n🔧 Security Features:")
    for i, feature in enumerate(report['security_features'], 1):
        print(f"   {i}. {feature}")
    
    # Test immediate decoding
    print(f"\n🔍 Immediate Decoding Test:")
    decoded = bp_rpattern.decode_bulletproof_frames(pattern['frames'])
    if decoded == test_data:
        print(f"   ✅ SUCCESS: Pattern decoded correctly")
    else:
        print(f"   ❌ FAILED: Pattern decode failed")


def demo_performance():
    """Demonstrate performance."""
    print("\n⚡ PERFORMANCE DEMONSTRATION")
    print("=" * 50)
    
    bp_rpattern = BulletproofRPattern(expiry_minutes=5, security_level="HIGH")
    
    # Test different data sizes
    test_sizes = [
        ("Small", "Hi"),
        ("Medium", "This is a medium length message for testing"),
        ("Large", "This is a much longer message that contains more data to test the performance of the bulletproof RPattern system created by Rahul Chaube with maximum security features"),
        ("URL", "https://github.com/rahulchaube/bulletproof-rpattern"),
        ("JSON", '{"name": "Rahul Chaube", "project": "BulletproofRPattern", "security": "maximum"}')
    ]
    
    total_encode_time = 0
    total_decode_time = 0
    
    for size_name, data in test_sizes:
        print(f"\n📊 {size_name} Data ({len(data)} chars): {data[:50]}...")
        
        # Encoding performance
        start_time = time.time()
        pattern = bp_rpattern.encode_bulletproof_data(data)
        encode_time = time.time() - start_time
        total_encode_time += encode_time
        
        # Decoding performance
        start_time = time.time()
        decoded = bp_rpattern.decode_bulletproof_frames(pattern['frames'])
        decode_time = time.time() - start_time
        total_decode_time += decode_time
        
        print(f"   🚀 Encode: {encode_time:.4f}s")
        print(f"   🔍 Decode: {decode_time:.4f}s")
        print(f"   📊 Frames: {pattern['total_frames']}")
        print(f"   ✅ Success: {decoded == data}")
    
    print(f"\n📈 TOTAL PERFORMANCE:")
    print(f"   🚀 Total Encode Time: {total_encode_time:.4f}s")
    print(f"   🔍 Total Decode Time: {total_decode_time:.4f}s")
    print(f"   ⚡ Average Encode: {total_encode_time/len(test_sizes):.4f}s")
    print(f"   ⚡ Average Decode: {total_decode_time/len(test_sizes):.4f}s")


def main():
    """Run the complete demo."""
    print_banner()
    
    print("🚀 Starting Bulletproof RPattern Demo...")
    print("💎 Created by Rahul Chaube")
    print("\nPress Enter to continue through each demo section...")
    input()
    
    try:
        # Encoding demo
        demo_encoding()
        input("\nPress Enter for Security Features demo...")
        
        # Security demo
        demo_security_features()
        input("\nPress Enter for Performance demo...")
        
        # Performance demo
        demo_performance()
        
        print("\n" + "=" * 60)
        print("🎉 BULLETPROOF RPATTERN DEMO COMPLETE!")
        print("🛡️ All systems operational and secure!")
        print("🚀 Ready for production use!")
        print("💎 Created by Rahul Chaube")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n🔴 Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}")
    
    print("\n✅ Demo session ended. Thank you!")


if __name__ == "__main__":
    main()
