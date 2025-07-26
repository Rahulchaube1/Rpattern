# 📖 RPattern API Documentation

## 🚀 **Core API Reference**

### `rpattern_revolutionary.py` - Core Engine

#### **RPatternCore Class**

The main class for pattern creation and decoding.

```python
from src.rpattern_revolutionary import RPatternCore

core = RPatternCore()
```

**Methods:**

##### `encode_revolutionary_pattern(data: str, duration: int = 30, security_level: str = "HIGH") -> Dict[str, Any]`

Creates an encrypted, animated pattern.

**Parameters:**
- `data` (str): Data to encode (max 1024 characters)
- `duration` (int): Pattern lifetime in seconds (10-300)
- `security_level` (str): "LOW", "MEDIUM", "HIGH", or "MILITARY"

**Returns:**
- Dictionary with pattern data including frames, metadata, and encryption info

**Example:**
```python
pattern = core.encode_revolutionary_pattern(
    data="Hello World!",
    duration=60,
    security_level="MILITARY"
)
```

##### `decode_revolutionary_pattern(frames: List[List[List[int]]]) -> str`

Decodes an encrypted pattern back to original data.

**Parameters:**
- `frames` (List): List of 4x4 color frame arrays

**Returns:**
- Original decoded string

**Raises:**
- `SecurityError`: If pattern is expired or invalid
- `ValueError`: If frames are malformed

---

#### **Utility Functions**

##### `create_revolutionary_pattern(data: str, duration: int = 30, security_level: str = "HIGH") -> Dict[str, Any]`

Quick pattern creation function.

```python
from src.rpattern_revolutionary import create_revolutionary_pattern

pattern = create_revolutionary_pattern("My secret data")
```

##### `validate_pattern(pattern: Dict[str, Any]) -> bool`

Validates pattern structure and security.

```python
is_valid = validate_pattern(pattern)
```

---

### `pattern_display.py` - Visual Display

#### **RPatternAnimator Class**

Handles pattern animation and display.

```python
from src.pattern_display import RPatternAnimator

animator = RPatternAnimator()
```

**Methods:**

##### `play_pattern(pattern: Dict[str, Any], fps: int = 15) -> None`

Displays animated pattern in a window.

**Parameters:**
- `pattern` (dict): Pattern data from core engine
- `fps` (int): Animation frame rate (5-30)

**Example:**
```python
animator.play_pattern(pattern, fps=20)
```

##### `export_gif(pattern: Dict[str, Any], filename: str, fps: int = 10) -> bool`

Exports pattern as animated GIF.

**Parameters:**
- `pattern` (dict): Pattern data
- `filename` (str): Output filename
- `fps` (int): GIF frame rate

**Returns:**
- True if successful, False otherwise

---

### `revolutionary_scanner.py` - AI Scanner

#### **RPatternScanner Class**

AI-powered pattern detection and decoding.

```python
from src.revolutionary_scanner import RPatternScanner

scanner = RPatternScanner()
```

**Methods:**

##### `scan_from_camera(camera_id: int = 0, timeout: int = 30) -> str`

Scans pattern from camera feed.

**Parameters:**
- `camera_id` (int): Camera device ID
- `timeout` (int): Scan timeout in seconds

**Returns:**
- Decoded data string

**Example:**
```python
decoded_data = scanner.scan_from_camera(camera_id=0, timeout=60)
```

##### `scan_from_image(image_path: str) -> str`

Scans pattern from static image.

**Parameters:**
- `image_path` (str): Path to image file

**Returns:**
- Decoded data string

##### `detect_pattern_region(frame: np.ndarray) -> Tuple[int, int, int, int]`

Detects pattern location in frame.

**Returns:**
- Tuple of (x, y, width, height) coordinates

---

### `rpattern_app.py` - GUI Application

#### **RPatternApp Class**

Complete GUI application interface.

```python
from src.rpattern_app import RPatternApp

app = RPatternApp()
app.run()
```

**Features:**
- Pattern generation interface
- Real-time camera scanning
- Pattern gallery management
- Settings configuration

---

## 🛡️ **Security API**

### **Encryption Functions**

