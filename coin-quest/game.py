"""
Simple Platformer Game using Pygame
Created with Kenney's New Platformer Pack
"""

import pygame
import sys
import os
from pathlib import Path

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Chaotic Python Platformer"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue

# Physics
GRAVITY = 0.8
JUMP_STRENGTH = -15
MOVE_SPEED = 5

# Asset paths
ASSETS_DIR = Path("app")
SPRITES_DIR = ASSETS_DIR / "Sprites"
SOUNDS_DIR = ASSETS_DIR / "Sounds"


class Game:
    """Main game class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load sounds
        self.sounds = self.load_sounds()
        
        # Create game objects
        self.player = Player(100, 300, self.sounds)
        self.platforms = self.create_level()
        self.camera_offset = 0
        
        # Score and collectibles
        self.coins_collected = 0
        self.coins = self.create_coins()
        
    def load_sounds(self):
        """Load all sound effects"""
        sounds = {}
        sound_files = {
            'jump': 'sfx_jump.ogg',
            'coin': 'sfx_coin.ogg',
            'hurt': 'sfx_hurt.ogg',
            'gem': 'sfx_gem.ogg'
        }
        
        for name, filename in sound_files.items():
            sound_path = SOUNDS_DIR / filename
            if sound_path.exists():
                sounds[name] = pygame.mixer.Sound(str(sound_path))
                sounds[name].set_volume(0.3)
            else:
                sounds[name] = None
                
        return sounds
    
    def create_level(self):
        """Create platforms for the level"""
        platforms = []
        
        # Ground platform
        platforms.append(Platform(0, SCREEN_HEIGHT - 50, 2000, 50, (100, 200, 100)))
        
        # Floating platforms
        platforms.append(Platform(200, 450, 200, 30, (139, 69, 19)))
        platforms.append(Platform(500, 400, 200, 30, (139, 69, 19)))
        platforms.append(Platform(800, 350, 200, 30, (139, 69, 19)))
        platforms.append(Platform(1100, 300, 200, 30, (139, 69, 19)))
        platforms.append(Platform(1400, 250, 250, 30, (139, 69, 19)))
        platforms.append(Platform(1700, 350, 200, 30, (139, 69, 19)))
        platforms.append(Platform(2000, 400, 200, 30, (139, 69, 19)))
        platforms.append(Platform(2300, 450, 200, 30, (139, 69, 19)))
        
        # Higher platforms for extra challenge
        platforms.append(Platform(600, 200, 150, 30, (139, 69, 19)))
        platforms.append(Platform(1200, 150, 150, 30, (139, 69, 19)))
        
        return platforms
    
    def create_coins(self):
        """Create collectible coins"""
        coins = []
        coin_positions = [
            (300, 400), (600, 350), (900, 300),
            (1200, 250), (1500, 200), (1800, 300),
            (2100, 350), (700, 150), (1300, 100)
        ]
        
        for x, y in coin_positions:
            coins.append(Coin(x, y))
            
        return coins
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()
    
    def update(self):
        """Update game state"""
        # Get keyboard input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Update player
        self.player.update(self.platforms)
        
        # Check coin collection
        for coin in self.coins[:]:
            if coin.check_collision(self.player):
                self.coins.remove(coin)
                self.coins_collected += 1
                if self.sounds['coin']:
                    self.sounds['coin'].play()
        
        # Update camera to follow player
        self.camera_offset = self.player.rect.centerx - SCREEN_WIDTH // 3
        self.camera_offset = max(0, self.camera_offset)
        
        # Check if player fell off the world
        if self.player.rect.top > SCREEN_HEIGHT + 100:
            self.player.reset_position(100, 300)
            if self.sounds['hurt']:
                self.sounds['hurt'].play()
    
    def draw(self):
        """Draw everything to screen"""
        # Clear screen with sky color
        self.screen.fill(BLUE)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_offset)
        
        # Draw coins
        for coin in self.coins:
            coin.draw(self.screen, self.camera_offset)
        
        # Draw player
        self.player.draw(self.screen, self.camera_offset)
        
        # Draw UI
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw user interface elements"""
        font = pygame.font.Font(None, 36)
        
        # Draw coins collected
        coin_text = font.render(f"Coins: {self.coins_collected}/{len(self.coins) + self.coins_collected}", True, BLACK)
        coin_bg = pygame.Surface((coin_text.get_width() + 20, coin_text.get_height() + 10))
        coin_bg.fill(WHITE)
        coin_bg.set_alpha(200)
        
        self.screen.blit(coin_bg, (10, 10))
        self.screen.blit(coin_text, (20, 15))
        
        # Draw controls hint
        hint_font = pygame.font.Font(None, 24)
        hint_text = hint_font.render("Arrow Keys: Move | Space/Up: Jump | ESC: Quit", True, BLACK)
        hint_bg = pygame.Surface((hint_text.get_width() + 20, hint_text.get_height() + 10))
        hint_bg.fill(WHITE)
        hint_bg.set_alpha(150)
        
        self.screen.blit(hint_bg, (SCREEN_WIDTH - hint_text.get_width() - 30, SCREEN_HEIGHT - 40))
        self.screen.blit(hint_text, (SCREEN_WIDTH - hint_text.get_width() - 20, SCREEN_HEIGHT - 35))
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


