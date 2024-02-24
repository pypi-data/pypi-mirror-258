![tests_badge](https://github.com/Jtachan/Rubik_sim/actions/workflows/unittests.yml/badge.svg)

# Rubik Sim

This project allows to simulate a 3x3 Rubik's cube and perform operations over it.

## ⚙️ Setup

**Requirements**

- Python 3.9 or higher

**Installation**

The package is installable via pip:

````shell
pip install rubik-sim
````

Alternatively, the 'develop' branch can be installed for the latest changes
```shell
pip install git+https://github.com/Jtachan/genetic_rubiks_solver.git@develop
```

## 🏃 Usage 

#### Initializing the cube

The package allows importing all the classes directly from the module. 

To initialize the cube, it is only needed the `RubiksCube` class.
This generates a fully solved cube. To obtain a random state using `scramble()` 

````python
from rubik_sim import RubiksCube

my_cube = RubiksCube()  # Solved cube
my_cube.scramble()  # Updates the cube by 25 random moves
````

The number of moves to scramble the cube can also be specified as a parameter:
<br/>`RubiksCube.scramble(nof_moves: int = 25)`

It is also possible to initialize any cube from a string of characters defining the color of each tile.

````python
my_cube = RubiksCube.from_color_code(
    'BBBBBBBBBGGGGGGGGGOOOOOOOOOYYYYYYYYYRRRRRRRRRWWWWWWWWW'
)
````

The only supported colors are green ('G'), orange ('O'), yellow ('Y'), red ('R'), white ('W') and blue ('B').

#### Representation

The cube's state can be represented by calling `print()`

```pycon
>>> print(my_cube)
             ['B' 'B' 'B']
             ['B' 'B' 'B']
             ['B' 'B' 'B']
['G' 'G' 'G']['O' 'O' 'O']['Y' 'Y' 'Y']['R' 'R' 'R']
['G' 'G' 'G']['O' 'O' 'O']['Y' 'Y' 'Y']['R' 'R' 'R']
['G' 'G' 'G']['O' 'O' 'O']['Y' 'Y' 'Y']['R' 'R' 'R']
             ['W' 'W' 'W']
             ['W' 'W' 'W']
             ['W' 'W' 'W']
```

From the representation, the faces are:

- Blue = Top (up) face 
- Green = Left face 
- Orange = Front face 
- Yellow = Right face 
- Red = Back face 
- White = Bottom (down) face 

#### Rotating the cube

`RubiksCube.perform_operations(operations: Sequence[NOTATION_MOVES])`

This method updates the current state of the cube by performing operations over it.
The supported operations are:
> U, U', U2, D, D', D2, R, R', R2, L, L', L2, F, F', F2, B, B', B2,
> M, M', M2, E, E', E2, S, S' and S2.
 
These are the general notations for the possible moves on the cube.
More about the Rubik's cube notation: https://ruwix.com/the-rubiks-cube/notation/

Any missing notation can be performed with the current notations.
