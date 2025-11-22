"""
2D Top-Down Pirate Naval Battle Game
Sail your ship, fire cannons, and explore the seas!
"""

import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TITLE = "Pirate Battles - Naval Combat"

# Colors
OCEAN_BLUE = (41, 128, 185)
SAND = (194, 178, 128)
DARK_GREEN = (39, 174, 96)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (231, 76, 60)
GOLD = (241, 196, 15)


class Game:
    """Main game class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game objects
        self.player_ship = PlayerShip(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.islands = self.create_islands()
        self.enemy_ships = self.create_enemies()
        self.cannonballs = []
        self.treasure_chests = self.create_treasures()
        
        # Score
        self.score = 0
        self.enemies_destroyed = 0
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def create_islands(self):
        """Create islands to navigate around"""
        islands = []
        island_data = [
            (200, 150, 80),
            (900, 200, 100),
            (300, 600, 60),
            (800, 650, 90),
            (600, 400, 70),
        ]
        
        for x, y, radius in island_data:
            islands.append(Island(x, y, radius))
        
        return islands
    
    def create_enemies(self):
        """Create enemy pirate ships"""
        enemies = []
        enemy_positions = [
            (400, 200),
            (800, 400),
            (300, 500),
            (1000, 600),
        ]
        
        for x, y in enemy_positions:
            enemies.append(EnemyShip(x, y))
        
        return enemies
    
    def create_treasures(self):
        """Create treasure chests to collect"""
        treasures = []
        treasure_positions = [
            (150, 100),
            (950, 150),
            (250, 650),
            (850, 700),
            (550, 350),
            (100, 400),
            (1100, 500),
        ]
        
        for x, y in treasure_positions:
            treasures.append(Treasure(x, y))
        
        return treasures
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Fire cannonball
                    cannonball = self.player_ship.fire()
                    if cannonball:
                        self.cannonballs.append(cannonball)
    
    def update(self):
        """Update game state"""
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Update player ship
        self.player_ship.update(keys, self.islands)
        
        # Update enemy ships
        for enemy in self.enemy_ships[:]:
            enemy.update(self.player_ship, self.islands)
            
            # Enemy shoots occasionally
            if random.randint(0, 100) < 2:  # 2% chance each frame
                cannonball = enemy.fire()
                if cannonball:
                    self.cannonballs.append(cannonball)
        
        # Update cannonballs
        for cannonball in self.cannonballs[:]:
            cannonball.update()
            
            # Remove if off screen
            if (cannonball.x < 0 or cannonball.x > SCREEN_WIDTH or
                cannonball.y < 0 or cannonball.y > SCREEN_HEIGHT):
                self.cannonballs.remove(cannonball)
                continue
            
            # Check collision with islands
            for island in self.islands:
                if island.check_collision_point(cannonball.x, cannonball.y):
                    if cannonball in self.cannonballs:
                        self.cannonballs.remove(cannonball)
                    break
            
            # Check collision with enemy ships
            if cannonball.fired_by == 'player':
                for enemy in self.enemy_ships[:]:
                    if enemy.check_collision(cannonball.x, cannonball.y):
                        self.enemy_ships.remove(enemy)
                        if cannonball in self.cannonballs:
                            self.cannonballs.remove(cannonball)
                        self.score += 100
                        self.enemies_destroyed += 1
                        break
            
            # Check collision with player ship
            elif cannonball.fired_by == 'enemy':
                if self.player_ship.check_collision(cannonball.x, cannonball.y):
                    if cannonball in self.cannonballs:
                        self.cannonballs.remove(cannonball)
                    self.player_ship.take_damage(10)
        
        # Check treasure collection
        for treasure in self.treasure_chests[:]:
            if treasure.check_collision(self.player_ship.x, self.player_ship.y):
                self.treasure_chests.remove(treasure)
                self.score += 50
        
        # Check game over
        if self.player_ship.health <= 0:
            self.running = False
    
    def draw(self):
        """Draw everything to screen"""
        # Draw ocean
        self.screen.fill(OCEAN_BLUE)
        
        # Draw islands
        for island in self.islands:
            island.draw(self.screen)
        
        # Draw treasures
        for treasure in self.treasure_chests:
            treasure.draw(self.screen)
        
        # Draw enemy ships
        for enemy in self.enemy_ships:
            enemy.draw(self.screen)
        
        # Draw player ship
        self.player_ship.draw(self.screen)
        
        # Draw cannonballs
        for cannonball in self.cannonballs:
            cannonball.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw user interface"""
        # Health bar
        health_text = self.small_font.render(f"Health: {self.player_ship.health}/100", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        # Draw health bar
        bar_width = 200
        bar_height = 20
        health_ratio = self.player_ship.health / 100
        pygame.draw.rect(self.screen, RED, (10, 35, bar_width, bar_height))
        pygame.draw.rect(self.screen, DARK_GREEN, (10, 35, bar_width * health_ratio, bar_height))
        pygame.draw.rect(self.screen, WHITE, (10, 35, bar_width, bar_height), 2)
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, GOLD)
        self.screen.blit(score_text, (10, 65))
        
        # Enemies destroyed
        enemies_text = self.small_font.render(f"Enemies: {self.enemies_destroyed}", True, WHITE)
        self.screen.blit(enemies_text, (10, 105))
        
        # Controls
        controls = [
            "Arrow Keys: Move",
            "SPACE: Fire Cannon",
            "ESC: Quit"
        ]
        
        y_offset = SCREEN_HEIGHT - 90
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            bg = pygame.Surface((text.get_width() + 10, text.get_height() + 5))
            bg.fill(BLACK)
            bg.set_alpha(150)
            self.screen.blit(bg, (SCREEN_WIDTH - text.get_width() - 15, y_offset + i * 25))
            self.screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, y_offset + i * 25 + 2))
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Game over screen
        self.show_game_over()
        pygame.quit()
        sys.exit()
    
    def show_game_over(self):
        """Show game over screen"""
        self.screen.fill(BLACK)
        
        game_over_text = self.font.render("GAME OVER!", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, GOLD)
        enemies_text = self.font.render(f"Enemies Destroyed: {self.enemies_destroyed}", True, WHITE)
        
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        enemies_rect = enemies_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(enemies_text, enemies_rect)
        
        pygame.display.flip()
        pygame.time.wait(3000)


