import numpy as np

# ── boundary models ───────────────────────────────────────────────────────────

def bowshock_jelinek(plane='xy', ang = [-np.pi/2, np.pi/2],  n_points=500):
    """
    Bow shock model from:
        Jelínek, K., Němeček, Z., & Šafránková, J. (2012).
        A new approach to magnetopause and bow shock positions.
        Journal of Geophysical Research: Space Physics, 117(A5).
        https://doi.org/10.1029/2011JA017159

    Conic-section fit: r = L / (1 + e*cos(theta))
    Parameters for average solar wind: L = 24.5 R_E, e = 1.17.
    Returns (x, rho) in GSE R_E, dayside only.
    """
    L, e = 24.5, 1.17
    theta = np.linspace(ang[0], ang[1], n_points)
    r = L / (1 + e * np.cos(theta))
    x = r * np.cos(theta)
    rho = r * np.sin(theta)          # cylindrical radial distance
    return x, rho if plane == 'xz' else rho


def magnetopause_lin(plane='xy', ang = [-np.pi/2, np.pi/2], n_points=500):
    """
    Magnetopause model from:
        Lin, R. L., Zhang, X. X., Liu, S. Q., Wang, Y. L., & Gong, J. C. (2010).
        A three-dimensional asymmetric magnetopause model.
        Journal of Geophysical Research: Space Physics, 115(A4).
        https://doi.org/10.1029/2009JA014235

    Simplified axisymmetric form with average solar wind parameters:
    r0 = 10.4 R_E, alpha = 0.58 (flaring parameter).
    Returns (x, rho) in GSE R_E, dayside only.
    """
    
    r0, alpha = 10.4, 0.58
    theta = np.linspace(ang[0], ang[1], n_points)
    r = r0 * (2 / (1 + np.cos(theta))) ** alpha
    x = r * np.cos(theta)
    rho = r * np.sin(theta)
    return x, rho
    
def add_bs_mp_model(ax, plane='xy', theta_range = (-np.pi / 2, np.pi / 2)):
    """
    Overlay approximate bow shock and magnetopause contours.

    Models (average solar wind conditions, Pd ≈ 2 nPa, Bz = 0):
      Bow shock    — Jelínek et al. (2012), simplified paraboloid
      Magnetopause — Shue et al. (1998), r0 = 10.22 R_E, α = 0.58

    In the Y-Z plane the boundaries are approximately circular.
    """
    theta = np.linspace(theta_range[0], theta_range[0])

    r_bs = 15.02 / (1 + 0.81 * np.cos(theta))
    xbs, ybs = r_bs * np.cos(theta), r_bs * np.sin(theta)

    r_mp = 10.22 / (1 + 0.58 * np.cos(theta))
    xmp, ymp = r_mp * np.cos(theta), r_mp * np.sin(theta)

    if plane == 'yz':
        ax.add_patch(plt.Circle((0, 0), 14.5, color='cyan',
                                fill=False, ls='--', lw=1.2,
                                label='Bow shock (model)'))
        ax.add_patch(plt.Circle((0, 0), 10.0, color='lime',
                                fill=False, ls='--', lw=1.2,
                                label='Magnetopause (model)'))
    else:
        ax.plot(xbs, ybs, 'c--', lw=1.2, label='Bow shock (model)')
        ax.plot(xmp, ymp, color='lime', ls='--', lw=1.2,
                label='Magnetopause (model)')    