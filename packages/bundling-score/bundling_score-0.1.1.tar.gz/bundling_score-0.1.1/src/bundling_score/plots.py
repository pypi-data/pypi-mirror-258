"""Provides tools to do plots, useful for testing.

Ghislain de Labbey
Last updated May 12th 2023
"""

import numpy as np
import matplotlib.pyplot as plt
import bundling_score.bundling_score as bs
from scipy.linalg import norm


def orientation_from_q(qs):
    ''' Get orientation from nematic tensor'''
    nY, nX = qs.shape[:2]
    u = np.zeros((nX, nY, 2))
    rr, cc = np.nonzero(norm(qs, axis=(2, 3)))

    u[rr, cc, 0] = np.sqrt(qs[rr, cc, 0, 0] + 1 / 2)
    u[rr, cc, 1] = np.sqrt(qs[rr, cc, 1, 1] + 1 / 2)

    rr, cc = np.nonzero(qs[..., 0, 1])
    u[rr, cc, 1] *= np.sign(qs[rr, cc, 0, 1])
    return u


def show_steps(image, smax=100):
    ''' Show all the different calculation steps. '''
    nY, nX = image.shape
    xx = np.array(range(nX))
    yy = np.array(range(nY))
    X, Y = np.meshgrid(xx, yy)

    grad = bs.get_gradient(image)
    qs, Qs = bs.get_nematic_tensor(image)
    u = orientation_from_q(qs)
    corr = bs.compute_correlations(Qs, smax)

    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(16, 9))
    ax = ax.ravel()
    ax[0].imshow(image, cmap='magma')
    ax[0].set_title('Original')

    ax[1].imshow(grad[..., 1], cmap='magma')
    ax[1].set_title('x-gradient')

    ax[2].imshow(grad[..., 0], cmap='magma')
    ax[2].set_title('y-gradient')

    ax[3].imshow(image)
    ax[3].quiver(X,
                 Y,
                 grad[..., 1],
                 grad[..., 0],
                 angles='xy',
                 scale_units='xy')
    ax[3].set_title('Arrow-gradient')

    ax[4].imshow(image)
    ax[4].quiver(X,
                 Y,
                 image * u[..., 1],
                 image * u[..., 0],
                 angles='xy',
                 linewidth=8,
                 scale_units='xy')
    ax[4].set_title('Arrow-polar vector')

    nem = ax[5].imshow(corr)

    ax[5].set_title('Nematic correlations')
    fig.colorbar(nem)


def show_direction(image, axes=None):
    ''' Show the direction on top of the image. '''
    nY, nX = image.shape
    xx = np.array(range(nX))
    yy = np.array(range(nY))
    X, Y = np.meshgrid(xx, yy)

    qs, _ = bs.get_nematic_tensor(image)
    u = orientation_from_q(qs)
    axes.imshow(image)
    axes.quiver(X,
                Y,
                u[..., 0],
                u[..., 1],
                u='xy',
                scale_units='xy')