```python
from src.rpattern_revolutionary import SecurityManager

security = SecurityManager()
```

#### `encrypt_data(data: str, key: bytes) -> bytes`

Encrypts data with AES-256-GCM.

#### `decrypt_data(encrypted_data: bytes, key: bytes) -> str`

Decrypts AES-256-GCM encrypted data.

#### `generate_secure_key() -> bytes`

Generates cryptographically secure 256-bit key.

---

## 🎨 **Color System**

### **Color Encoding**

RPattern uses 8-color encoding system:

```python
COLOR_MAP = {
    0: (255, 0, 0),    # Red
    1: (0, 255, 0),    # Green  
    2: (0, 0, 255),    # Blue
    3: (255, 255, 0),  # Yellow
    4: (255, 0, 255),  # Magenta
    5: (0, 255, 255),  # Cyan
    6: (255, 165, 0),  # Orange
    7: (128, 0, 128),  # Purple
}
```

Each color represents 3 bits of data (2³ = 8 colors).

---

## ⚡ **Performance Guidelines**

### **Optimization Tips**

1. **Pattern Generation:**
   - Use appropriate security levels
   - Limit data size for faster encoding
   - Cache frequently used patterns

2. **Display Performance:**
   - Adjust FPS based on device capability
   - Use lower resolution for mobile devices
   - Enable hardware acceleration when available

3. **Scanning Optimization:**
   - Use good lighting conditions
   - Maintain steady camera position
   - Set appropriate timeout values

---

## 🧪 **Testing API**

### **Unit Testing**

```python
import unittest
from src.rpattern_revolutionary import RPatternCore

class TestRPatternCore(unittest.TestCase):
    def setUp(self):
        self.core = RPatternCore()
    
    def test_pattern_creation(self):
        pattern = self.core.encode_revolutionary_pattern("test")
        self.assertIsNotNone(pattern)
        self.assertIn('frames', pattern)
```

### **Performance Testing**

```python
import time
from src.rpattern_revolutionary import create_revolutionary_pattern

def benchmark_pattern_creation():
    start_time = time.time()
    for i in range(100):
        pattern = create_revolutionary_pattern(f"test data {i}")
    end_time = time.time()
    
    print(f"Created 100 patterns in {end_time - start_time:.2f} seconds")
```

---

## 🔧 **Configuration**

### **Environment Variables**

```bash
# Security settings
RPATTERN_DEFAULT_SECURITY=MILITARY
RPATTERN_MAX_DURATION=300

# Display settings  
RPATTERN_DEFAULT_FPS=15
RPATTERN_WINDOW_SIZE=800x600

# Scanner settings
RPATTERN_SCAN_TIMEOUT=30
RPATTERN_DETECTION_THRESHOLD=0.8
```

### **Config File Example**

```json
{
    "security": {
        "default_level": "MILITARY",
        "max_duration": 300,
        "auto_expire": true
    },
    "display": {
        "default_fps": 15,
        "window_size": [800, 600],
        "fullscreen": false
    },
    "scanner": {
        "timeout": 30,
        "detection_threshold": 0.8,
        "camera_id": 0
    }
}
```

---

## 🚨 **Error Handling**

### **Common Exceptions**

```python
from src.rpattern_revolutionary import SecurityError, PatternError

try:
    pattern = create_revolutionary_pattern("data")
except SecurityError as e:
    print(f"Security error: {e}")
except PatternError as e:
    print(f"Pattern error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### **Error Codes**

- `SEC001`: Encryption failure
- `SEC002`: Pattern expired
- `SEC003`: Invalid security level
- `PAT001`: Malformed pattern data
- `PAT002`: Pattern too large
- `SCAN001`: No pattern detected
- `SCAN002`: Camera not available

---

## 📞 **Support**

For API questions and support:
- 📧 Email: api-support@rahulchaube.dev
- 📚 GitHub Issues: [Report API issues](https://github.com/Rahulchaube1/Rpattern/issues)
- 💬 Discussions: [API discussions](https://github.com/Rahulchaube1/Rpattern/discussions)

---

*API Documentation v1.0 - Created by Rahul Chaube 💎*
