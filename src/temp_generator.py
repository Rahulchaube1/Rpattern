
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    import pygame
    import time
    from bulletproof_core import BulletproofRPattern
    
    def run_bulletproof_generator():
        """Run the bulletproof pattern generator."""
        # Initialize
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("🚀 Bulletproof RPattern Generator")
        clock = pygame.time.Clock()
        
        # Create pattern
        bp_rpattern = BulletproofRPattern(expiry_minutes=3, security_level="HIGH")
        pattern_data = bp_rpattern.encode_bulletproof_data('Enter your data here...')
        
        frames = pattern_data['frames']
        frame_duration = pattern_data['frame_duration']
        
        print(f"🚀 Bulletproof Pattern Generated!")
        print(f"🛡️ Security Level: HIGH")
        print(f"📊 Total Frames: {len(frames)}")
        print(f"⏱️ Frame Duration: {frame_duration}s")
        print("📱 Use scanner to decode!")
        print("❌ Press ESC or close window to exit")
        
        running = True
        frame_index = 0
        last_time = time.time()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update frame
            current_time = time.time()
            if current_time - last_time >= frame_duration:
                frame_index = (frame_index + 1) % len(frames)
                last_time = current_time
            
            # Draw frame
            screen.fill((0, 0, 0))
            
            frame = frames[frame_index]
            cell_size = 600 // len(frame)
            
            for y, row in enumerate(frame):
                for x, color in enumerate(row):
                    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            
            # Display info
            font = pygame.font.Font(None, 24)
            info_text = f"Frame {frame_index + 1}/{len(frames)} | HIGH SECURITY"
            text_surface = font.render(info_text, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10))
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
    
    if __name__ == "__main__":
        run_bulletproof_generator()

except ImportError as e:
    print(f"Import error: {e}")
    print("Trying fallback display...")
    
    # Simple fallback
    import tkinter as tk
    
    root = tk.Tk()
    root.title("Bulletproof RPattern - Fallback")
    root.geometry("400x300")
    
    tk.Label(root, text="🚀 Bulletproof RPattern", font=("Arial", 20, "bold")).pack(pady=20)
    tk.Label(root, text=f"Data: {repr(data)}", wraplength=300).pack(pady=10)
    tk.Label(root, text="✅ Pattern would be generated here", fg="green").pack(pady=10)
    tk.Button(root, text="Close", command=root.quit, bg="red", fg="white").pack(pady=20)
    
    root.mainloop()
