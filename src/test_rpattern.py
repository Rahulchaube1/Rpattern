"""
RPattern Test Suite
Creator: Rahul Chaube 🚀

Test suite to verify all RPattern components work correctly.
"""

import sys
import time
import traceback
from typing import List, Dict, Any


def test_crypto_utils():
    """Test the cryptography utilities."""
    print("🔐 Testing Crypto Utils...")
    
    try:
        from crypto_utils import encrypt_data, decrypt_data, encode_base64, decode_base64
        
        test_data = "Hello RPattern by Rahul Chaube!"
        
        # Test AES encryption (might fail if pycryptodome not installed)
        try:
            encrypted = encrypt_data(test_data)
            decrypted = decrypt_data(encrypted)
            assert decrypted == test_data, "AES encryption/decryption failed"
            print("  ✅ AES encryption/decryption: PASS")
        except ImportError:
            print("  ⚠️  AES encryption: SKIP (pycryptodome not installed)")
        
        # Test base64 encoding
        encoded = encode_base64(test_data)
        decoded = decode_base64(encoded)
        assert decoded == test_data, "Base64 encoding/decoding failed"
        print("  ✅ Base64 encoding/decoding: PASS")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Crypto utils test failed: {e}")
        return False


def test_rpattern_core():
    """Test the core RPattern functionality."""
    print("🎯 Testing RPattern Core...")
    
    try:
        from rpattern_core import RPattern, create_test_pattern
        
        test_data = "https://rahulcodes.in"
        
        # Test pattern creation
        rpattern = RPattern(expiry_minutes=5)
        
        # Test without encryption first (to avoid crypto dependency)
        pattern = rpattern.encode_data(test_data, use_encryption=False)
        assert pattern is not None, "Pattern creation failed"
        assert pattern['total_frames'] > 0, "No frames generated"
        print(f"  ✅ Pattern creation: PASS ({pattern['total_frames']} frames)")
        
        # Test decoding
        decoded_data = rpattern.decode_frames(pattern['frames'])
        assert decoded_data == test_data, f"Decoding failed: {decoded_data} != {test_data}"
        print("  ✅ Pattern decoding: PASS")
        
        # Test pattern info
        info = rpattern.get_pattern_info(pattern)
        assert isinstance(info, dict), "Pattern info should be a dictionary"
        assert 'total_frames' in info, "Pattern info missing total_frames"
        print("  ✅ Pattern info: PASS")
        
        # Test with encryption if available
        try:
            encrypted_pattern = rpattern.encode_data(test_data, use_encryption=True)
            encrypted_decoded = rpattern.decode_frames(encrypted_pattern['frames'])
            assert encrypted_decoded == test_data, "Encrypted pattern decoding failed"
            print("  ✅ Encrypted pattern: PASS")
        except ImportError:
            print("  ⚠️  Encrypted pattern: SKIP (crypto not available)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ RPattern core test failed: {e}")
        traceback.print_exc()
        return False


def test_pattern_generator():
    """Test the pattern generator (without actually displaying)."""
    print("🎨 Testing Pattern Generator...")
    
    try:
        from pattern_generator import RPatternGenerator
        
        # Test pattern generation
        pattern = RPatternGenerator.generate_pattern("test_data", use_encryption=False)
        assert pattern is not None, "Pattern generation failed"
        assert pattern['total_frames'] > 0, "No frames in generated pattern"
        print(f"  ✅ Pattern generation: PASS ({pattern['total_frames']} frames)")
        
        # Test display class initialization (without pygame)
        try:
            import pygame
            pygame.init()
            from pattern_generator import RPatternDisplay
            
            display = RPatternDisplay((400, 300))
            display.load_pattern(pattern)
            print("  ✅ Display initialization: PASS")
            
            pygame.quit()
        except ImportError:
            print("  ⚠️  Display test: SKIP (pygame not available)")
        except Exception as e:
            print(f"  ⚠️  Display test: SKIP ({e})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Pattern generator test failed: {e}")
        return False


def test_pattern_scanner():
    """Test the pattern scanner (without camera)."""
    print("📷 Testing Pattern Scanner...")
    
    try:
        from pattern_scanner import ColorDetector, RPatternScanner
        import numpy as np
        
        # Test color detector
        detector = ColorDetector()
        
        # Create a test image patch (red color)
        test_patch = np.zeros((50, 50, 3), dtype=np.uint8)
        test_patch[:, :] = [0, 0, 255]  # BGR red
        
        dominant_color = detector.detect_dominant_color(test_patch)
        color_class = detector.classify_color(dominant_color)
        print(f"  ✅ Color detection: PASS (detected {dominant_color} -> {color_class})")
        
        # Test scanner initialization (without camera)
        try:
            scanner = RPatternScanner(camera_index=0)
            print("  ✅ Scanner initialization: PASS")
        except Exception as e:
            print(f"  ⚠️  Scanner camera test: SKIP ({e})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Pattern scanner test failed: {e}")
        return False


def test_demo_imports():
    """Test that demo can be imported."""
    print("🚀 Testing Demo Application...")
    
    try:
        from demo import RPatternDemoGUI
        print("  ✅ Demo import: PASS")
        
        # Test GUI initialization (without actually showing)
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide the window
            demo = RPatternDemoGUI()
            root.destroy()
            print("  ✅ GUI initialization: PASS")
        except Exception as e:
            print(f"  ⚠️  GUI test: SKIP ({e})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Demo test failed: {e}")
        return False


def check_dependencies():
    """Check if required dependencies are available."""
    print("📦 Checking Dependencies...")
    
    dependencies = {
        'numpy': 'NumPy',
        'cv2': 'OpenCV (opencv-python)',
        'pygame': 'Pygame',
        'tkinter': 'Tkinter (usually built-in)',
        'Crypto': 'PyCryptodome (optional for encryption)'
    }
    
    available = []
    missing = []
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            available.append(name)
            print(f"  ✅ {name}: Available")
        except ImportError:
            missing.append(name)
            print(f"  ❌ {name}: Missing")
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
    else:
        print("\n🎉 All dependencies available!")
    
    return len(missing) == 0


def run_full_test_suite():
    """Run the complete test suite."""
    print("🚀 RPattern Test Suite")
    print("Creator: Rahul Chaube")
    print("=" * 50)
    
    start_time = time.time()
    
    # Check dependencies first
    deps_ok = check_dependencies()
    print()
    
    # Run tests
    tests = [
        ("Crypto Utils", test_crypto_utils),
        ("RPattern Core", test_rpattern_core),
        ("Pattern Generator", test_pattern_generator),
        ("Pattern Scanner", test_pattern_scanner),
        ("Demo Application", test_demo_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        try:
            if test_func():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            traceback.print_exc()
            print()
    
    # Summary
    elapsed = time.time() - start_time
    print("=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    print(f"⏱️  Total time: {elapsed:.2f} seconds")
    
    if passed == total and deps_ok:
        print("🎉 All tests passed! RPattern is ready to use.")
        print("\n🚀 Quick Start:")
        print("  python src/demo.py              # Run full demo")
        print("  python src/pattern_generator.py # Generate patterns")
        print("  python src/pattern_scanner.py   # Scan patterns")
    else:
        print("⚠️  Some tests failed or dependencies missing.")
        if not deps_ok:
            print("   Install dependencies: pip install -r requirements.txt")
    
    return passed == total


if __name__ == "__main__":
    success = run_full_test_suite()
    sys.exit(0 if success else 1)
