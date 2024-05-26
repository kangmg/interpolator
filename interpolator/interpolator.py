from .utils import centroid , get_coordinates_xyz_from_string # utilities
import copy
import numpy as np

def xyz_formatter(atom_symbols, coords):
  """
  Convert an array of coordinates to XYZ format string.

  Parameters
  ----------
  - atom_symbols(np.array) : array of atomic symbols
  - coords(np.array) : array of atomic coordinates

  Returns
  -------
  xyz format string(str)
  """
  num_atoms = len(atom_symbols)
  xyz_block = f"{num_atoms}\n"

  for idx, symbol in enumerate(atom_symbols):
    x, y, z = coords[idx]
    xyz_block += "\n{:<3} {:>9.5f} {:>9.5f} {:>9.5f}".format(symbol, x, y, z)
  
  return xyz_block


def interpolations(P_str: str, Q_str: str, num_images:int=15, get_single_string=False)->list[str] | str:
  '''
  Description
  -----------

  Parameters
  ----------
    - P_str(str) : xyz format string
    - Q_str(str) : xyz format string
    - num_images(int): number of images

  Returns
  -------
    
  '''
  P_atoms, P_coord = get_coordinates_xyz_from_string(P_str)
  Q_atoms, Q_coord = get_coordinates_xyz_from_string(Q_str)

  # atomic order check
  if not (P_atoms == Q_atoms).all():
    raise ValueError(f"Wrong atomic order between two xyz structures.")
  
  # Recenter to centroid
  P_cent = centroid(P_coord)
  Q_cent = centroid(Q_coord)
  P_coord -= P_cent
  Q_coord -= Q_cent

  # interpolation
  interpolated_images = np.linspace(P_coord, Q_coord, num_images)
  xyz_format_images = list(xyz_formatter(P_atoms, image) for image in interpolated_images)

  # return single traj string
  if get_single_string:
    traj_string = xyz_format_images[0]
    for xyz in xyz_format_images[1:]:
      traj_string += f"\n{xyz}"
    return traj_string
    
  return xyz_format_images


def interpolate(P_str: str, Q_str: str, t:float)->list[str]:
  '''
  Description
  -----------

  Parameters
  ----------
    - P_str(str) : xyz format string
    - Q_str(str) : xyz format string
    - t: Interpolation parameter, 0 <= t <= 1

  Returns
  -------
    
  '''
  P_atoms, P_coord = get_coordinates_xyz_from_string(P_str)
  Q_atoms, Q_coord = get_coordinates_xyz_from_string(Q_str)

  # atomic order check
  if not (P_atoms == Q_atoms).all():
    raise ValueError(f"Wrong atomic order between two xyz structures.")
  
  # Recenter to centroid
  P_cent = centroid(P_coord)
  Q_cent = centroid(Q_coord)
  P_coord -= P_cent
  Q_coord -= Q_cent

  # t range check
  if (t < 0) or (t > 1): raise ValueError(f"interpolation parameter(t) expected 0 <= t <= 1, but got {t}") 
  
  interploated = (1 - t) * P_coord + t * Q_coord

  xyz_block = xyz_formatter(P_atoms, interploated)

  return xyz_block
