import numpy as np

from qai_hub_models.models.fcn_resnet50.app import FCN_ResNet50App
from qai_hub_models.models.fcn_resnet50.demo import INPUT_IMAGE_ADDRESS
from qai_hub_models.models.fcn_resnet50.demo import main as demo_main
from qai_hub_models.models.fcn_resnet50.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    FCN_ResNet50,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.testing import skip_clone_repo_check

OUTPUT_IMAGE_LOCAL_PATH = "fcn_demo_output.png"
OUTPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, OUTPUT_IMAGE_LOCAL_PATH
)


def _test_impl(app: FCN_ResNet50App):
    image = load_image(INPUT_IMAGE_ADDRESS)
    output_image = load_image(OUTPUT_IMAGE_ADDRESS)
    app_output_image = app.predict(image, False)

    np.testing.assert_allclose(
        np.asarray(app_output_image, dtype=np.float32) / 255,
        np.asarray(output_image, dtype=np.float32) / 255,
        rtol=0.02,
        atol=0.2,
    )


@skip_clone_repo_check
def test_task():
    _test_impl(FCN_ResNet50App(FCN_ResNet50.from_pretrained()))


@skip_clone_repo_check
def test_trace():
    _test_impl(FCN_ResNet50App(FCN_ResNet50.from_pretrained().convert_to_torchscript()))


def test_demo():
    demo_main(is_test=True)
