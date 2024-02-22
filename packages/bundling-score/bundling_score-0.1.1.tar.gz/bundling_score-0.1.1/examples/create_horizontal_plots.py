''' Several simple examples of images and bundling scores '''

import matplotlib.pyplot as plt
import numpy as np

import bundling_score.bundling_score as bs
import bundling_score.plots as bp

from skimage.filters import gaussian
from scipy.linalg import norm

plt.ion()
plt.close('all')

# Size of the image
N = 7
# Limit value for rx and ry, avoids padding
smax = 20
# Simple line
image = np.zeros((N, N))
image[N//2, :] = 1
image = gaussian(image, .5)

qs, Qs = bs.get_nematic_tensor(image)
grad = bs.get_gradient(image)
norm_grad = norm(grad, axis=2)
rr, cc = np.nonzero(norm_grad)
grad[rr, cc, :] /= norm_grad[rr, cc, None]
u = bp.orientation_from_q(qs)

nY, nX = image.shape
xx = np.array(range(nX))
yy = np.array(range(nY))
X, Y = np.meshgrid(xx, yy)

plt.subplot(121)
plt.imshow(image, cmap='gray')
plt.quiver(X,
           Y,
           grad[..., 1],
           grad[..., 0],
           angles='xy',
           width=.02,
           scale=1,
           scale_units='xy', color='tab:blue')

plt.subplot(122)
plt.imshow(image, cmap='gray')
plt.quiver(X,
           Y,
           u[..., 1],
           u[..., 0],
           angles='xy',
           width=.02,
           scale=1,
           scale_units='xy', color='tab:orange')
plt.show()
