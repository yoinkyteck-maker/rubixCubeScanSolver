import kociemba

def convertColorToKociemba(CubeString : str):
    convertList = {'Y':'U','G':'F','R':'L','B':'B','O':'R','W':'D'}
    return "".join([convertList[i] for i in CubeString])

def solve_cube(cubestring):
    if len(cubestring) != 54:
        return "Cube string must be 54 characters."
    if any(cubestring.count(c) != 9 for c in "URFDLB"):
        return "Each color must appear exactly 9 times."
    
    try:
        solution = kociemba.solve(cubestring)
    except ValueError as e:
        print(f"Invalid cube: {e}")
        return None
    except Exception as e:
        print(f"Solver failed: {e}")
        return None
    
    return solution

"""
cube is represented by

             |************|
             |*U1**U2**U3*|
             |************|
             |*U4**U5**U6*|
             |************|
             |*U7**U8**U9*|
             |************|
 ************|************|************|************
 *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*
 ************|************|************|************
 *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
 ************|************|************|************
 *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
 ************|************|************|************
             |************|
             |*D1**D2**D3*|
             |************|
             |*D4**D5**D6*|
             |************|
             |*D7**D8**D9*|
             |************|


    "UUUUUUUUU"
    "RRRRRRRRR"
    "FFFFFFFFF"
    "DDDDDDDDD"
    "LLLLLLLLL"
    "BBBBBBBBB"
"""

