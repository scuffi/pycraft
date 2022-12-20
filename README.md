
# PyCraft

PyCraft is a barebones Minecraft copy built in Ursina.

_PyCraft was tested on an i9-9900k & RTX 2080Ti and averaged 80-100FPS, performance may be unplayable on worse machines_




## Features

- Procedural terrain generation
- Placing & Breaking block mechanics
- Chunk based saving system
- Configurable blocks
- Event system, allowing easy expansion of the game without manipulating existing code


## Installation

PyCraft was built and tested in Python 3.10.8.
_Expected supported versions are 3.6+ (don't quote me)_

Clone the repository:
```bash
git clone https://github.com/scuffi/pycraft.git
```
Enter the repository directory:
```bash
cd pycraft
```
Install dependencies (Virtual Environment recommended):
```bash
pip install -r requirements.txt
```
Finally, run the game:
```bash
python main.py
```
    
## Configuration

The main configuration file is `settings.yml` in the main directory.
In this file you will find multiple different settings that correspond to the rendering, generation and configuration of the world, all these settings are documented in that file.


The default configuration file for custom blocks is `blocks.yml` in the main directory.
To configure custom blocks, you will need a texture. Ensure the texture is a square file, as it will wrap the block.

Blocks are configured as so:
```yml
Dirt:
  texture: dirt.png
  break_sound: dirt_break.ogg
  place_sound: dirt_place.ogg

Stone:
  texture: stone.png
  break_sound: stone.ogg
```
Where all 'assets' must be placed somewhere in the 'assets' folder in the main directory. The sound effects must either be `.ogg` or `.wav`.
All configured assets must be found, or else the program will not continue.


## Goals

#### Terrain generation

Create a system that can generate terrain based on Perlin noise

#### Procedural generation

Morph the terrain generation system to generate terrain around a player when they move around the map

#### Murdering old terrain

Morph the system again to remove terrain that is far away from a user

#### Placing & Breaking

Allow a user to place and break interactable blocks in the world

#### Sound effects

Add sound effects to placing and breaking blocks

#### Configurable blocks

Allow for blocks to be loaded from an external file, which documents block textures and names

#### Integration of configured blocks

Allow the user to place all of the configured blocks as they please


## Optimisations

- Non-collision map
> The map itself has no collisions for all visible entities, this increases performance as the program doesn't have to run physics simulations on anything except a small bounding box around the player.
- Configurable collision box
> The collision box as spoken about above allows to be a configured area, called 'reach' which dictates how far a player can 'reach' i.e. how far they can interact with.
- Procedural generation
> To allow for quick starting up of the game, we generate as we move into new chunks, this allows for us to have a seemingly infinite map. Only drawback is when loading brand new terrain, the game may slow down to load it.
- Kill old chunks
> To ensure that there are never too many entities on the screen, we remove any chunks from our render that are too far away. They still exist, but we take the strain off the engine by removing them from the scene.
- Store old chunks when not rendered
> Due to the fact we continue to store the unrendered chunks, when walking into new, but pregenerated terrain, we do not feel a large jump, as most processing has already been done.

Ontop of these optimisations, we also don't reperform any calculations on blocks or chunks that already exist. This is what the registry is for, as we can assure that if it exists in the registry, the calculations have already been completed, so we don't have to regenerate it, we assume the calculations have already been completed.


## UML Diagrams
These UML Diagrams are high level insights into how different aspects of the program operate. They will change slightly in comparison with the code, however, the whole journey will be roughly the same.

#### Main Flow:
This is the flow that starts the program:\
![Main Program](/umls/main-flow.png?raw=true "Main Code Flow")

#### Update loop:
This is the loop that get's executed every frame:\
![Update loop](/umls/update-loop-flow.png?raw=true "Update Loop Flow")

#### Generate Terrain:
This is the flow that will generate new terrain, and remove old terrain:\
![Terrain Generation](/umls/generate-terrain-flow.png?raw=true "Terrain Generation Flow")

#### Generate Bounding Box:
This is the flow that will generate the interactive bounding box around a player:\
![Bounding Box Generation](/umls/generate-boundings.png?raw=true "Bounding Box Generation Flow")

#### Place Block:
This is the flow that will place a block in the world:\
![Place Block](/umls/place-block-flow.png?raw=true "Place Block Flow")

#### Break Block:
This is the flow that will break a block in the world:\
![Break Block](/umls/break-block-flow.png?raw=true "Break Block Flow")

#### Change Selected:
This is the flow that will change the players current selected block:\
![Change Selected](/umls/change-selected-flow.png?raw=true "Change Selected Flow")
