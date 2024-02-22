from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.inception_v3.demo import main as demo_main
from qai_hub_models.models.inception_v3.model import MODEL_ID, InceptionNetV3


def test_task():
    run_imagenet_classifier_test(InceptionNetV3.from_pretrained(), MODEL_ID)


def test_trace():
    run_imagenet_classifier_trace_test(InceptionNetV3.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
