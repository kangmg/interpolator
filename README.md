<a target="_blank" href="https://colab.research.google.com/github/kangmg/interpolator/blob/main/notebooks/usage_tutorial.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## interpolator
Linear interpolator for xyz format strings

## Usage

```python
from interpolator import interpolations, interpolate

xyz_1 = """ 6

  C -1.469988 0.536776 0.005252
  Br 0.903269 0.545886 -0.004619
  H -1.591701 0.607720 1.082741
  H -1.593960 -0.412748 -0.508430
  H -1.585688 1.436191 -0.571323
  Cl -4.127302 0.571417 -0.003556"""

xyz_2 = """ 6

  C -1.277168 0.545365 -0.000063
  Br 0.648058 0.543727 0.000199
  H -1.652166 0.593222 1.017641
  H -1.652215 -0.359651 -0.467952
  H -1.651698 1.403205 -0.550042
  Cl -4.402752 0.572053 0.000227"""

mid_xyz = interpolate(xyz_1, xyz_2, t=0.5)
print(mid_xyz)

traj = interpolations(xyz_1, xyz_2, num_images=10, get_single_string=True)
print(traj)
```
