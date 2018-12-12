import os
import numpy as np
_default_path = '/Users/jgreco/Dropbox/drop-data/hsc-pointings'

def load_hsc_pointings(path=_default_path, band='i', full=False):
    """
    Return the current HSC wide pointings in
    the given band.
    """
    from astropy.table import Table
    fn = 'FullWidePointings.lst' if full else 'ObservedWidePointings.lst'  
    fn = os.path.join(path, fn)
    ra = []
    dec = []
    if full:
        ra, dec = np.loadtxt(fn, delimiter='|', usecols=(1,2), unpack=True)
    else:
        with open(fn) as file:
            for line in iter(file):
                data = line.split('|')
                if data[1][-1]==band:
                    ra.append(float(data[2]))
                    dec.append(float(data[3]))
    coords = Table([ra, dec], names=['ra', 'dec'])
    return coords
