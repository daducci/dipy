#! /usr/bin/env python

import nibabel as nib
import numpy as np
import argparse

from dipy.reconst.shm import sf_to_sh
from dipy.core.sphere import Sphere


def sh_estimate(sphere_file, directions_file, out_file,
                rank=4, smoothness=0.0):
    in_nifti = nib.load(sphere_file)
    refaff = in_nifti.get_affine()
    data = in_nifti.get_data()

    vertices = np.loadtxt(directions_file)
    sphere = Sphere(xyz=vertices)

    odf_sh = sf_to_sh(data, sphere, int(rank), "mrtrix", smoothness)

    sh_out = nib.Nifti1Image(odf_sh.astype(np.float32), refaff)
    nib.save(sh_out, out_file)


DESCRIPTION = 'Spherical harmonics (SH) estimation from a sampled '\
              'spherical function.'


def buildArgsParser():
    p = argparse.ArgumentParser(description=DESCRIPTION,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument(action='store', dest='sphere_file',
                   help='Input nifti file representing the spherical function\n'
                        'on N vertices.')
    p.add_argument(action='store', dest='directions_file',
                   help="""Sphere vertices in a text file (Nx3)
    x1 x2 x3
     ...
    xN yN zN""")
    p.add_argument(action='store', dest='out_file', help='Output nifti file.')
    p.add_argument('-n', '--order', action='store', dest='rank',
                   metavar='int', required=False, default=8,
                   help='Maximum SH order of estimation (default 8)')
    p.add_argument('-l', '--lambda', action='store', dest='smoothness',
                   metavar='float', required=False, default=0.006,
                   help='Laplace-Beltrami regularization (default 0.006)')
    return p


def main():
    parser = buildArgsParser()
    args = parser.parse_args()

    sphere_file = args.sphere_file
    directions_file = args.directions_file
    out_file = args.out_file
    rank = args.rank
    smoothness = args.smoothness

    sh_estimate(sphere_file, directions_file, out_file, rank, smoothness)


if __name__ == "__main__":
    main()
