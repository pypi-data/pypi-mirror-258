from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.resnext101.demo import main as demo_main
from qai_hub_models.models.resnext101.model import MODEL_ID, ResNeXt101


def test_task():
    run_imagenet_classifier_test(
        ResNeXt101.from_pretrained(), MODEL_ID, atol=0.02, rtol=0.02, diff_tol=0.005
    )


def test_trace():
    run_imagenet_classifier_trace_test(ResNeXt101.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
