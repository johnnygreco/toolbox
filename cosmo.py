#!/usr/bin/env python 

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

class Cosmology:
    """
    Class for calculating common cosmological quantities
    """

    def __init__(self, h, omegaM0, omegaL0):
        self.h = h
        self.H0 = 100.0*h # km/s/Mpc
        self.omegaM0 = omegaM0
        self.omegaL0 = omegaL0
        self.c = 2.99792458e5 # km/s
        self.G = 4.302113488372941e-09 # km2 Mpc / (M_sun s2)
        self.DH = self.c/self.H0

    def E(self, z):
        """
        the ratio of the Hubble parameter at redshift z to
        its present value
        """
        return np.sqrt(self.omegaM0*(1.0+z)**3 + self.omegaL0)

    def invE(self, z):
        """
        inverse of above ratio
        """
        return 1.0/np.sqrt(self.omegaM0*(1.0+z)**3 + self.omegaL0)

    def rhocrit(self, z):
        """
        critical density in units of Msun Mpc^-3
        """
        return (3.0*(self.H0*self.E(z))**2)/(8*np.pi*self.G) 

    def com_dist(self, z):
        """
        comoving distance as a function of z
        """
        return self.DH*quad(lambda z : 1.0/self.E(z), 0, z)[0]

    def D_L(self, z):
        """
        angular diameter distance as a function of z
        """
        return self.com_dist(z)*(1.0 + z)

    def D_A(self, z):
        """
        angular diameter distance as a function of z
        """
        return self.com_dist(z) / (1.0 + z)

    def ang_size(self, z, size):
        """
        angular size on the sky as a function of redshift
        """
        DA = self.AngDiamDist(z)
        return np.arctan(size / DA)

    def com_sep(self, ra1, dec1, z1, ra2, dec2, z2):
        """
        comoving separation between two galaxies 
        """
        from tools import angsep
        Dc1 = self.com_dist(z1)
        Dc2 = self.com_dist(z2)
        theta = angsep(ra1, dec1, ra2, dec2)
        sep = np.sqrt(Dc1**2 + Dc2**2 - 2.0*Dc1*Dc2*np.cos(theta))
        return sep 
