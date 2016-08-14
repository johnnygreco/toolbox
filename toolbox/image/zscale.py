import numpy as np

def zscale(img, contrast=0.25, samples=1000):
    """
    Implement IRAF zscale algorithm; samples=1000 
    and contrast=0.25 are the IRAF defaults.

    Parameters
    ----------
    img : 2D ndarray
        Image to be scaled.
    contrast : float, optional
        Desired contrast
    samples : int, optional
        Number of samples to take from img

    Returns 
    -------
    z1 : float
        Max pixel value
    z2 : float
        Min pixel value

    Source
    ------ 
    http://hsca.ipmu.jp/hscsphinx/scripts/psfMosaic.html
    """
    ravel = img.ravel()
    if len(ravel) > samples:
        imsort = np.sort(np.random.choice(ravel, size=samples))
    else:
        imsort = np.sort(ravel)

    n = len(imsort)
    idx = np.arange(n)

    med = imsort[int(n/2)]
    w = 0.25
    i_lo, i_hi = int((0.5-w)*n), int((0.5+w)*n)
    p = np.polyfit(idx[i_lo:i_hi], imsort[i_lo:i_hi], 1)
    slope, intercept = p

    z1 = med - (slope/contrast)*(n/2-n*w)
    z2 = med + (slope/contrast)*(n/2-n*w)

    return z1, z2
