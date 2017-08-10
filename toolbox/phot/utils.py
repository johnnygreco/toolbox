import os
import numpy as np
from astropy import units as u
from ..utils.misc import project_dir, isiterable

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
        assert z is not None, 'must give z or D_L'
        z = _make_array_if_needed(z)
        if cosmo is None:
            from astropy.cosmology import FlatLambdaCDM
            cosmo = FlatLambdaCDM(70.0, 0.3)
        D_L = cosmo.luminosity_distance(z)
    else:
        D_L = _make_array_if_needed(D_L)
    mag = _make_array_if_needed(mag)
    return mag - 5*np.log10(D_L.to('pc').value) + 5


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


def lnu_from_AB_mag(abs_mag):
    abs_mag = _make_array_if_needed(abs_mag)
    d = 10*u.pc
    return 4*np.pi*(d.to('cm'))**2*fnu_from_AB_mag(abs_mag)


def sfr_uv(Lnu):
    """
    Star formation rate in M_sun/yr from L_nu in UV. 
    Kennicutt, Jr., R. C. 1998, ARA&A, 36, 189
    """
    return 1.4e-28*(Lnu/(u.erg/u.s/u.Hz)).decompose()*u.Msun/u.yr


class Bell2003(object):
    """
    Estimate stellar masses using the using the mass-to-light ratio/color 
    relation derived from Bell et al. (2003).
    """

    def __init__(self):
        from astropy.io import ascii
        fn = os.path.join(project_dir, 'data/bell-table.txt')
        self.table = ascii.read(fn).to_pandas()
        self.table.set_index('Color', inplace=True)

    def mass_to_light(self, band, color_name, color):
        log_ml = self.table.loc[color_name, 'a'+band] +\
                 self.table.loc[color_name, 'b'+band]*color
        return (10.0**log_ml)*u.M_sun/u.L_sun

    def stellar_mass(self, band, color_name, color, abs_mag):
        color = _make_array_if_needed(color)
        abs_mag = _make_array_if_needed(abs_mag)
        lum = lum_solar_units(abs_mag, band)
        return lum*self.mass_to_light(band, color_name, color)


def _make_array_if_needed(p):
    return np.asarray(p) if isiterable(p) else p
