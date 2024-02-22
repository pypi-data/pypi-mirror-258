from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.mobilenet_v2_quantized.demo import main as demo_main
from qai_hub_models.models.mobilenet_v2_quantized.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    MobileNetV2Quantizable,
)
from qai_hub_models.utils.testing import skip_clone_repo_check


@skip_clone_repo_check
def test_task():
    run_imagenet_classifier_test(
        MobileNetV2Quantizable.from_pretrained(),
        MODEL_ID,
        asset_version=MODEL_ASSET_VERSION,
        probability_threshold=0.56,
        diff_tol=0.06,
    )


@skip_clone_repo_check
def test_trace():
    run_imagenet_classifier_trace_test(
        MobileNetV2Quantizable.from_pretrained(),
        is_quantized=True,
        atol=0.03,
    )


@skip_clone_repo_check
def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
