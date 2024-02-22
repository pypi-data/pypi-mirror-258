from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.shufflenet_v2.demo import main as demo_main
from qai_hub_models.models.shufflenet_v2.model import MODEL_ID, ShufflenetV2


def test_task():
    run_imagenet_classifier_test(ShufflenetV2.from_pretrained(), MODEL_ID)


def test_trace():
    run_imagenet_classifier_trace_test(ShufflenetV2.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
