# 🏝️ Pirate Island Explorer 3D

A 3D first-person exploration game where you walk around a pirate island and collect hidden treasure chests!

## 🎮 About

Experience the thrill of exploring a 3D pirate island! Walk around in first-person view, jump over rocks, navigate between palm trees, and discover hidden treasure chests scattered across the island.

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

**Note**: Ursina requires Python 3.6+ and will automatically install dependencies (Panda3D, etc.)

### Run the Game

```bash
python game.py
```

## 🕹️ Controls

- **W/A/S/D** - Move around (forward/left/backward/right)
- **Mouse** - Look around (camera control)
- **SPACE** - Jump
- **ESC** - Quit and see final stats

## 🎯 Gameplay

### Objective
🏴‍☠️ Find and collect all 11 treasure chests hidden around the island!

### Features
- **First-Person 3D**: Immersive 3D environment
- **Free Exploration**: Roam the entire island
- **Treasure Hunt**: Find glowing, rotating treasure chests
- **Interactive Props**: Barrels, palm trees, and rocks
- **Dynamic Lighting**: Beautiful sky and lighting
- **Physics**: Jump and navigate 3D terrain

## 🎓 What You'll Learn

This game teaches:
- **3D Game Development** with Ursina engine
- **First-Person Controllers** (FPS movement)
- **3D Positioning** (X, Y, Z coordinates)
- **Entity System** (creating 3D objects)
- **3D Collision Detection**
- **Lighting and Environment** setup
- **Camera Control** in 3D space

## 🛠️ Customization Ideas

### Easy Changes

1. **Add more treasures**: Duplicate treasure positions in `create_treasures()`
2. **Change island colors**: Modify RGB values for sand, water, trees
3. **Adjust player speed**: Change `speed` in `FirstPersonController`
4. **Make island bigger**: Increase scale of main island plane

### Advanced Features to Add

- **Multiple islands**: Create islands you can jump between
- **Enemies**: Add AI pirates that patrol the island
- **Quests**: Hide maps that reveal treasure locations
- **Boats**: Add a rowboat you can ride
- **Caves**: Create underground treasure caves
- **Day/Night cycle**: Change lighting over time
- **Weather effects**: Add rain or fog
- **Inventory system**: Collect different types of items
- **3D Models**: Use the actual pirate-den 3D models (GLB/FBX files)

## 📝 Code Structure

```python
PirateIslandGame    # Main game class
  - setup_environment()    # Sky, ocean, lighting
  - setup_player()        # First-person controller
  - create_island()       # Main island terrain
  - create_palm_trees()   # Vegetation
  - create_treasures()    # Collectibles
  - update()             # Game loop

Treasure            # Collectible treasure chest
  - Rotates and floats
  - Has sparkle effect
  - Checks player distance
```

## 🔧 Technical Details

- **Engine**: Ursina (built on Panda3D)
- **3D Rendering**: Real-time 3D graphics
- **Controls**: First-person FPS-style
- **Physics**: Built-in Ursina physics

## 💡 Tips for Playing

- **Look around**: Use your mouse to scan for glowing treasure chests
- **Explore thoroughly**: Treasures are scattered all over the island
- **Jump carefully**: Use SPACE to jump over obstacles
- **Check behind trees**: Some treasures hide behind palm trees

## 🎨 Using the Pirate-Den 3D Models

Want to use the actual 3D pirate models? Here's how:

### Loading GLB Models

```python
# Load a pirate ship model
ship = Entity(
    model='path/to/pirate-den/Models/GLB format/ship-large.glb',
    position=(10, 0, 10),
    scale=2,
    collider='box'
)

# Load a treasure chest
chest_model = Entity(
    model='path/to/pirate-den/Models/GLB format/chest.glb',
    position=(5, 0, 5),
    scale=1
)
```

### Models Available in Pirate-Den

- **Ships**: ship-large, ship-medium, ship-small, ship-pirate-large
- **Props**: barrel, chest, cannon, crate, bottle
- **Structures**: tower-complete, structure-platform, structure-fence
- **Nature**: palm-straight, palm-bend, rocks-a/b/c
- **And 50+ more models!**

## 🆚 2D vs 3D Comparison

| Feature | 2D (pirate-battles-2d) | 3D (This Game) |
|---------|------------------------|----------------|
| View | Top-down | First-person |
| Movement | X, Y (2D plane) | X, Y, Z (3D space) |
| Camera | Fixed | Free-look |
| Complexity | Simpler | More complex |
| Performance | Faster | Heavier |
| Learning Curve | Easier | Steeper |

## 📚 Learning Path

1. **Start with 2D** (pirate-battles-2d) to learn basics
2. **Then try 3D** (this game) to level up
3. **Read tutorials** to understand concepts
4. **Modify and experiment** to learn by doing

## 🔗 Resources

- [Ursina Documentation](https://www.ursinaengine.org/)
- [Panda3D Manual](https://docs.panda3d.org/)
- [3D Game Development Basics](https://www.ursinaengine.org/documentation.html)

---

**Explore the island and claim your treasure!** 🏴‍☠️💰🏝️

