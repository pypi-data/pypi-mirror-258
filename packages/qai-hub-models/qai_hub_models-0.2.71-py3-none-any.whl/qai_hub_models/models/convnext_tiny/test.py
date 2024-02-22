from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.convnext_tiny.demo import main as demo_main
from qai_hub_models.models.convnext_tiny.model import MODEL_ID, ConvNextTiny


def test_task():
    run_imagenet_classifier_test(ConvNextTiny.from_pretrained(), MODEL_ID)


def test_trace():
    run_imagenet_classifier_trace_test(ConvNextTiny.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
