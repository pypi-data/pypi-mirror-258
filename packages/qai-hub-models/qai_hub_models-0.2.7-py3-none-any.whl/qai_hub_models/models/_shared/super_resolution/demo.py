from __future__ import annotations

from typing import Type

from qai_hub_models.models._shared.super_resolution.app import SuperResolutionApp
from qai_hub_models.utils.args import (
    demo_model_from_cli_args,
    get_model_cli_parser,
    get_on_device_demo_parser,
    validate_on_device_demo_args,
)
from qai_hub_models.utils.asset_loaders import CachedWebAsset, load_image
from qai_hub_models.utils.base_model import BaseModel
from qai_hub_models.utils.display import display_or_save_image


# Run Super Resolution end-to-end on a sample image.
# The demo will display both the input image and the higher resolution output.
def super_resolution_demo(
    model_cls: Type[BaseModel],
    default_image: str | CachedWebAsset,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_cls)
    parser = get_on_device_demo_parser(parser, add_output_dir=True)
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="image file path or URL.",
    )

    args = parser.parse_args([] if is_test else None)
    validate_on_device_demo_args(args, model_cls.get_model_id())

    # Load image & model
    model = demo_model_from_cli_args(model_cls, args)
    app = SuperResolutionApp(model)
    print("Model Loaded")
    image = load_image(args.image)
    pred_images = app.upscale_image(image)
    if not is_test:
        display_or_save_image(
            image, args.output_dir, "original_image.png", "original image"
        )
        display_or_save_image(
            pred_images[0], args.output_dir, "upscaled_image.png", "upscaled image"
        )
