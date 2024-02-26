from PIL import Image
from torch import Tensor

from explainer.datasets.base import ClassificationDataset

from ._api import register_dataset

__all__ = ["CustomCLIP"]


@register_dataset
class CustomCLIP(ClassificationDataset):
    def transform(img: Image.Image) -> Tensor:
        raise NotImplementedError

    #list of interesting classes for language model
    """
        'poles', 'utility poles', 'electricity poles', 'bollards', 'guardrails',
        'road', 'street', 'path', 'road lines', 'license plates', 'signs', 'road signs',
        'street signs', 'directional signs', 'warning signs', 'stop signs', 'pedestrian signs',
        'speed limit signs', 'chevron signs', 'chevrons', 'bus stop sign', 'bus stop',
        'markers', 'kilometre markers', 'hills', 'rolling hills', 'mountains', 'trees',
        'palm trees', 'grass', 'vegetation', 'landscape', 'dirt', 'soil', 'houses', 'buildings',
        'roofs', 'cars', 'vehicles', 'taxis', 'pedestrian', 'script', 'letters'
    """
    def classes():
        return [
            "car",
            "truck",
            "bus",
            "vehicle",

    	    "road",
            "side_walk",
            "cross_walk",
            "traffic_light",
            "sign",
            "light_pole",
            "barrier",

            "building",
            "stone",
            "house",
            "person",

            "vegetation",
            "tree",
            "sky",
            "soil",

            "text"
            
        ]

    def class_texts():
        return list(
            map(lambda x: f"an image of a {x.replace('_', ' ')}", CustomCLIP.classes())
        )
