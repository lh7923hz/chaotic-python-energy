"""
3D Pirate Island Explorer
Walk around a pirate island, collect treasure, and explore in 3D!
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

class PirateIslandGame(Ursina):
    """Main 3D pirate game"""
    
    def __init__(self):
        super().__init__()
        
        # Game settings
        window.title = "Pirate Island Explorer 3D"
        window.borderless = False
        window.fullscreen = False
        window.exit_button.visible = False
        window.fps_counter.enabled = True
        
        # Score
        self.treasure_collected = 0
        self.total_treasures = 0
        
        # Setup game
        self.setup_environment()
        self.setup_player()
        self.create_island()
        self.create_treasures()
        self.create_props()
        self.setup_ui()
        
        print("=" * 60)
        print("🏴‍☠️ PIRATE ISLAND EXPLORER 3D 🏴‍☠️")
        print("=" * 60)
        print("\nControls:")
        print("  WASD      : Move around")
        print("  Mouse     : Look around")
        print("  SPACE     : Jump")
        print("  ESC       : Quit")
        print("\nObjective: Find and collect all the treasure chests!")
        print("=" * 60)
    
    def setup_environment(self):
        """Setup sky, lighting, and environment"""
        # Sky
        Sky(color=color.rgb(135, 206, 250))  # Nice blue sky
        
        # Sun/lighting
        DirectionalLight(y=2, z=3, shadows=True, rotation=(45, -45, 45))
        
        # Ambient light
        AmbientLight(color=color.rgba(255, 255, 255, 0.3))
        
        # Ocean (large blue plane)
        self.ocean = Entity(
            model='plane',
            texture='white_cube',
            color=color.rgb(41, 128, 185),
            scale=(200, 1, 200),
            y=-0.5,
            collider='box'
        )
    
    def setup_player(self):
        """Setup first-person player controller"""
        self.player = FirstPersonController(
            position=(0, 2, -10),
            speed=5,
            jump_height=2
        )
        
        # Make mouse visible
        mouse.locked = True
        
    def create_island(self):
        """Create the main island"""
        # Main island (large sandy platform)
        self.island = Entity(
            model='plane',
            texture='white_cube',
            color=color.rgb(194, 178, 128),  # Sand color
            scale=(40, 1, 40),
            y=0,
            collider='box'
        )
        
        # Add some height variation with smaller platforms
        for i in range(5):
            x = random.uniform(-15, 15)
            z = random.uniform(-15, 15)
            height = random.uniform(0.5, 2)
            size = random.uniform(3, 8)
            
            Entity(
                model='cube',
                texture='white_cube',
                color=color.rgb(194, 178, 128),
                position=(x, height / 2, z),
                scale=(size, height, size),
                collider='box'
            )
        
        # Palm trees
        self.create_palm_trees()
        
        # Rocks
        self.create_rocks()
    
    def create_palm_trees(self):
        """Create simple palm trees"""
        tree_positions = [
            (-12, 0, -12), (12, 0, -12), (-12, 0, 12), (12, 0, 12),
            (-8, 0, 0), (8, 0, 0), (0, 0, -8), (0, 0, 8),
            (-15, 0, -5), (15, 0, 5), (-5, 0, -15), (5, 0, 15)
        ]
        
        for pos in tree_positions:
            # Trunk
            trunk = Entity(
                model='cylinder',
                color=color.rgb(101, 67, 33),
                position=pos,
                scale=(0.3, 4, 0.3),
                collider='box'
            )
            
            # Leaves (green sphere on top)
            leaves = Entity(
                model='sphere',
                color=color.rgb(34, 139, 34),
                position=(pos[0], pos[1] + 3, pos[2]),
                scale=(2, 1.5, 2)
            )
    
    def create_rocks(self):
        """Create decorative rocks"""
        for i in range(20):
            x = random.uniform(-18, 18)
            z = random.uniform(-18, 18)
            scale_val = random.uniform(0.5, 1.5)
            
            Entity(
                model='sphere',
                color=color.rgb(128, 128, 128),
                position=(x, scale_val / 2, z),
                scale=(scale_val, scale_val * 0.7, scale_val),
                collider='box'
            )
    
    def create_treasures(self):
        """Create treasure chests to collect"""
        self.treasures = []
        treasure_positions = [
            (-10, 1, -10), (10, 1, -10), (-10, 1, 10), (10, 1, 10),
            (0, 1, 0), (-5, 1, 5), (5, 1, -5),
            (-15, 1, 0), (15, 1, 0), (0, 1, -15), (0, 1, 15)
        ]
        
        for pos in treasure_positions:
            treasure = Treasure(pos)
            self.treasures.append(treasure)
            self.total_treasures += 1
    
    def create_props(self):
        """Create barrels, crates, and other props"""
        prop_positions = [
            (-8, 0.5, -8), (8, 0.5, 8), (-6, 0.5, 6),
            (6, 0.5, -6), (3, 0.5, -10), (-3, 0.5, 10)
        ]
        
        for pos in prop_positions:
            # Barrel
            Entity(
                model='cylinder',
                color=color.rgb(139, 69, 19),
                position=pos,
                scale=(0.8, 1, 0.8),
                collider='box'
            )
    
    def setup_ui(self):
        """Setup user interface"""
        self.treasure_text = Text(
            text=f'Treasure: {self.treasure_collected}/{self.total_treasures}',
            position=(-0.85, 0.45),
            origin=(0, 0),
            scale=2,
            color=color.rgb(241, 196, 15)
        )
        
        self.controls_text = Text(
            text='WASD: Move | Mouse: Look | SPACE: Jump | ESC: Quit',
            position=(0, -0.45),
            origin=(0, 0),
            scale=1.2,
            color=color.white
        )
    
    def input(self, key):
        """Handle input"""
        if key == 'escape':
            self.check_game_complete()
            application.quit()
    
    def update(self):
        """Update game (called every frame)"""
        # Check treasure collection
        for treasure in self.treasures[:]:
            if treasure.check_collection(self.player.position):
                self.treasure_collected += 1
                self.treasures.remove(treasure)
                treasure.collect()
                self.update_ui()
                
                # Check if all treasures collected
                if self.treasure_collected >= self.total_treasures:
                    self.win_game()
    
    def update_ui(self):
        """Update UI text"""
        self.treasure_text.text = f'Treasure: {self.treasure_collected}/{self.total_treasures}'
    
    def win_game(self):
        """Show win message"""
        win_text = Text(
            text='🎉 YOU FOUND ALL THE TREASURE! 🎉',
            position=(0, 0.2),
            origin=(0, 0),
            scale=3,
            color=color.rgb(241, 196, 15),
            background=True
        )
        
        quit_text = Text(
            text='Press ESC to quit',
            position=(0, 0),
            origin=(0, 0),
            scale=2,
            color=color.white
        )
    
    def check_game_complete(self):
        """Print final stats when quitting"""
        print("\n" + "=" * 60)
        print("📊 FINAL STATS")
        print("=" * 60)
        print(f"Treasure Collected: {self.treasure_collected}/{self.total_treasures}")
        
        if self.treasure_collected >= self.total_treasures:
            print("🎉 CONGRATULATIONS! You found all the treasure!")
        else:
            print(f"💰 You found {self.treasure_collected} treasures!")
            print(f"   There are {self.total_treasures - self.treasure_collected} still hidden on the island!")
        print("=" * 60)


class Treasure(Entity):
    """Treasure chest entity"""
    
    def __init__(self, position):
        super().__init__(
            model='cube',
            color=color.rgb(241, 196, 15),  # Gold color
            position=position,
            scale=(1, 0.8, 0.8),
            collider='box'
        )
        
        self.original_y = position[1]
        self.rotation_speed = 50
        self.float_speed = 1
        self.time = 0
        
        # Add sparkle on top
        self.sparkle = Entity(
            model='sphere',
            color=color.rgb(255, 255, 200),
            position=(position[0], position[1] + 0.5, position[2]),
            scale=0.3
        )
    
    def update(self):
        """Animate treasure (rotate and float)"""
        self.time += time.dt
        
        # Rotate
        self.rotation_y += self.rotation_speed * time.dt
        
        # Float up and down
        self.y = self.original_y + math.sin(self.time * self.float_speed) * 0.2
        
        # Update sparkle position
        if self.sparkle:
            self.sparkle.position = (self.x, self.y + 0.5, self.z)
            self.sparkle.scale = 0.3 + math.sin(self.time * 2) * 0.1
    
    def check_collection(self, player_pos):
        """Check if player is close enough to collect"""
        distance = Vec3(player_pos.x - self.x, 0, player_pos.z - self.z).length()
        return distance < 2
    
    def collect(self):
        """Collect the treasure"""
        # Play a simple sound (if available)
        # Audio('collect_sound')  # Uncomment if you have sound files
        
        # Remove sparkle
        if self.sparkle:
            destroy(self.sparkle)
        
        # Destroy the treasure
        destroy(self)


def main():
    """Main function"""
    game = PirateIslandGame()
    game.run()


if __name__ == '__main__':
    main()

