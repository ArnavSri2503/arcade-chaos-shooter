Arcade Chaos Shooter

Designed and developed a modular 2D arcade shooter in Python (Pygame), using iterative prototyping and AI-assisted development while focusing on gameplay systems, debugging, and performance optimization.

Built through multiple iterations, with earlier versions exploring mechanics such as basic shooting, enemy behaviors, and visual effects before evolving into a structured, multi-mode system.

arcade-chaos-shooter

A fast-paced 2D arcade shooter featuring multiple game modes, dynamic weapon loadouts, pattern-based chaos waves, and multi-phase boss fights with strong emphasis on game feel and visual feedback.

Features:
> Core Gameplay
Free movement with precision focus mode
Continuous auto-firing system
Score-based progression
Multiple gameplay phases (Wave → Boss → Chaos)

> Game Modes
Classic – Wave → Boss → Chaos progression
Endless Survival – Infinite scaling enemy waves
Boss Rush – Continuous boss fights
Chaos Arena – Pattern-based swarm gameplay
Hardcore – 1 HP challenge mode

> Weapon System
Object-oriented weapon architecture
Pre-game loadout selection (limited slots)
Weapon switching during gameplay

Weapons include:

Normal – standard shots
Spread – multi-directional bullets
Rapid – high fire rate
Homing – target-seeking bullets
Laser – continuous beam damage
Shotgun – wide burst attack

> Enemy System
Sniper – aimed projectile attacks
Charger – aggressive tracking movement
Orbit – sinusoidal movement patterns
Zigzag – unpredictable lateral motion
Splitter – variation-based behavior

> Boss System
Multi-phase boss design

Phases include:
Radial bullet bursts
Spiral attack patterns
Safe-zone shifting chaos phase

Additional features:
Boss warning splash ("WARNING: BOSS INCOMING")
Health-based phase transitions
Slow-motion effect on boss defeat

> Chaos System
Pattern-based wave generation (not random spam)
Dynamic safe zone shifting
Balanced density for playability
Increasing pressure with controlled fairness

> Visual Polish

Screen shake on:
-hits
-explosions
-boss attacks

Particle system for explosions and feedback
Hit flash on enemies
Layered laser beam visuals
Background starfield movement
Fade transitions between phases

> Player Systems
Health system with invulnerability frames

Focus mode (Shift):
slows entire stage
allows precise dodging
Weapon cycling system
Collision-based damage handling

> Controls
Key	Actions:
← / →	                              Move
Shift	                              Focus mode (slow stage + precision)
Q / E	                              Switch weapons
1–6	                                Select weapons (loadout / in-game)
Enter	                              Start game
ESC	                                Return to menu
R	                                  Restart (Game Over)

> Design Highlights
Modular multi-file architecture
Clear separation of systems (player, enemies, weapons, effects, UI)
State-based flow (menu → loadout → gameplay)
Pattern-driven difficulty instead of randomness
Balanced chaos design using safe zones
Emphasis on game feel:
responsive feedback
readable visuals
smooth pacing

> Tech Stack
Python 3
Pygame

> Future Improvements (maybe)
Sound effects and background music
Expanded enemy variety
Weapon upgrade / progression system
High score tracking
Additional boss patterns and phases

> Inspiration
Arcade shooters
Bullet-hell design principles
Pattern-based gameplay systems
Iterative prototyping approach

> Author
Arnav Srivastava
Manipal University Jaipur, Jaipur
1st Year (at the time of writing this)
