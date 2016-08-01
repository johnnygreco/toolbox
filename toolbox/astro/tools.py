import numpy as np

def angsep(ra1, dec1, ra2, dec2, sepunits='arcsec'):
    """
    Return angular separation btwn points

    Inputs
    ------
    ra1 :  float or ndarray 
        Right ascension(s) of first point(s) (in degrees). The shape
        must be the same as dec1.
    dec1 : float or ndarray 
        Declination(s) of first point(s) (in degrees). The shape must
        be the same as ra1.
    ra2 :  float or ndarray 
        Right ascension(s) of second(s) point (in degrees). The shape
        must be the same as dec2.
    dec2 : float or ndarray 
        Declination(s) of second point(s) (in degrees). The shape must
        be the same as ra2.
    sepunits : string, optional, default = 'arcsec'
        Angular unit of the returned separation
        (radian, degree, arcsec, or arcmin)

    Returns
    -------
    sep : same type as input angles, angular separation between points

    Note
    ----
    This is function uses the Vincenty formula:
    https://en.wikipedia.org/wiki/Great-circle_distance.
    """
    deg2rad = np.pi/180.0

    ra1 = ra1*deg2rad
    dec1 = dec1*deg2rad
    ra2 = ra2*deg2rad
    dec2 = dec2*deg2rad

    sin_dRA = np.sin(ra2 - ra1)
    cos_dRA = np.cos(ra2 - ra1)
    sin_dec1 = np.sin(dec1)
    sin_dec2 = np.sin(dec2)
    cos_dec1 = np.cos(dec1)
    cos_dec2 = np.cos(dec2)

    num1 = cos_dec2*sin_dRA
    num2 = cos_dec1*sin_dec2 - sin_dec1*cos_dec2*cos_dRA
    denom = sin_dec1*sin_dec2 + cos_dec1*cos_dec2*cos_dRA
    sep = np.arctan2(np.sqrt(num1*num1 + num2*num2), denom)

    conversion = {'radian':1.0, 'arcsec':206264.806, 'arcmin':206264.806/60.0, 'degree':180./np.pi}
    sep *= conversion[sepunits]

    return sep
