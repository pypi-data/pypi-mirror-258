import argparse

from qai_hub_models.models.esrgan.app import ESRGANApp
from qai_hub_models.models.esrgan.model import ESRGAN, MODEL_ASSET_VERSION, MODEL_ID
from qai_hub_models.utils.args import add_output_dir_arg
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.display import display_or_save_image

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "esrgan_demo.jpg"
)


# Run ESRGAN end-to-end on a sample image.
# The demo will display a image upscaled with no loss in quality.
def main(is_test: bool = False):
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        default=IMAGE_ADDRESS,
        help="image file path or URL.",
    )
    add_output_dir_arg(parser)

    args = parser.parse_args([] if is_test else None)

    # Load image & model
    app = ESRGANApp(ESRGAN.from_pretrained())
    image = load_image(args.image)
    pred_image = app.upscale_image(image)
    if not is_test:
        display_or_save_image(
            image, args.output_dir, "original_image.png", "original image"
        )
        display_or_save_image(
            pred_image, args.output_dir, "upscaled_image.png", "upscaled image"
        )


if __name__ == "__main__":
    main()
