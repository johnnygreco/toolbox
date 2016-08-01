import numpy as np

def match_coordinates(matchcoord, catcoord, maxsep, sep_units='arcsec', return_seps=False):
    """
    Match catalogs given ra and dec in degrees. This function 
    is essetially a wrapper for astropy's match_coordinates_sky, 
    but I've modified the return values.
    
    Parameters
    ----------
    matchcoord : BaseCoordinateFrame or SkyCoord (see astropy)
        The coordinate(s) to match to the catalog.
    catcoord : BaseCoordinateFrame or SkyCoord
        The base catalog in which to search for matches. 
    maxsep : float
        The maximum angular separation for which objects are 
        considered to be the same.
    sep_units : string, optional, default = 'arcsec'
        Units of maxsep. (arcsec, degree, or radian)
    return_seps : bool, optional, default = False
        If True, return the angular separations between the
        matched objects in the catalogs.

    Returns
    -------
    mask :  ndarray, shape is the same as matchcoord
        Mask for matchcoord, which gives the matches to catcoord.
    idx : ndarray, shape matches matchcoord
        Indices for catcoord, which give the matches to matchcoord.
    sep2d : ndarray, optional
        The angular separations between the matches in units
        given by sep_units.
    """
    from astropy.coordinates import match_coordinates_sky
    convert = {'degree':1.0, 'arcsec':1./3600.0, 'radian':180.0/np.pi}
    idx, sep2d, sep3d = match_coordinates_sky(matchcoord, catcoord, nthneighbor=1)
    mask = sep2d.value < (maxsep*convert[sep_units])
    idx = idx[mask]
    sep2d = sep2d.value[mask]/convert[sep_units]
    return (mask, idx) if not return_seps else (mask, idx, sep2d)

def crossmatch(table_1, table_2, maxsep, sep_units='arcsec', return_seps=False):
    """
    Build astropy SkyCoord objects given two tables with ra and dec columns 
    and match them using astropy's match_coordinates_sky function.

    Parameters
    ----------
    table_1 : numpy array with named columns (astropy Table)
        A Table with the first catalogs ra and dec.
    table_2 : numpy array with named columns (astropy Table)
        A Table with the second catalogs ra and dec.
    maxsep : float
        The maximum angular separation for which objects are 
        considered to be the same.
    sep_units : string, optional, default = 'arcsec'
        Units of maxsep. (arcsec, degree, or radian)
    return_seps : bool, optional, default = False
        If True, return the angular separations between the
        matched objects in the catalogs.
        
    Returns
    -------
    matched_1 : numpy array with named columns (astropy Table)
        Matched first catalog.
    matched_2 : numpy array with named columns (astropy Table)
        Matched second catalog.

    Note: The shapes of matched_1 and matched_2 are the same and the 
    objects are (within the maxsep threshold) the same.
    """
    from astropy.coordinates import SkyCoord

    cats = []
    for tab in [table_1, table_2]:
        cats.append(SkyCoord(tab['ra'], tab['dec'], frame='icrs', unit='deg'))
    mask, idx, sep2d = match_coordinates(cats[0], cats[1], maxsep, sep_units, True)
    return (table_1[mask], table_2[idx], sep2d) if return_seps else (table_1[mask], table_2[idx])
