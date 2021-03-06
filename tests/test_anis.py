from fidimag.atomistic import Anisotropy
from fidimag.common import CuboidMesh
from fidimag.atomistic import Sim
import numpy as np


def test_anis():
    mesh = CuboidMesh(nx=5, ny=3, nz=2)
    spin = np.zeros(90)
    anis = Anisotropy(Ku=1, axis=[1, 0, 0])
    mu_s = np.ones(90)
    anis.setup(mesh, spin, mu_s)
    field = anis.compute_field()
    assert len(mesh.coordinates) == 5 * 3 * 2
    assert np.max(field) == 0
    spin[0] = 99
    field = anis.compute_field()
    assert field[0] == 2 * 99


if __name__ == '__main__':
    test_anis()
