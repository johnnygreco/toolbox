
__all__ = ['draw_ellipse', 'line_widths']

def draw_ellipse(mu, C, scales=[1, 2, 3], ax=None, **kwargs):
    """
    Taken from astroML.plotting.tools: 
    https://github.com/astroML/astroML
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse

    if ax is None:
        ax = plt.gca()

    # find principal components and rotation angle of ellipse
    sigma_x2 = C[0, 0]
    sigma_y2 = C[1, 1]
    sigma_xy = C[0, 1]

    alpha = 0.5 * np.arctan2(2 * sigma_xy,
                             (sigma_x2 - sigma_y2))
    tmp1 = 0.5 * (sigma_x2 + sigma_y2)
    tmp2 = np.sqrt(0.25 * (sigma_x2 - sigma_y2) ** 2 + sigma_xy ** 2)

    sigma1 = np.sqrt(tmp1 + tmp2)
    sigma2 = np.sqrt(tmp1 - tmp2)

    for scale in scales:
        ax.add_patch(Ellipse((mu[0], mu[1]),
                             2 * scale * sigma1, 2 * scale * sigma2,
                             alpha * 180. / np.pi,
                             **kwargs))
def line_widths(lw):
    """
    Set major/minor ticks and axies line widths.
    """
    import matplotlib.pyplot as plt
    plt.rc('axes', linewidth=lw)
    plt.rc('ytick.major', width=lw)
    plt.rc('ytick.major', width=lw)
    plt.rc('xtick.major', width=lw)
