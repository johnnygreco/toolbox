
__all__ = ['ds9view']

def ds9view(fitsfile, regfile=None, width=750, height=750, mecube=False):
    """
    View image with our without regions in ds9.

    Parameters
    ----------
    fitsfile : string
        Fits file of image
    regfile : string, optional
        ds9 regions file. If None, no regions will be drawn.
    width : float, optional
        Width of window
    height : float, optional
        height of window
    mecube : bool, optional
        If True, open file as multiple extension cube. 
    """
    import pyds9

    ds9 = pyds9.DS9(start='-view layout vertical '+\
                          '-width '+str(width)+' '+\
                          '-height '+str(height)+' '+\
                          '-scale zscale '+\
                          '-wcs skyformat degrees '+\
                          '-cmap invert yes ')

    cmd = 'file mecube '+fitsfile if mecube else 'file '+fitsfile
    ds9.set(cmd)

    if regfile is not None:
        ds9.set('regions load '+regfile)

    ds9.set('zoom to fit')