class Player:
    """Player character class"""
    
    def __init__(self, x, y, sounds):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.facing_right = True
        self.sounds = sounds
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.state = 'idle'  # idle, walking, jumping
        
        # Colors for simple character representation
        self.colors = {
            'body': (100, 200, 255),
            'outline': (50, 100, 150)
        }
        
        # Start position for reset
        self.start_x = x
        self.start_y = y
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        self.velocity_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -MOVE_SPEED
            self.facing_right = False
            if self.on_ground:
                self.state = 'walking'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = MOVE_SPEED
            self.facing_right = True
            if self.on_ground:
                self.state = 'walking'
        else:
            if self.on_ground:
                self.state = 'idle'
    
    def jump(self):
        """Make player jump"""
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            self.state = 'jumping'
            if self.sounds['jump']:
                self.sounds['jump'].play()
    
    def update(self, platforms):
        """Update player position and physics"""
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Limit fall speed
        if self.velocity_y > 20:
            self.velocity_y = 20
        
        # Update animation
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
        
        # Move horizontally
        self.rect.x += self.velocity_x
        
        # Check horizontal collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:  # Moving left
                    self.rect.left = platform.rect.right
        
        # Move vertically
        self.rect.y += self.velocity_y
        
        # Check vertical collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        
        # Update state
        if not self.on_ground:
            self.state = 'jumping'
    
    def draw(self, screen, camera_offset):
        """Draw player to screen"""
        draw_x = self.rect.x - camera_offset
        
        # Draw simple character
        body_rect = pygame.Rect(draw_x, self.rect.y, self.rect.width, self.rect.height)
        
        # Body
        pygame.draw.rect(screen, self.colors['body'], body_rect, border_radius=5)
        pygame.draw.rect(screen, self.colors['outline'], body_rect, 3, border_radius=5)
        
        # Head
        head_size = 25
        head_x = draw_x + self.rect.width // 2
        head_y = self.rect.y + 15
        pygame.draw.circle(screen, self.colors['body'], (int(head_x), int(head_y)), head_size)
        pygame.draw.circle(screen, self.colors['outline'], (int(head_x), int(head_y)), head_size, 3)
        
        # Eyes
        eye_offset = 8 if self.facing_right else -8
        pygame.draw.circle(screen, WHITE, (int(head_x + eye_offset), int(head_y - 5)), 6)
        pygame.draw.circle(screen, BLACK, (int(head_x + eye_offset), int(head_y - 5)), 3)
        
        # Arms (animate when walking)
        if self.state == 'walking':
            arm_swing = 10 if self.animation_frame % 2 == 0 else -10
        else:
            arm_swing = 0
            
        # Left arm
        pygame.draw.line(screen, self.colors['outline'], 
                        (draw_x + 10, self.rect.y + 35), 
                        (draw_x + 5, self.rect.y + 35 + arm_swing), 4)
        
        # Right arm
        pygame.draw.line(screen, self.colors['outline'], 
                        (draw_x + self.rect.width - 10, self.rect.y + 35), 
                        (draw_x + self.rect.width - 5, self.rect.y + 35 - arm_swing), 4)
    
    def reset_position(self, x, y):
        """Reset player to starting position"""
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.velocity_x = 0


class Platform:
    """Platform class"""
    
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, screen, camera_offset):
        """Draw platform to screen"""
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_offset
        
        # Only draw if on screen
        if -self.rect.width < draw_rect.x < SCREEN_WIDTH:
            pygame.draw.rect(screen, self.color, draw_rect)
            pygame.draw.rect(screen, (0, 0, 0), draw_rect, 2)


class Coin:
    """Collectible coin class"""
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.original_y = y
        self.float_offset = 0
        self.float_speed = 0.1
        self.color = (255, 215, 0)  # Gold
    
    def check_collision(self, player):
        """Check if player collected this coin"""
        return self.rect.colliderect(player.rect)
    
    def draw(self, screen, camera_offset):
        """Draw coin to screen with floating animation"""
        import math
        self.float_offset += self.float_speed
        
        draw_x = self.rect.x - camera_offset
        draw_y = self.original_y + math.sin(self.float_offset) * 5
        
        # Only draw if on screen
        if -self.rect.width < draw_x < SCREEN_WIDTH:
            # Outer ring
            pygame.draw.circle(screen, self.color, (int(draw_x + 10), int(draw_y + 10)), 12)
            # Inner highlight
            pygame.draw.circle(screen, (255, 255, 200), (int(draw_x + 10), int(draw_y + 10)), 8)
            # Dark outline
            pygame.draw.circle(screen, (200, 150, 0), (int(draw_x + 10), int(draw_y + 10)), 12, 2)


def main():
    """Main function to start the game"""
    print("=" * 50)
    print(">>> CHAOTIC PYTHON PLATFORMER <<<")
    print("=" * 50)
    print("\nControls:")
    print("  Arrow Keys / A,D : Move left and right")
    print("  Space / Up Arrow : Jump")
    print("  ESC              : Quit game")
    print("\nObjective: Collect all the coins!")
    print("\nStarting game...")
    print("=" * 50)
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

