from __future__ import annotations

import torchvision.models as tv_models

from qai_hub_models.models._shared.imagenet_classifier.model import ImagenetClassifier

MODEL_ID = "squeezenet1_1"
DEFAULT_WEIGHTS = "IMAGENET1K_V1"


class SqueezeNet(ImagenetClassifier):
    @classmethod
    def from_pretrained(cls, weights: str = DEFAULT_WEIGHTS) -> ImagenetClassifier:
        net = tv_models.squeezenet1_1(weights=weights)
        return cls(net)
