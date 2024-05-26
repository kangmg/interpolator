LICENSE = """
This code script governed by the terms of the license below.

code source url : https://github.com/charnley/rmsd

----------------------------------------------------------------------------

Copyright (c) 2013, Jimmy Charnley Kromann <jimmy@charnley.dk> & Lars Bratholm
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
----------------------------------------------------------------------------
"""

import numpy as np
from numpy import ndarray
from typing import List, Tuple, Union
import re


ELEMENT_NAMES = {
    1: "H",
    2: "He",
    3: "Li",
    4: "Be",
    5: "B",
    6: "C",
    7: "N",
    8: "O",
    9: "F",
    10: "Ne",
    11: "Na",
    12: "Mg",
    13: "Al",
    14: "Si",
    15: "P",
    16: "S",
    17: "Cl",
    18: "Ar",
    19: "K",
    20: "Ca",
    30: "Zn",
    31: "Ga",
    32: "Ge",
    33: "As",
    34: "Se",
    35: "Br",
    36: "Kr",
    37: "Rb",
    38: "Sr",
    50: "Sn",
    51: "Sb",
    52: "Te",
    53: "I",
}

NAMES_ELEMENT = {value: key for key, value in ELEMENT_NAMES.items()}



def str_atom(atom: int) -> str:
    """
    Convert atom type from integer to string

    Parameters
    ----------
    atoms : string

    Returns
    -------
    atoms : integer

    """
    return ELEMENT_NAMES[atom]


def int_atom(atom: str) -> int:
    """
    Convert atom type from string to integer

    Parameters
    ----------
    atoms : string

    Returns
    -------
    atoms : integer
    """

    atom = atom.capitalize().strip()
    return NAMES_ELEMENT[atom]

def centroid(X: ndarray) -> ndarray:
    """
    Centroid is the mean position of all the points in all of the coordinate
    directions, from a vectorset X.

    https://en.wikipedia.org/wiki/Centroid

    C = sum(X)/len(X)

    Parameters
    ----------
    X : array
        (N,D) matrix, where N is points and D is dimension.

    Returns
    -------
    C : ndarray
        centroid
    """
    C: ndarray = X.mean(axis=0)
    return C


def get_coordinates_xyz_lines(
    lines: List[str], return_atoms_as_int: bool = False
) -> Tuple[ndarray, ndarray]:

    V: Union[List[ndarray], ndarray] = list()
    atoms: Union[List[str], ndarray] = list()
    n_atoms = 0

    assert isinstance(V, list)
    assert isinstance(atoms, list)

    # Read the first line to obtain the number of atoms to read
    try:
        n_atoms = int(lines[0])
    except ValueError:
        exit("error: Could not obtain the number of atoms in the .xyz file.")

    # Skip the title line
    # Use the number of atoms to not read beyond the end of a file
    for lines_read, line in enumerate(lines[2:]):

        line = line.strip()

        if lines_read == n_atoms:
            break

        values = line.split()

        if len(values) < 4:
            atom = re.findall(r"[a-zA-Z]+", line)[0]
            atom = atom.upper()
            numbers = re.findall(r"[-]?\d+\.\d*(?:[Ee][-\+]\d+)?", line)
            numbers = [float(number) for number in numbers]
        else:
            atom = values[0]
            numbers = [float(number) for number in values[1:]]

        # The numbers are not valid unless we obtain exacly three
        if len(numbers) >= 3:
            V.append(np.array(numbers)[:3])
            atoms.append(atom)
        else:
            msg = (
                f"Reading the .xyz file failed in line {lines_read + 2}."
                "Please check the format."
            )
            exit(msg)

    try:
        # I've seen examples where XYZ are written with integer atoms types
        atoms_ = [int(atom) for atom in atoms]
        atoms = [str_atom(atom) for atom in atoms_]

    except ValueError:
        # Correct atom spelling
        atoms = [atom.capitalize() for atom in atoms]

    if return_atoms_as_int:
        atoms_ = [int_atom(atom) for atom in atoms]
        atoms = np.array(atoms_)
    else:
        atoms = np.array(atoms)

    V = np.array(V)

    return atoms, V


def get_coordinates_xyz_from_string(xyz_string, return_atoms_as_int=False):
    """
    get_coordinates_xyz from xyz string
    """
    lines = xyz_string.splitlines()

    atoms, V = get_coordinates_xyz_lines(lines, return_atoms_as_int=return_atoms_as_int)

    return atoms, V