# ⚓ Pirate Battles - 2D Naval Combat

A top-down naval combat game where you command a pirate ship, fire cannons, collect treasure, and battle enemy vessels!

## 🎮 About

Sail the high seas in this action-packed 2D pirate game. Navigate around islands, engage in ship-to-ship combat, and collect treasure while avoiding enemy fire!

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run the Game

```bash
python game.py
```

## 🕹️ Controls

- **Arrow Keys** or **WASD** - Steer your ship (turn left/right, move forward/backward)
- **SPACE** - Fire cannons!
- **ESC** - Quit game

## 🎯 Gameplay

### Objectives
- 🏴‍☠️ Destroy enemy pirate ships (+100 points each)
- 💰 Collect treasure chests (+50 points each)
- ❤️ Keep your ship's health above 0
- 🏝️ Navigate carefully around islands

### Features
- **Ship Physics**: Realistic turning and momentum
- **Naval Combat**: Fire cannons at enemy ships
- **AI Enemies**: Enemy ships patrol and fire back!
- **Collision Detection**: Islands block movement and cannonballs
- **Score System**: Track your performance
- **Health System**: Avoid enemy fire or it's game over!

## 🎓 What You'll Learn

This game demonstrates:
- **Top-down 2D movement** with rotation
- **Trigonometry** for angles and directions
- **Simple AI** for enemy behavior
- **Projectile physics** for cannonballs
- **Collision detection** (circles and points)
- **Game state management**

## 🛠️ Customization Ideas

### Easy Changes

1. **Adjust difficulty**: Change enemy ship count or fire rate
2. **Modify physics**: Change `max_speed`, `turn_speed`, or `acceleration`
3. **Add more islands**: Edit `create_islands()` method
4. **Change colors**: Modify color constants at the top

### Advanced Features to Add

- **Multiple enemy types** (fast scouts, heavy galleons)
- **Power-ups** (repair kits, faster cannons, shields)
- **Waves system** (increasingly difficult enemy waves)
- **Multiple weapon types** (chain shot, grapeshot)
- **Minimap** showing the entire ocean
- **Weather effects** (storms that affect movement)
- **Multiplayer** (two ships on same keyboard)

## 📝 Code Structure

```python
Game         # Main game loop and state management
PlayerShip   # Player-controlled ship with physics
EnemyShip    # AI-controlled enemy ship
Cannonball   # Projectile fired from cannons
Island       # Obstacle that blocks movement
Treasure     # Collectible item
```

## 🔧 Technical Details

- **Engine**: Pygame
- **Resolution**: 1200x800
- **FPS**: 60
- **Physics**: Angle-based movement with momentum

## 💡 Tips & Tricks

- **Turn before moving**: It's easier to steer when moving forward
- **Lead your shots**: Aim where the enemy will be, not where they are
- **Use islands as cover**: Hide behind islands to avoid enemy fire
- **Collect treasure safely**: Clear enemies first, then collect treasure

## 🎨 Assets Used

Simple geometric shapes (no external assets required)

## 📚 Next Steps

Want to enhance this game? Check out:
- The `3d-pirate-explorer` for 3D gameplay
- `TUTORIAL.txt` for detailed code explanations
- Kenney's pirate assets for better graphics

---

**Set sail and dominate the seas!** 🏴‍☠️⚓

