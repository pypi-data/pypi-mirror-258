import numpy as np
import PIL.Image
import torch
from explainer.models.base import VisionModel, XAI_Map


__all__ = ["explanation_score"]


def explanation_score(
        xai_map:XAI_Map,
        image:PIL.Image,
        model:VisionModel,
        iterations:int = 50
        ) -> float:
    """
    Calculates a score for a XAI Map.
    Score is based on the AOPC score. Creates a series of pertubations of the image where an increasing number of pixels are replaced with noise.
    Pixels are removed by descending order of relevance in the explanation.
    The score is the biggest amount of original pixels for which the image was miss-classified, as a ratio of all pixels.
    Score relies on randomization. Result is the average of several calculations.

    Parameters
    ----------
    xai_map:XAI_Map
        the XAI Map to be scored
    image:PIL.Image
        the image for which the XAI Map was created
    model:VisionModel
        the model which the XAI Map explains
    iterations:int
        number of iterations, default = 50

    Returns
    -------
    float
        explanation score
    """
    
    explanation:np.ndarray = xai_map.map
    prediction:int = xai_map.predicted_label
    image:np.ndarray = np.array(image.resize(explanation.shape))

    score_sum = 0

    for i in range(iterations):
        score_sum += _score(image, explanation, model, prediction)

    return score_sum/iterations
    

def _score(image: np.ndarray, explanation:np.ndarray, obj_model:VisionModel, prediction: int, stride:float = 0.1, iterations:int = 5) -> float:
    """
    Determines how many pixels of the image can be replaced with noise without changing the model output.
    Pixels are replaced in order of descending relevance.
    Search starts with a linear search with given stride, then proceeds with a binary search.
    Uses randomization. Calling this function several times will lead to different results.
    
    Parameters
    ----------
    image:np.ndarray
        the image
    explanation:np.ndarray
        expanation for the image and model
    obj_model:VisionModel
        the model
    prediction:int
        predicted class
    stride:float
        stride for the linear search, default = 0.1
    iterations:int
        number of iterations for the binary search, default = 5

    Returns
    -------
        number of replaced pixels as a ratio of all pixels
    """

    h = image.shape[0]
    w = image.shape[1]

    # generate noise
    max_value = np.max(image)
    min_value = np.min(image)
    noise = np.random.rand(h,w,3)
    noise = noise * (max_value - min_value) + min_value

    selection_noise = np.random.rand(h,w) * 0.5

    upper = 1
    lower = upper - stride

    while lower > 0:
        result = _pertubation_step(image, explanation, obj_model, lower, noise, selection_noise, h, w)
        if prediction not in result:
            # print(f"First Phase, upper={upper} lower={lower}, BREAK")
            break
        upper = lower
        lower -= stride
        # print(f"First Phase, upper={upper} lower={lower}, CONTINUE")

    lower = max(0,lower)
    
    for i in range(iterations):
        q = (upper+lower)/2
        result = _pertubation_step(image, explanation, obj_model, q, noise, selection_noise, h, w)
        if prediction in result:
            # print(f"Second Phase, upper={upper} q={q} lower={lower}, LOWER")
            upper = q
        else:
            # print(f"Second Phase, upper={upper} q={q} lower={lower}, UPPER")
            lower = q
    
    return (upper+lower)/2



def _pertubation_step(image: np.ndarray, explanation:np.ndarray, obj_model:VisionModel, q, noise:np.ndarray, selection_noise:np.ndarray, h:int, w:int, precision:int = 5):
    """
    Calculates a pertubation and returns the model output

    Parameters
    ----------
    image:np.ndarray
        the image on which the pertubation is based
    explanation:np.ndarray
        expanation for the image and model
    obj_model:VisionModel
        the model
    q:float
        Pixels which lie above the q-th quantile are replaced with noise in the pertubation
    noise:np.ndarray
        values with which pixels are replaced
    selection_noise:np.ndarray
        controls which pixels are replaced if several have the same value
    h:int
        height
    w:int
        width
    precision:int
        how close the actual number of replaced pixels is compared to a perfect split. Default=5

    Returns
    -------
        model output
    """

    remove = _select_by_quantile(explanation, q, selection_noise, h, w, precision)

    remove = remove.reshape((h,w,1))
    remove = remove.repeat(3,2)

    keep = np.bitwise_not(remove)

    p1 = image * keep
    p2 = noise * remove
    pertubation = np.add(p1,p2)

    pertubation = pertubation.astype(np.uint8)

    result = obj_model.predict(PIL.Image.fromarray(pertubation))
    
    return result

def _select_by_quantile(arr: np.ndarray, q:float, noise: np.ndarray, h:int, w:int, precision:int = 5) -> np.ndarray:
    """
    Selects pixels which are larger than the given quantile.
    Tries to always select (1-q) * h * w pixels. If several pixels have the same value, uses noise to choose.

    Parameters
    ----------
    arr:np.ndarray
        array from which pixels are choosen
    q:float
        quantile
    noise:np.ndarray
        determines which pixels are choosen if several have the same value
    h:int
        height
    w:int
        width
    precision:int
        controls how big the distance between the perfect number of selected pixels and the actual number may be. Default = 5

    Returns
    -------
    np.ndarray
        selection
    """


    target_amount = round((1-q) * h * w)

    q_value = np.quantile(arr, q)
    selection_small = np.greater(arr, q_value)

    selected_amount = np.count_nonzero(selection_small)

    if abs(target_amount - selected_amount) > precision:        
        selection_big = np.greater_equal(arr, q_value)

        selection_combined = selection_small + selection_big + noise
        q_value = np.quantile(selection_combined, q)
        selection = np.greater(selection_combined, q_value)

        return selection
    else:
        return selection_small
