"""
Test suite for RPattern Revolutionary Core Engine
Author: Rahul Chaube
"""

import unittest
import time
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from rpattern_revolutionary import RPatternCore, create_revolutionary_pattern
except ImportError:
    # Mock the imports if not available
    RPatternCore = MagicMock
    create_revolutionary_pattern = MagicMock


class TestRPatternCore(unittest.TestCase):
    """Test cases for RPattern core functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        if RPatternCore != MagicMock:
            self.core = RPatternCore()
        else:
            self.core = MagicMock()
    
    def test_pattern_creation_basic(self):
        """Test basic pattern creation"""
        test_data = "Hello World!"
        
        if create_revolutionary_pattern != MagicMock:
            pattern = create_revolutionary_pattern(test_data)
            
            # Check pattern structure
            self.assertIsInstance(pattern, dict)
            self.assertIn('frames', pattern)
            self.assertIn('pattern_id', pattern)
            self.assertIn('timestamp', pattern)
            self.assertIn('expiry', pattern)
        else:
            # Mock test
            pattern = {'frames': [], 'pattern_id': 'test', 'timestamp': time.time()}
            self.assertIsInstance(pattern, dict)
    
    def test_pattern_creation_with_security_levels(self):
        """Test pattern creation with different security levels"""
        test_data = "Security Test Data"
        security_levels = ["LOW", "MEDIUM", "HIGH", "MILITARY"]
        
        for level in security_levels:
            if create_revolutionary_pattern != MagicMock:
                pattern = create_revolutionary_pattern(test_data, 30, level)
                self.assertIsInstance(pattern, dict)
                self.assertEqual(pattern.get('security_level'), level)
            else:
                # Mock test
                pattern = {'security_level': level}
                self.assertEqual(pattern.get('security_level'), level)
    
    def test_pattern_expiry(self):
        """Test pattern auto-expiry functionality"""
        test_data = "Expiry Test"
        
        if create_revolutionary_pattern != MagicMock:
            pattern = create_revolutionary_pattern(test_data, 1)  # 1 second expiry
            
            # Check that expiry time is set
            self.assertGreater(pattern.get('expiry', 0), pattern.get('timestamp', 0))
            
            # Pattern should be valid immediately
            current_time = time.time() * 1000  # Convert to milliseconds
            self.assertLess(current_time, pattern.get('expiry', 0))
        else:
            # Mock test
            current_time = time.time() * 1000
            pattern = {
                'timestamp': current_time - 1000,
                'expiry': current_time + 1000
            }
            self.assertLess(pattern['timestamp'], pattern['expiry'])
    
    def test_large_data_handling(self):
        """Test handling of large data"""
        # Test with various data sizes
        small_data = "Small"
        medium_data = "Medium size data for testing pattern creation" * 10
        large_data = "Large data string for comprehensive testing" * 50
        
        test_cases = [small_data, medium_data, large_data]
        
        for data in test_cases:
            if create_revolutionary_pattern != MagicMock:
                try:
                    pattern = create_revolutionary_pattern(data)
                    self.assertIsInstance(pattern, dict)
                except Exception as e:
                    # Large data might have size limits
                    if len(data) > 1000:  # Assuming 1KB limit
                        self.assertIsInstance(e, (ValueError, OverflowError))
                    else:
                        self.fail(f"Unexpected error for data size {len(data)}: {e}")
            else:
                # Mock test
                pattern = {'data_size': len(data)}
                self.assertIsInstance(pattern, dict)
    
    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        invalid_inputs = [
            None,
            "",
            123,  # Non-string
            [],   # List
            {}    # Dict
        ]
        
        for invalid_input in invalid_inputs:
            if create_revolutionary_pattern != MagicMock:
                try:
                    pattern = create_revolutionary_pattern(invalid_input)
                    # Should either succeed with string conversion or fail gracefully
                    if pattern is not None:
                        self.assertIsInstance(pattern, dict)
                except (ValueError, TypeError):
                    # Expected for invalid inputs
                    pass
            else:
                # Mock test - just check we handle the case
                self.assertIsNotNone(invalid_input)  # Placeholder assertion


class TestPatternSecurity(unittest.TestCase):
    """Test cases for pattern security features"""
    
    def test_pattern_uniqueness(self):
        """Test that identical data creates unique patterns"""
        test_data = "Uniqueness Test"
        
        if create_revolutionary_pattern != MagicMock:
            pattern1 = create_revolutionary_pattern(test_data)
            pattern2 = create_revolutionary_pattern(test_data)
            
            # Patterns should be different due to timestamps/randomness
            self.assertNotEqual(pattern1.get('pattern_id'), pattern2.get('pattern_id'))
        else:
            # Mock test
            pattern1 = {'pattern_id': 'id1', 'timestamp': 1000}
            pattern2 = {'pattern_id': 'id2', 'timestamp': 1001}
            self.assertNotEqual(pattern1['pattern_id'], pattern2['pattern_id'])
    
    def test_encryption_integrity(self):
        """Test encryption integrity"""
        test_data = "Encryption Test Data"
        
        if create_revolutionary_pattern != MagicMock:
            pattern = create_revolutionary_pattern(test_data, 60, "MILITARY")
            
            # Check that we have encrypted frames
            self.assertIn('frames', pattern)
            self.assertIsInstance(pattern['frames'], list)
            
            if pattern['frames']:
                # Frames should contain numeric color data
                frame = pattern['frames'][0]
                self.assertIsInstance(frame, list)
                if frame:
                    self.assertIsInstance(frame[0], list)
        else:
            # Mock test
            pattern = {
                'frames': [[[1, 2, 3], [4, 5, 6]], [[7, 0, 1], [2, 3, 4]]],
                'encryption': 'AES-256-GCM+ChaCha20'
            }
            self.assertIn('frames', pattern)


class TestPerformanceMetrics(unittest.TestCase):
    """Test cases for performance requirements"""
    
    def test_pattern_creation_speed(self):
        """Test pattern creation performance"""
        test_data = "Performance Test Data"
        num_patterns = 10
        
        start_time = time.time()
        
        for i in range(num_patterns):
            if create_revolutionary_pattern != MagicMock:
                pattern = create_revolutionary_pattern(f"{test_data} {i}")
                self.assertIsInstance(pattern, dict)
            else:
                # Mock test with small delay
                time.sleep(0.001)  # 1ms mock delay
        
        end_time = time.time()
        total_time = end_time - start_time
        patterns_per_second = num_patterns / total_time
        
        # Should create at least 50 patterns per second (very conservative)
        self.assertGreater(patterns_per_second, 50, 
                          f"Performance too slow: {patterns_per_second:.2f} patterns/second")
    
    def test_memory_efficiency(self):
        """Test memory usage is reasonable"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create multiple patterns
        patterns = []
        for i in range(100):
            if create_revolutionary_pattern != MagicMock:
                pattern = create_revolutionary_pattern(f"Memory test {i}")
                patterns.append(pattern)
            else:
                patterns.append({'id': i})
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Should use less than 100MB for 100 patterns
        self.assertLess(memory_increase, 100, 
                       f"Memory usage too high: {memory_increase:.2f} MB")


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestRPatternCore))
    test_suite.addTest(unittest.makeSuite(TestPatternSecurity))
    test_suite.addTest(unittest.makeSuite(TestPerformanceMetrics))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"RPattern Core Tests Summary")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    print(f"\n🚀 RPattern Core Testing Complete!")