class PlayerShip:
    """Player's pirate ship"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Direction ship is facing (0 = right)
        self.speed = 0
        self.max_speed = 4
        self.acceleration = 0.2
        self.turn_speed = 3
        self.health = 100
        self.size = 30
        self.cannon_cooldown = 0
        
    def update(self, keys, islands):
        """Update ship position and rotation"""
        # Rotation
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += self.turn_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= self.turn_speed
        
        # Forward/backward movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
        else:
            # Natural deceleration
            if self.speed > 0:
                self.speed = max(0, self.speed - self.acceleration / 2)
            elif self.speed < 0:
                self.speed = min(0, self.speed + self.acceleration / 2)
        
        # Calculate new position
        angle_rad = math.radians(self.angle)
        new_x = self.x + math.cos(angle_rad) * self.speed
        new_y = self.y - math.sin(angle_rad) * self.speed
        
        # Check collision with islands
        can_move = True
        for island in islands:
            if island.check_collision_point(new_x, new_y):
                can_move = False
                self.speed = 0
                break
        
        # Update position if no collision
        if can_move:
            self.x = max(self.size, min(SCREEN_WIDTH - self.size, new_x))
            self.y = max(self.size, min(SCREEN_HEIGHT - self.size, new_y))
        
        # Update cannon cooldown
        if self.cannon_cooldown > 0:
            self.cannon_cooldown -= 1
    
    def fire(self):
        """Fire a cannonball"""
        if self.cannon_cooldown == 0:
            self.cannon_cooldown = 30  # Half second cooldown at 60 FPS
            
            # Create cannonball in front of ship
            angle_rad = math.radians(self.angle)
            offset = self.size + 10
            cannon_x = self.x + math.cos(angle_rad) * offset
            cannon_y = self.y - math.sin(angle_rad) * offset
            
            return Cannonball(cannon_x, cannon_y, self.angle, 'player')
        return None
    
    def take_damage(self, damage):
        """Take damage"""
        self.health = max(0, self.health - damage)
    
    def check_collision(self, x, y):
        """Check if point collides with ship"""
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance < self.size
    
    def draw(self, screen):
        """Draw the ship"""
        # Draw ship as a triangle
        angle_rad = math.radians(self.angle)
        
        # Calculate triangle points
        front_x = self.x + math.cos(angle_rad) * self.size
        front_y = self.y - math.sin(angle_rad) * self.size
        
        left_angle = angle_rad + math.radians(135)
        left_x = self.x + math.cos(left_angle) * self.size * 0.7
        left_y = self.y - math.sin(left_angle) * self.size * 0.7
        
        right_angle = angle_rad - math.radians(135)
        right_x = self.x + math.cos(right_angle) * self.size * 0.7
        right_y = self.y - math.sin(right_angle) * self.size * 0.7
        
        # Draw ship
        points = [(front_x, front_y), (left_x, left_y), (right_x, right_y)]
        pygame.draw.polygon(screen, BROWN, points)
        pygame.draw.polygon(screen, BLACK, points, 3)
        
        # Draw sail (white triangle)
        sail_size = self.size * 0.4
        sail_front = (self.x + math.cos(angle_rad) * sail_size,
                     self.y - math.sin(angle_rad) * sail_size)
        sail_left = (self.x + math.cos(angle_rad + math.radians(90)) * sail_size * 0.5,
                    self.y - math.sin(angle_rad + math.radians(90)) * sail_size * 0.5)
        sail_right = (self.x + math.cos(angle_rad - math.radians(90)) * sail_size * 0.5,
                     self.y - math.sin(angle_rad - math.radians(90)) * sail_size * 0.5)
        
        sail_points = [sail_front, sail_left, sail_right]
        pygame.draw.polygon(screen, WHITE, sail_points)
        pygame.draw.polygon(screen, BLACK, sail_points, 2)


class EnemyShip:
    """Enemy pirate ship with simple AI"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.randint(0, 360)
        self.speed = 2
        self.size = 25
        self.cannon_cooldown = 0
        self.patrol_timer = 0
        self.target_angle = self.angle
        
    def update(self, player, islands):
        """Update enemy ship AI"""
        # Simple patrol behavior
        self.patrol_timer += 1
        
        if self.patrol_timer > 120:  # Change direction every 2 seconds
            self.target_angle = random.randint(0, 360)
            self.patrol_timer = 0
        
        # Smoothly turn towards target angle
        angle_diff = (self.target_angle - self.angle + 180) % 360 - 180
        if abs(angle_diff) > 2:
            self.angle += 2 if angle_diff > 0 else -2
        
        # Move forward
        angle_rad = math.radians(self.angle)
        new_x = self.x + math.cos(angle_rad) * self.speed
        new_y = self.y - math.sin(angle_rad) * self.speed
        
        # Check boundaries
        if 0 < new_x < SCREEN_WIDTH and 0 < new_y < SCREEN_HEIGHT:
            # Check island collision
            can_move = True
            for island in islands:
                if island.check_collision_point(new_x, new_y):
                    can_move = False
                    self.target_angle = (self.angle + 180) % 360
                    break
            
            if can_move:
                self.x = new_x
                self.y = new_y
        else:
            # Bounce off walls
            self.target_angle = (self.angle + 180) % 360
        
        # Update cannon cooldown
        if self.cannon_cooldown > 0:
            self.cannon_cooldown -= 1
    
    def fire(self):
        """Fire a cannonball"""
        if self.cannon_cooldown == 0:
            self.cannon_cooldown = 90  # 1.5 second cooldown
            
            angle_rad = math.radians(self.angle)
            offset = self.size + 10
            cannon_x = self.x + math.cos(angle_rad) * offset
            cannon_y = self.y - math.sin(angle_rad) * offset
            
            return Cannonball(cannon_x, cannon_y, self.angle, 'enemy')
        return None
    
    def check_collision(self, x, y):
        """Check if point collides with ship"""
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance < self.size
    
    def draw(self, screen):
        """Draw enemy ship (red sails)"""
        angle_rad = math.radians(self.angle)
        
        # Ship body
        front_x = self.x + math.cos(angle_rad) * self.size
        front_y = self.y - math.sin(angle_rad) * self.size
        
        left_angle = angle_rad + math.radians(135)
        left_x = self.x + math.cos(left_angle) * self.size * 0.7
        left_y = self.y - math.sin(left_angle) * self.size * 0.7
        
        right_angle = angle_rad - math.radians(135)
        right_x = self.x + math.cos(right_angle) * self.size * 0.7
        right_y = self.y - math.sin(right_angle) * self.size * 0.7
        
        points = [(front_x, front_y), (left_x, left_y), (right_x, right_y)]
        pygame.draw.polygon(screen, (100, 50, 20), points)
        pygame.draw.polygon(screen, BLACK, points, 2)
        
        # Red sail
        sail_size = self.size * 0.4
        sail_front = (self.x + math.cos(angle_rad) * sail_size,
                     self.y - math.sin(angle_rad) * sail_size)
        sail_left = (self.x + math.cos(angle_rad + math.radians(90)) * sail_size * 0.5,
                    self.y - math.sin(angle_rad + math.radians(90)) * sail_size * 0.5)
        sail_right = (self.x + math.cos(angle_rad - math.radians(90)) * sail_size * 0.5,
                     self.y - math.sin(angle_rad - math.radians(90)) * sail_size * 0.5)
        
        sail_points = [sail_front, sail_left, sail_right]
        pygame.draw.polygon(screen, RED, sail_points)
        pygame.draw.polygon(screen, BLACK, sail_points, 2)


