#!/usr/bin/env python 

import numpy as np
from ..astro import angsep
from ..utils import isiterable, vectorize_if_needed
from scipy.integrate import quad
WMAP9 = [0.693, 0.287, 1.0-0.287]

class Cosmology:
    """
    Class for calculating common cosmological quantities
    """
    def __init__(self, params=WMAP9):
        self.h, self.omegaM0, self.omegaL0 = params
        self.H0 = 100.0*self.h # km/s/Mpc
        self.c = 2.99792458e5 # km/s
        self.G = 4.302113488372941e-09 # km2 Mpc / (M_sun s2)
        self.DH = self.c/self.H0

    def E(self, z):
        """
        the ratio of the Hubble parameter at redshift z to
        its present value
        """
        if isiterable(z):
            z = np.asarray(z)
        return np.sqrt(self.omegaM0*(1.0+z)**3 + self.omegaL0)

    def rhocrit(self, z):
        """
        critical density in units of Msun Mpc^-3
        """
        if isiterable(z):
            z = np.asarray(z)
        return (3.0*(self.H0*self.E(z))**2)/(8*np.pi*self.G) 

    def com_dist(self, z):
        """
        comoving distance as a function of z
        """
        func = lambda z: quad(lambda z : 1.0/self.E(z), 0, z)[0]
        return self.DH*vectorize_if_needed(func, z)

    def D_L(self, z):
        """
        angular diameter distance as a function of z
        """
        if isiterable(z):
            z = np.asarray(z)
        return self.com_dist(z)*(1.0 + z)

    def D_A(self, z):
        """
        angular diameter distance as a function of z
        """
        if isiterable(z):
            z = np.asarray(z)
        return self.com_dist(z) / (1.0 + z)

    def com_sep(self, coord3d_1, coord3d_2):
        """
        comoving separation between two galaxies 
        """
        for i in range(3):
            if isiterable(coord3d_1[i]):
                coord3d_1[i] = np.asarray(coord3d_1[i])
            if isiterable(coord3d_2[i]):
                coord3d_2[i] = np.asarray(coord3d_2[i])
        ra1, dec1, z1 = coord3d_1
        ra2, dec2, z2 = coord3d_2
        Dc1 = self.com_dist(z1)
        Dc2 = self.com_dist(z2)
        theta = angsep(ra1, dec1, ra2, dec2)
        sep = np.sqrt(Dc1**2 + Dc2**2 - 2.0*Dc1*Dc2*np.cos(theta))
        return sep 
