from PIL import Image
import cv2 as cv
import numpy as np
from skimage.measure import block_reduce
from torchvision.transforms import Resize

import explainer.util.hooks as hooks


def resize_map(map, target_shape):
    """
    Resize a map to a target shape
    """

    img = Image.fromarray(map)
    img = Resize(target_shape)(img)
    return np.array(img)


def pool(fn, x, size=2):
    return block_reduce(x, (size, size), fn)


def blur_filter(x, size=5, use_gaussian_kernel=False):
    return (
        cv.GaussianBlur(x, (size, size), 0)
        if use_gaussian_kernel
        else cv.blur(x, (size, size))
    )


def preprocces_lrp(
    lrp_map: np.ndarray,
    num_downscalings=4,
    downscaling_factor=2,
    reduction_function=np.sum,
    num_smoothing_iterations_per_downscale=2,
    smoothing_kernel_size=5,
    use_gaussian_kernel=True,
) -> np.ndarray:
    MIN_ALLOWED_RESOLUTION = 32

    orig_shape = lrp_map.shape

    for _ in range(num_downscalings):
        if lrp_map.shape[0] > MIN_ALLOWED_RESOLUTION:
            lrp_map = pool(reduction_function, lrp_map, size=downscaling_factor)

        for _ in range(num_smoothing_iterations_per_downscale):
            lrp_map = blur_filter(
                lrp_map,
                size=smoothing_kernel_size,
                use_gaussian_kernel=use_gaussian_kernel,
            )

    lrp_map = resize_map(lrp_map, orig_shape)

    hooks.debug("preprocessed_lrp_xai_map", lrp_map)

    return lrp_map
