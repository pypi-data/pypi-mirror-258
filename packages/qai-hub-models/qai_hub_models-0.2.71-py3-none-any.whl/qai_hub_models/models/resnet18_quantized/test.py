from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.resnet18_quantized.demo import main as demo_main
from qai_hub_models.models.resnet18_quantized.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    ResNet18Quantizable,
)


def test_task():
    run_imagenet_classifier_test(
        ResNet18Quantizable.from_pretrained(),
        MODEL_ID,
        probability_threshold=0.45,
        diff_tol=0.005,
        rtol=0.02,
        atol=0.2,
        asset_version=MODEL_ASSET_VERSION,
    )


def test_trace():
    run_imagenet_classifier_trace_test(
        ResNet18Quantizable.from_pretrained(),
        diff_tol=0.007,
        rtol=0.02,
        atol=0.2,
        is_quantized=True,
    )


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
