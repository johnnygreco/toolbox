from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

__all__ = ['cutout_grid']

def cutout_grid(cat, max_cols=5, cutout_radius=20, butler=None, skymap=None,
                fig_size_scale=10, **kwargs):
    """
    Show sources in grid using matplotlib.

    Parameters
    ----------
    cat : ndarray with shape (num_sources, 2)
        catalog of ra and dec in degrees
        
    """
    import lsstutils

    if skymap is None:
        from .utils import get_skymap
        butler, skymap = get_skymap()

    num_sources = len(cat)
    if num_sources <= max_cols:
        rows, cols = 1, num_sources
        figsize = (fig_size_scale, fig_size_scale/num_sources)
    else:
        cols = max_cols
        rows = np.ceil(num_sources/float(max_cols)).astype(int)
        ratio = rows/cols if rows!=cols else 1.0
        if rows >= cols:
            figsize = (fig_size_scale, fig_size_scale*ratio)
        else:
            figsize = (fig_size_scale/ratio, fig_size_scale)

    subplot_kw = dict(xticks=[], yticks=[], aspect='equal')
    fig, axes = plt.subplots(
        rows, cols, figsize=figsize, subplot_kw=subplot_kw, **kwargs)

    for i, ax in enumerate(axes.flat):
        if i < num_sources:
            ra, dec = cat[i]
            rgb = lsstutils.make_rgb_image(ra, dec, cutout_radius, 
                                           butler=butler, skymap=skymap)
            ax.imshow(rgb, origin='lower')
        else:
            ax.set_axis_off()

    fig.tight_layout()

    return fig, axes
