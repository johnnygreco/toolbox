"""
SExtractor utilities
"""

from __future__ import print_function

__all__ = ['read_sexout', 'sexout_to_ds9reg']

def read_sexout(sexfile):
    """
    Read a sextractor output file using astropy.

    Parameters
    ----------
    sexfile : string
      SExtractor output file. If None, must pass the output

    Returns
    -------
    sexout : structured array
      Output of sextractor in a numpy structured array.
    """
    from astropy.table import Table
    sexout = Table.read(sexfile, format='ascii.sextractor')
    return sexout

def sexout_to_ds9reg(sexfile, color='green', tag='all', winparams=False,
                     outfile='same', drawmode='ellipse', textparam=None):
    """
    Write a ds9 region file from SExtractor output.

    Parameters
    ----------
    sexfile : string
      SExtractor output file. If None, must pass the output
      in the sexout parameter.
    color : string, optional 
      Region color (cyan, blue, magenta, red, green, 
      yellow, white, or black)
    tag : string, optional
      ds9 tag for all the regions
    winparams : bool, optional
        If True, use sextractor's windowed parameters.
    outfile : string, optional
        Output reg file name. If 'same', use sexfile names 
        with a .reg extension. 
    drawmode : string, optional
        Draw an 'ellipse' or 'point' for every object
    textparam : string, optional
        If not None, write this sextractor output parameter 
        next to each object in the catalog. 

    Notes
    -----
     i) Adapted from https://github.com/nhmc/Barak.git. 
    ii) The sextractor output file must contain X_IMAGE and 
        Y_IMAGE for drawmode=point, and for drawmode=ellipse, 
        it must also contain A_IMAGE, B_IMAGE, and THETA_IMAGE.
        The corresponding 'WIN' parameters are acceptable with 
        winparams set to True. 
    """
    assert (drawmode=='ellipse') or (drawmode=='point')

    sexout = read_sexout(sexfile)
    regions = ['global font="helvetica 10 normal" select=1 highlite=1 '
               'edit=0 move=1 delete=1 include=1 fixed=0 source']
    regions.append('image')

    fields = ['X_IMAGE', 'Y_IMAGE', 'A_IMAGE','B_IMAGE','THETA_IMAGE']
    if drawmode=='point':
        fields = fields[:2]
    if winparams:
        fields = [f.split('_')[0]+'WIN'+'_'+f.split('_')[1] for f in fields]
    if textparam is not None:
        textfmt = 'text={%s}'
        fields.append(textparam)
    else:
        textfmt = ''

    fmt = {'ellipse':'ellipse(%s %s %s %s %s) # '+textfmt+' color=%s tag={%s}',
           'point':'point(%s %s) # point=circle '+textfmt+' color=%s tag={%s}'}[drawmode]

    for row  in sexout[fields]:
        vals = list(row)
        vals.extend([color, tag])
        regions.append(fmt % tuple(vals))

    if outfile=='same':
        outfile = sexfile[:-4]+'.reg'

    print('writing to region file to', outfile)
    fh = open(outfile,'w')
    fh.write('\n'.join(regions))
    fh.close()