class Cannonball:
    """Cannonball projectile"""
    
    def __init__(self, x, y, angle, fired_by):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.fired_by = fired_by
        self.radius = 5
    
    def update(self):
        """Update cannonball position"""
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * self.speed
        self.y -= math.sin(angle_rad) * self.speed
    
    def draw(self, screen):
        """Draw cannonball"""
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (50, 50, 50), (int(self.x), int(self.y)), self.radius - 1)


class Island:
    """Island obstacle"""
    
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    
    def check_collision_point(self, x, y):
        """Check if point is inside island"""
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance < self.radius
    
    def draw(self, screen):
        """Draw island"""
        # Sand circle
        pygame.draw.circle(screen, SAND, (int(self.x), int(self.y)), self.radius)
        
        # Add some palm trees (simple)
        for i in range(3):
            angle = (i * 120) + random.randint(-10, 10)
            offset = self.radius * 0.4
            tree_x = self.x + math.cos(math.radians(angle)) * offset
            tree_y = self.y + math.sin(math.radians(angle)) * offset
            
            # Trunk
            pygame.draw.circle(screen, BROWN, (int(tree_x), int(tree_y)), 3)
            # Leaves
            pygame.draw.circle(screen, DARK_GREEN, (int(tree_x), int(tree_y - 5)), 6)
        
        # Outline
        pygame.draw.circle(screen, (150, 140, 100), (int(self.x), int(self.y)), self.radius, 2)


