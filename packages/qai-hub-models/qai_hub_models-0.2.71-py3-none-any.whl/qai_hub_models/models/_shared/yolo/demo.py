from __future__ import annotations

from typing import Callable, Type

from PIL import Image

from qai_hub_models.models._shared.yolo.app import YoloObjectDetectionApp
from qai_hub_models.utils.args import (
    demo_model_from_cli_args,
    get_model_cli_parser,
    get_on_device_demo_parser,
    validate_on_device_demo_args,
)
from qai_hub_models.utils.asset_loaders import CachedWebAsset, load_image
from qai_hub_models.utils.base_model import BaseModel
from qai_hub_models.utils.display import display_or_save_image
from qai_hub_models.utils.quantization import make_image_sample_data_loader


# Run Yolo end-to-end on a sample image.
# The demo will display a image with the predicted bounding boxes.
def yolo_detection_demo(
    model_type: Type[BaseModel],
    app_type: Callable[..., YoloObjectDetectionApp],
    default_image: str | CachedWebAsset,
    stride_multiple: int | None = None,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_type)
    parser = get_on_device_demo_parser(parser, add_output_dir=True)
    image_help = "image file path or URL."
    if stride_multiple:
        image_help = f"{image_help} Image spatial dimensions (x and y) must be multiples of {stride_multiple}."
    parser.add_argument("--image", type=str, default=default_image, help=image_help)
    parser.add_argument(
        "--score-threshold",
        type=float,
        default=0.45,
        help="Score threshold for NonMaximumSuppression",
    )
    parser.add_argument(
        "--iou-threshold",
        type=float,
        default=0.7,
        help="Intersection over Union (IoU) threshold for NonMaximumSuppression",
    )
    parser.add_argument(
        "--run-quantization",
        action="store_true",
        help="Set the flag to run post_train_quantization on sample data.",
    )
    args = parser.parse_args([] if is_test else None)
    validate_on_device_demo_args(args, model_type.get_model_id())

    if args.run_quantization:
        # Override default quantized weight to use fp32 weight
        args.weights_name = ""
    model = demo_model_from_cli_args(model_type, args)

    if args.run_quantization:
        # model is not quantized if we load fp32 weights instead of
        # int8 weights
        calibration_data_loader = make_image_sample_data_loader()
        model.post_train_quantization(calibration_data_loader)

    app = app_type(model, args.score_threshold, args.iou_threshold)
    print("Model Loaded")
    image = load_image(args.image)
    pred_images = app.predict_boxes_from_image(image)
    out = Image.fromarray(pred_images[0])
    if not is_test:
        display_or_save_image(out, args.output_dir, "yolo_demo_output.png")
