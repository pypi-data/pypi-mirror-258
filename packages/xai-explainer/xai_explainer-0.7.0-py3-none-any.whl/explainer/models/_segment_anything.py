from PIL import Image
import numpy as np

from explainer.util.segment_anything import (
    SamAutomaticMaskGenerator,
    sam_model_registry,
)
from explainer.util.segment_anything.modeling.sam import Sam

from ._api import ModelType, register_model
from .base import SegmentationModel

__all__ = [
    "segment_to_image",
    "SamSegmentation",
]


def get_mask(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x["area"]), reverse=True)

    n, m = sorted_anns[0]["segmentation"].shape

    mask = np.zeros((n, m), dtype=int)

    for idx, ann in enumerate(sorted_anns):
        indices = ann["segmentation"]
        mask[indices] = idx + 1

    return mask


def segment_to_image(segmentation):
    unique_labels = np.unique(segmentation)
    num_classes = len(unique_labels) - 1  # Exclude background label

    colors = np.random.randint(0, 255, size=(num_classes, 3), dtype=np.uint8)
    colors = np.vstack([[0, 0, 0], colors])  # Add black color for background label

    height, width = segmentation.shape
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for label in unique_labels:
        if label == 0:  # Skip background label
            continue
        mask = segmentation == label
        image[mask] = colors[label]

    return image


def get_np_img(img: Image):
    return np.array(img)


class SamSegmentation(SegmentationModel):
    def __init__(
        self,
        sam: Sam,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.sam = sam
        self.mask_generator = SamAutomaticMaskGenerator(
            sam,
            min_mask_region_area=1000,  # default 0, sets the minimum area of a segment, increase this to filter out smaller segments
            pred_iou_thresh=0.96,  # default 0.88, a larger value improves the smoothness at the edges between two segments, if the value is to large weird artifacts occur
            stability_score_offset=0.1,  # default 1, with a lower value more segments are detected, a value to low can lead to an oversegmentation, the quality/smothness/size of the segments is not affected by this parameter
            box_nms_thresh=0.5,  # default 0.7, larger values reduce the area (black segment) where no segments are detected but reduce the quality, smaller values increase the area (black segment) where no segments are detected but increase the quality, so 0.5 may be a good tradeoff
            crop_n_layers=0,  # default 0, set this to 1 to obtain more finer/detailed segments but with added noise, increasing this value further will result in increased running time
        )

    def load_state_dict(self, state_dict):
        # Overwrite this method to enable loading
        self.sam.load_state_dict(state_dict)

    def forward(self, *_):
        raise NotImplementedError("Don't call this method directly.")

    def _prepare_img(self, img: Image) -> np.ndarray:
        return self.input_transform(img)

    def _predict(self, x: np.ndarray):
        # Overwrite this method to enable prediction
        anns = self.mask_generator.generate(x)
        return self.output_handle(anns)


def _create_sam_model(name, model_key, weights_url):
    @register_model(
        model_type=ModelType.SEGMENTATION_MODEL,
        weights_url=weights_url,
        name=name,
        config={
            "input_transform": get_np_img,
            "output_handle": get_mask,
        },
    )
    def sam_model(**kwargs):
        sam = sam_model_registry[model_key]()
        return SamSegmentation(sam, **kwargs)

    return sam_model


_create_sam_model(
    "segment_anything_huge",
    "vit_h",
    "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth",
)
_create_sam_model(
    "segment_anything_large",
    "vit_l",
    "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth",
)
_create_sam_model(
    "segment_anything_base",
    "vit_b",
    "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth",
)
