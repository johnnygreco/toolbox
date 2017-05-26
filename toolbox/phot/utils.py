import numpy as np
from astropy import units as u
from ..utils.misc import isiterable

#B&M and http://www.ucolick.org/~cnaw/sun.html
M_sun = dict(
    U=5.61,
    B=5.48,
    V=4.83,
    R=4.42,
    I=4.08,
    J=3.64,
    H=3.32,
    K=3.28,
    u=6.75,
    g=5.33,
    r=4.67,
    i=4.48,
    z=4.42
)
BANDS = list(M_sun.keys())
mAB_0 = 48.6
# NUV_mag = -2.5 * log10(flux) + 20.08
# FUV_mag = -2.5 * log10(flux) + 18.82
galex_NUV_mAB_0 = 20.08
galex_FUV_mAB_0 = 18.82    


def absolute_magnitude(mag, z=None, D_L=None, cosmo=None):
    if D_L is None:
        assert z, 'must give z or D_L'
        z = _make_array_if_needed(z)
        if cosmo is None:
            from astropy.cosmology import FlatLambdaCDM
            cosmo = FlatLambdaCDM(70.0, 0.3)
        D_L = cosmo.luminosity_distance(z)
    else:
        D_L = _make_array_if_needed(D_L)
    mag = _make_array_if_needed(mag)
    return mag - 5*np.log10(D_L.to('pc')/u.pc) + 5


def lum_solar_units(abs_mag, band):
    """
    Luminosity in Solar units.
    """
    assert band in BANDS, 'band not in '+', '.join(BANDS)
    abs_mag = _make_array_if_needed(abs_mag)
    return 10**(0.4*(M_sun[band] - abs_mag))*u.L_sun


def fnu_from_AB_mag(mag):
    mag = _make_array_if_needed(mag)
    fnu = 10.**((mag + mAB_0)/(-2.5))
    return fnu*u.erg/u.s/u.Hz/u.cm**2


def Lnu_from_AB_mag(abs_mag):
    abs_mag = _make_array_if_needed(abs_mag)
    d = 10*u.pc
    return 4*np.pi*(d.to('cm'))**2*fnu_from_AB_mag(abs_mag)


def _make_array_if_needed(p):
    return np.asarray(p) if isiterable(p) else p
