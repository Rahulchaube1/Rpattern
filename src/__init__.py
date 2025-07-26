"""
RPattern Revolutionary System
The Future of Visual Security Patterns

Created by Rahul Chaube 💎
Portfolio: https://rahulchaube.dev
GitHub: https://github.com/Rahulchaube1/Rpattern

A revolutionary visual pattern system that completely replaces QR codes with:
- Military-grade encryption (AES-256 + ChaCha20)
- Dynamic animated color patterns
- AI-powered computer vision scanning
- Auto-expiring security mechanisms
- Quantum-resistant cryptography
"""

__version__ = "1.0.0"
__author__ = "Rahul Chaube"
__email__ = "rahul@rahulchaube.dev"
__license__ = "MIT"
__copyright__ = "Copyright 2024 Rahul Chaube"

# Import main components for easy access
try:
    from .rpattern_revolutionary import (
        RPatternCore,
        create_revolutionary_pattern,
        SecurityManager
    )
    from .pattern_display import RPatternAnimator
    from .revolutionary_scanner import RPatternScanner
    from .rpattern_app import RPatternApp
    
    __all__ = [
        'RPatternCore',
        'create_revolutionary_pattern', 
        'SecurityManager',
        'RPatternAnimator',
        'RPatternScanner',
        'RPatternApp',
        '__version__',
        '__author__',
        '__email__'
    ]
    
except ImportError:
    # If dependencies are not available, still allow version import
    __all__ = ['__version__', '__author__', '__email__']

# Package metadata
PACKAGE_INFO = {
    'name': 'rpattern-revolutionary',
    'version': __version__,
    'author': __author__,
    'email': __email__,
    'license': __license__,
    'description': 'Revolutionary Visual Pattern System - The Future of QR Codes',
    'url': 'https://github.com/Rahulchaube1/Rpattern',
    'keywords': ['qr-code', 'visual-patterns', 'encryption', 'security'],
    'status': 'Production/Stable'
}

def get_version():
    """Get package version"""
    return __version__

def get_info():
    """Get package information"""
    return PACKAGE_INFO.copy()

def print_banner():
    """Print RPattern banner"""
    banner = f"""
🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥
                    
                🚀 RPATTERN REVOLUTIONARY SYSTEM 🚀
                      Version {__version__}
                     Created by {__author__} 💎
                    
🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥🚀🔥

🛡️ MILITARY-GRADE SECURITY | 🎨 ANIMATED PATTERNS | 🤖 AI-POWERED SCANNING
⚡ LIGHTNING FAST | 🔮 QUANTUM-RESISTANT | 💎 IMPOSSIBLE TO FORGE

The Future of Visual Security is HERE!
"""
    print(banner)

# Check Python version compatibility
import sys
if sys.version_info < (3, 10):
    raise RuntimeError(
        f"RPattern requires Python 3.10 or higher. "
        f"Current version: {sys.version_info.major}.{sys.version_info.minor}"
    )