class Treasure:
    """Treasure chest to collect"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 15
        self.collected = False
        self.float_offset = random.random() * 6.28
    
    def check_collision(self, x, y):
        """Check if player collected treasure"""
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance < self.size + 10
    
    def draw(self, screen):
        """Draw treasure chest"""
        # Floating animation
        self.float_offset += 0.05
        float_y = self.y + math.sin(self.float_offset) * 3
        
        # Chest
        rect = pygame.Rect(self.x - self.size // 2, float_y - self.size // 2, 
                          self.size, self.size)
        pygame.draw.rect(screen, GOLD, rect)
        pygame.draw.rect(screen, (200, 150, 0), rect, 2)
        
        # Shine effect
        pygame.draw.circle(screen, (255, 255, 200), (int(self.x), int(float_y)), 3)


def main():
    """Main function to start the game"""
    print("=" * 60)
    print(">>> PIRATE BATTLES - NAVAL COMBAT <<<")
    print("=" * 60)
    print("\nControls:")
    print("  Arrow Keys / WASD : Steer your ship")
    print("  SPACE             : Fire cannons!")
    print("  ESC               : Quit game")
    print("\nObjective:")
    print("  - Destroy enemy ships")
    print("  - Collect treasure chests")
    print("  - Avoid enemy cannonballs")
    print("  - Don't crash into islands!")
    print("\nStarting game...")
    print("=" * 60)
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

